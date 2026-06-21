import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.export.export_helpers import (  # noqa: E402
    AI_SUGGESTIONS_EXPORT_COLUMNS,
    MANAGEMENT_EXPORT_SHEETS,
    MANAGEMENT_EXPORT_FILENAME,
    build_export_filename,
    dataframe_has_columns,
    dataframe_has_rows,
    has_required_sheets,
    missing_required_sheets,
    ordered_columns,
    required_management_export_sheets,
    safe_sheet_name,
)


def test_management_export_filename_is_stable():
    assert MANAGEMENT_EXPORT_FILENAME == "commerce_readiness_ai_management_export.xlsx"


def test_management_export_sheet_order_is_stable():
    assert MANAGEMENT_EXPORT_SHEETS == [
        "Management Summary",
        "Product Scores",
        "Issues",
        "Review Tasks",
        "AI Suggestions",
        "Source Products",
    ]


def test_ai_suggestions_export_columns_are_stable():
    assert AI_SUGGESTIONS_EXPORT_COLUMNS == [
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


def test_safe_sheet_name_replaces_invalid_excel_characters():
    assert safe_sheet_name("Issues: Critical/Warning?") == "Issues_ Critical_Warning_"
    assert safe_sheet_name("  Product Scores  ") == "Product Scores"


def test_safe_sheet_name_uses_fallback_and_limits_length():
    assert safe_sheet_name("", fallback="Export") == "Export"
    assert safe_sheet_name(None) == "Sheet"
    assert len(safe_sheet_name("a" * 40)) == 31


def test_build_export_filename():
    assert build_export_filename("review_tasks", "csv") == "review_tasks.csv"
    assert build_export_filename("report.xlsx", ".xlsx") == "report.xlsx"
    assert build_export_filename("", "csv") == "export.csv"
    assert build_export_filename("readme", "") == "readme"


def test_required_management_export_sheets_returns_copy():
    sheets = required_management_export_sheets()
    assert sheets == [
        "Management Summary",
        "Product Scores",
        "Issues",
        "Review Tasks",
        "AI Suggestions",
        "Source Products",
    ]

    sheets.append("Extra")
    assert "Extra" not in required_management_export_sheets()


def test_required_sheet_validation_accepts_mapping_or_list():
    sheet_mapping = {sheet: object() for sheet in required_management_export_sheets()}
    assert has_required_sheets(sheet_mapping)
    assert missing_required_sheets(sheet_mapping) == []

    partial_sheet_list = ["Management Summary", "Product Scores"]
    assert not has_required_sheets(partial_sheet_list)
    assert "Issues" in missing_required_sheets(partial_sheet_list)


def test_dataframe_has_rows():
    assert dataframe_has_rows(pd.DataFrame({"sku": ["A-1"]}))
    assert not dataframe_has_rows(pd.DataFrame(columns=["sku"]))
    assert not dataframe_has_rows(None)


def test_dataframe_has_columns():
    suggestions = pd.DataFrame(columns=AI_SUGGESTIONS_EXPORT_COLUMNS)
    assert dataframe_has_columns(suggestions, ["sku", "bullet_points"])
    assert not dataframe_has_columns(suggestions, ["missing_column"])
    assert not dataframe_has_columns(None, ["sku"])


def test_ordered_columns_keeps_preferred_columns_first():
    existing = ["price", "sku", "product_name", "brand"]
    preferred = ["sku", "product_name"]

    assert ordered_columns(existing, preferred) == [
        "sku",
        "product_name",
        "price",
        "brand",
    ]
