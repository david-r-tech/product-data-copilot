from io import BytesIO

import pandas as pd
import pytest
from openpyxl import Workbook

from product_data_copilot.data.product_input import (
    MAX_FILE_BYTES, MAX_PRODUCTS, ProductInputError, dataset_fingerprint, load_product_file,
)


def excel_file(headers, rows):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(headers)
    for row in rows:
        sheet.append(row)
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()


@pytest.mark.parametrize("delimiter", [",", ";", "\t"])
def test_csv_identifiers_and_literal_na_are_preserved(delimiter):
    content = delimiter.join(["sku", "product_name", "ean", "brand"]) + "\n"
    content += delimiter.join(["000123", "Storage box", "0123456789012", "NA"])
    data = load_product_file(content.encode("utf-8-sig"), "products.CSV")
    assert data.iloc[0].to_dict() == {
        "sku": "000123", "product_name": "Storage box", "ean": "0123456789012", "brand": "NA",
    }


def test_excel_identifiers_formulas_and_blank_optional_fields_are_preserved():
    content = excel_file(["sku", "product_name", "ean", "description", "brand"], [
        ["000123", "Storage box", "0123456789012", "=1+1", None],
    ])
    data = load_product_file(content, "products.XLSX")
    assert data.iloc[0]["sku"] == "000123"
    assert data.iloc[0]["ean"] == "0123456789012"
    assert data.iloc[0]["description"] == "=1+1"
    assert data.iloc[0]["brand"] == ""


@pytest.mark.parametrize("content,filename,message", [
    (b"", "a.csv", "empty"),
    (b"sku,product_name\n", "a.csv", "no product rows"),
    (b"name,price\nBox,10\n", "a.csv", "Missing required"),
    (b"sku,product_name\n,Box\n", "a.csv", "Missing SKU"),
    (b"sku,product_name\nA,Box\n A ,Bag", "a.csv", "Duplicate SKUs"),
    (b"sku,product_name,SKU\nA,Box,B", "a.csv", "unique"),
    (b"sku,product_name\nA,Box,extra", "a.csv", "expected 2"),
    (b'sku,product_name\nA,"unclosed', "a.csv", "malformed"),
    (b"sku,product_name\nA,\xff", "a.csv", "UTF-8"),
    (b"not excel", "a.xlsx", "valid, unencrypted"),
    (b"anything", "a.xls", "CSV or XLSX"),
])
def test_invalid_files_have_actionable_errors(content, filename, message):
    with pytest.raises(ProductInputError, match=message):
        load_product_file(content, filename)


def test_import_limits_are_enforced():
    with pytest.raises(ProductInputError, match="10 MB"):
        load_product_file(b"x" * (MAX_FILE_BYTES + 1), "a.csv")
    content = "sku,product_name\n" + "\n".join(f"{i},Box" for i in range(MAX_PRODUCTS + 1))
    with pytest.raises(ProductInputError, match="1,000"):
        load_product_file(content.encode(), "a.csv")


def test_empty_excel_is_rejected():
    with pytest.raises(ProductInputError):
        load_product_file(excel_file([], []), "empty.xlsx")


def test_quoted_csv_multiline_text_and_optional_columns(valid_product):
    valid_product["description"] = 'Two lines, with "quoted" text.\nSecond line.'
    content = pd.DataFrame([valid_product]).to_csv(index=False).encode()
    data = load_product_file(content, "a.csv")
    assert data.iloc[0].to_dict() == valid_product


def test_dataset_identity_includes_all_bytes_and_source_name():
    assert dataset_fingerprint(b"a", "one.csv") == dataset_fingerprint(b"a", "one.csv")
    assert dataset_fingerprint(b"a", "one.csv") != dataset_fingerprint(b"b", "one.csv")
    assert dataset_fingerprint(b"a", "one.csv") != dataset_fingerprint(b"a", "two.csv")
