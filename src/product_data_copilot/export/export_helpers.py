"""Small, pure helpers for export preparation."""

import pandas as pd

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

IMPROVED_EXPORT_STATUS_GROUPS = [
    "approved",
    "pending",
    "rejected",
    "blocked",
    "unknown",
]

IMPROVED_PRODUCT_EXPORT_COLUMNS = [
    "sku",
    "product_name",
    "field",
    "current_value",
    "suggested_value",
    "original_value",
    "approved_value",
    "source",
    "reason",
    "confidence",
    "risk_level",
    "approval_status",
    "suggestion_status",
    "export_status",
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


def normalize_improved_export_status(suggestion):
    """Return a safe export status for a Smart Suggestions v2 record.

    These helpers prepare export data only. They do not approve suggestions,
    update source product data, or write changes back to uploaded files.
    """
    if not isinstance(suggestion, dict):
        return "unknown"

    suggestion_status = _normalize_status_text(suggestion.get("suggestion_status"))
    if suggestion_status in {"blocked", "blocked_insufficient_source"}:
        return "blocked"

    status_value = _first_non_blank_value(
        suggestion,
        ["human_review_status", "review_status", "approval_status"],
    )
    status_text = _normalize_status_text(status_value)

    if status_text in {"approved"}:
        return "approved"
    if status_text in {"rejected"}:
        return "rejected"
    if status_text in {"blocked", "blocked_insufficient_source"}:
        return "blocked"
    if status_text in {"pending", "needs_review", "review_required", "draft"}:
        return "pending"

    if suggestion_status in {"pending", "needs_review", "review_required", "draft"}:
        return "pending"

    return "unknown"


def smart_suggestion_to_export_row(suggestion):
    """Return one export-ready row without mutating the source suggestion.

    The returned row separates source/current values from approved values so a
    future export can stay review-focused and avoid automatic write-back.
    """
    if not isinstance(suggestion, dict):
        suggestion = {}

    export_status = normalize_improved_export_status(suggestion)
    current_value = _first_non_blank_value(
        suggestion,
        ["current_value", "original_value"],
    )
    suggested_value = _first_non_blank_value(
        suggestion,
        ["proposed_value", "suggested_value", "approved_value"],
    )

    row = {
        "sku": _text_value(suggestion.get("sku")),
        "product_name": _text_value(suggestion.get("product_name")),
        "field": _text_value(
            _first_non_blank_value(
                suggestion,
                ["target_field", "field", "field_name"],
            )
        ),
        "current_value": _text_value(current_value),
        "suggested_value": _text_value(suggested_value),
        "original_value": _text_value(current_value),
        "approved_value": _text_value(suggested_value)
        if export_status == "approved"
        else "",
        "source": _source_value(
            _first_non_blank_value(suggestion, ["source_fields", "source"])
        ),
        "reason": _text_value(suggestion.get("reason")),
        "confidence": _text_value(suggestion.get("confidence")),
        "risk_level": _text_value(suggestion.get("risk_level")),
        "approval_status": export_status,
        "suggestion_status": _text_value(suggestion.get("suggestion_status")),
        "export_status": export_status,
    }

    return {column: row.get(column, "") for column in IMPROVED_PRODUCT_EXPORT_COLUMNS}


def smart_suggestions_to_export_dataframe(suggestions):
    """Return export-ready Smart Suggestions v2 rows as a stable DataFrame.

    The input can be a list of dictionaries, one dictionary, or a pandas
    DataFrame. The original input is never mutated.
    """
    rows = [
        smart_suggestion_to_export_row(suggestion)
        for suggestion in _suggestion_records(suggestions)
    ]

    return pd.DataFrame(rows, columns=IMPROVED_PRODUCT_EXPORT_COLUMNS)


def split_smart_suggestions_for_export(suggestions):
    """Split Smart Suggestions v2 records into safe export DataFrame groups.

    Groups are `approved`, `pending`, `rejected`, `blocked`, and `unknown`.
    This only prepares derived export data; it does not apply changes to source
    product data and does not write files.
    """
    export_dataframe = smart_suggestions_to_export_dataframe(suggestions)
    grouped_dataframes = {}

    for status_group in IMPROVED_EXPORT_STATUS_GROUPS:
        if len(export_dataframe) == 0:
            grouped_dataframes[status_group] = pd.DataFrame(
                columns=IMPROVED_PRODUCT_EXPORT_COLUMNS
            )
        else:
            grouped_dataframes[status_group] = export_dataframe[
                export_dataframe["export_status"] == status_group
            ].copy()

    return grouped_dataframes


def _suggestion_records(suggestions):
    """Return a copied list of suggestion dictionaries."""
    if suggestions is None:
        return []

    if isinstance(suggestions, pd.DataFrame):
        return [dict(record) for record in suggestions.to_dict(orient="records")]

    if isinstance(suggestions, dict):
        return [dict(suggestions)]

    try:
        return [dict(record) for record in suggestions if isinstance(record, dict)]
    except TypeError:
        return []


def _first_non_blank_value(record, field_names):
    for field_name in field_names:
        value = record.get(field_name)
        if not _is_blank_value(value):
            return value
    return ""


def _normalize_status_text(value):
    return _text_value(value).lower().replace("-", "_").replace(" ", "_")


def _source_value(value):
    if isinstance(value, (list, tuple, set)):
        return ", ".join(_text_value(item) for item in value if _text_value(item) != "")
    return _text_value(value)


def _is_blank_value(value):
    if value is None:
        return True
    if isinstance(value, (list, tuple, set)):
        return len([item for item in value if _text_value(item) != ""]) == 0
    return _text_value(value) == ""


def _text_value(value):
    if value is None:
        return ""
    return str(value).strip()
