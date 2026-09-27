"""Read bounded local product files without coercing identifiers to numbers."""

import csv
import hashlib
from io import BytesIO, StringIO
from pathlib import Path
from xml.etree.ElementTree import ParseError
from zipfile import BadZipFile, ZipFile

import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_UNCOMPRESSED_BYTES = 50 * 1024 * 1024
MAX_PRODUCTS = 1000
MAX_COLUMNS = 100
REQUIRED_COLUMNS = {"sku", "product_name"}


class ProductInputError(ValueError):
    """An input problem that can be shown directly to the user."""


def dataset_fingerprint(content, source_name):
    """Scope review state to the complete input, including its source identity."""
    return hashlib.sha256(source_name.encode("utf-8") + b"\0" + content).hexdigest()


def validate_product_identity(products):
    """Reject ambiguous product identity before issues or decisions are assigned."""
    if "sku" not in products:
        raise ProductInputError("The file must contain a sku column.")
    skus = products["sku"].fillna("").astype(str).str.strip()
    if skus.eq("").any():
        rows = [str(i + 2) for i, blank in enumerate(skus.eq("")) if blank]
        raise ProductInputError(
            "Every product needs a SKU. Missing SKU in data row(s): "
            + ", ".join(rows[:10]) + ". Correct the file and upload it again."
        )
    if skus.duplicated(keep=False).any():
        raise ProductInputError(
            "SKUs must be unique. Duplicate SKUs were found; correct the file "
            "before reviewing products."
        )


def load_product_file(content, filename):
    """Load UTF-8 CSV or the first XLSX sheet; formulas remain literal text.

    All imported cells are text. Column names and SKUs are trimmed. Other cell
    text is retained; optional absent columns are handled by the rule engine.
    """
    if not content:
        raise ProductInputError("The file is empty. Upload a file with product rows.")
    if len(content) > MAX_FILE_BYTES:
        raise ProductInputError("The file exceeds the local MVP limit of 10 MB.")
    suffix = Path(filename).suffix.lower()
    if suffix == ".csv":
        rows = _read_csv_rows(content)
    elif suffix == ".xlsx":
        rows = _read_excel_rows(content)
    else:
        raise ProductInputError("Use a CSV or XLSX file.")
    if not rows:
        raise ProductInputError("The file has no header or product rows.")
    headers = [str(value).strip().lower() for value in rows[0]]
    if len(headers) > MAX_COLUMNS:
        raise ProductInputError("Use at most 100 columns per product file.")
    if any(not header for header in headers) or len(set(headers)) != len(headers):
        raise ProductInputError("Column names must be non-empty and unique.")
    missing = sorted(REQUIRED_COLUMNS - set(headers))
    if missing:
        raise ProductInputError(
            "Missing required column(s): " + ", ".join(missing)
            + ". Use the sample file as the column template."
        )
    records = []
    for row_number, row in enumerate(rows[1:], start=2):
        if not any(str(value).strip() for value in row):
            continue
        if len(row) != len(headers):
            raise ProductInputError(
                f"Row {row_number} has {len(row)} cells; expected {len(headers)}. "
                "Check the delimiter and quote text containing delimiters."
            )
        records.append(row)
    if not records:
        raise ProductInputError("The file contains headers but no product rows.")
    if len(records) > MAX_PRODUCTS:
        raise ProductInputError("Use at most 1,000 products per file in this local MVP.")
    products = pd.DataFrame(records, columns=headers, dtype=str)
    products["sku"] = products["sku"].str.strip()
    validate_product_identity(products)
    return products


def _read_csv_rows(content):
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ProductInputError("Save the CSV as UTF-8, then upload it again.") from error
    header_line = text.splitlines()[0] if text.splitlines() else ""
    try:
        delimiter = csv.Sniffer().sniff(header_line, delimiters=",;\t").delimiter
    except csv.Error:
        delimiter = ","
    try:
        return list(csv.reader(StringIO(text, newline=""), delimiter=delimiter, strict=True))
    except csv.Error as error:
        raise ProductInputError("The CSV is malformed. Check its quotes and delimiters.") from error


def _read_excel_rows(content):
    workbook = None
    try:
        with ZipFile(BytesIO(content)) as archive:
            if sum(info.file_size for info in archive.infolist()) > MAX_UNCOMPRESSED_BYTES:
                raise ProductInputError("The expanded workbook is too large for this local MVP.")
        workbook = load_workbook(BytesIO(content), read_only=True, data_only=False)
        sheet = workbook.worksheets[0]
        # Do not trust inflated worksheet dimensions written by other tools.
        sheet.reset_dimensions()
        rows = []
        for row in sheet.iter_rows(values_only=True):
            if len(row) > MAX_COLUMNS:
                raise ProductInputError("Use at most 100 columns per product file.")
            rows.append(["" if value is None else str(value) for value in row])
            if len(rows) > MAX_PRODUCTS + 1:
                raise ProductInputError("Use at most 1,000 products per file in this local MVP.")
        # XLSX rows omit trailing empty cells. Pad to the header width only.
        if rows:
            rows = [row + [""] * max(0, len(rows[0]) - len(row)) for row in rows]
        return rows
    except ProductInputError:
        raise
    except (BadZipFile, InvalidFileException, ParseError, ValueError, KeyError, IndexError, OSError) as error:
        raise ProductInputError("The Excel file could not be read. Upload a valid, unencrypted XLSX workbook.") from error
    finally:
        if workbook is not None:
            workbook.close()
