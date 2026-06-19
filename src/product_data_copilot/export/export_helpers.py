"""Small, pure helpers for export preparation."""

MANAGEMENT_EXPORT_FILENAME = "commerce_readiness_ai_management_export.xlsx"

MANAGEMENT_EXPORT_SHEETS = [
    "Management Summary",
    "Product Scores",
    "Issues",
    "Review Tasks",
    "AI Suggestions",
    "Source Products",
]

AI_SUGGESTIONS_EXPORT_COLUMNS = [
    "sku",
    "selected_suggestion_types",
    "improved_product_title",
    "improved_product_description",
    "bullet_points",
    "suggested_missing_attributes",
    "translation",
    "compliance_safety_review_note",
    "human_review_notes",
]

EXCEL_SHEET_NAME_MAX_LENGTH = 31
INVALID_EXCEL_SHEET_CHARACTERS = set("[]:*?/\\")


def safe_sheet_name(sheet_name, fallback="Sheet"):
    """Return an Excel-safe sheet name."""
    if sheet_name is None:
        sheet_name = ""

    text = str(sheet_name).strip()
    cleaned = "".join(
        "_" if char in INVALID_EXCEL_SHEET_CHARACTERS else char for char in text
    )
    cleaned = cleaned.strip().strip("'")

    if cleaned == "":
        cleaned = str(fallback).strip() or "Sheet"

    return cleaned[:EXCEL_SHEET_NAME_MAX_LENGTH]


def build_export_filename(base_name, extension):
    """Return a simple export filename with the requested extension."""
    base = str(base_name or "export").strip()
    file_extension = str(extension or "").strip().lstrip(".")

    if base == "":
        base = "export"
    if file_extension == "":
        return base
    if base.lower().endswith(f".{file_extension.lower()}"):
        return base

    return f"{base}.{file_extension}"


def required_management_export_sheets():
    """Return the expected management export sheet names."""
    return MANAGEMENT_EXPORT_SHEETS.copy()


def missing_required_sheets(available_sheets, required_sheets=None):
    """Return required sheet names that are missing from an export mapping/list."""
    if required_sheets is None:
        required_sheets = MANAGEMENT_EXPORT_SHEETS

    if hasattr(available_sheets, "keys"):
        available_names = set(available_sheets.keys())
    else:
        available_names = set(available_sheets)

    return [sheet for sheet in required_sheets if sheet not in available_names]


def has_required_sheets(available_sheets, required_sheets=None):
    """Return True when all required sheets are present."""
    return len(missing_required_sheets(available_sheets, required_sheets)) == 0


def dataframe_has_rows(dataframe):
    """Return True when a dataframe-like object has at least one row."""
    if dataframe is None:
        return False

    try:
        return len(dataframe) > 0
    except TypeError:
        return False


def dataframe_has_columns(dataframe, required_columns):
    """Return True when a dataframe-like object contains all required columns."""
    if dataframe is None or not hasattr(dataframe, "columns"):
        return False

    return all(column in dataframe.columns for column in required_columns)


def ordered_columns(existing_columns, preferred_columns):
    """Return preferred columns first, followed by remaining existing columns."""
    existing_columns = list(existing_columns)
    preferred_columns = list(preferred_columns)

    ordered = [column for column in preferred_columns if column in existing_columns]
    ordered.extend(column for column in existing_columns if column not in ordered)

    return ordered
