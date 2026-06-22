import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.export.export_helpers import (  # noqa: E402
    AI_SUGGESTIONS_EXPORT_COLUMNS,
    IMPROVED_EXPORT_STATUS_GROUPS,
    IMPROVED_PRODUCT_EXPORT_COLUMNS,
    MANAGEMENT_EXPORT_SHEETS,
    MANAGEMENT_EXPORT_FILENAME,
    build_export_filename,
    dataframe_has_columns,
    dataframe_has_rows,
    has_required_sheets,
    missing_required_sheets,
    normalize_improved_export_status,
    ordered_columns,
    required_management_export_sheets,
    safe_sheet_name,
    smart_suggestions_to_export_dataframe,
    split_smart_suggestions_for_export,
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


def test_improved_export_status_groups_are_stable():
    assert IMPROVED_EXPORT_STATUS_GROUPS == [
        "approved",
        "pending",
        "rejected",
        "blocked",
        "unknown",
    ]


def test_improved_product_export_columns_are_stable():
    assert IMPROVED_PRODUCT_EXPORT_COLUMNS == [
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


def test_approved_suggestions_are_separated_correctly():
    suggestions = [
        {
            "sku": "SKU-1",
            "product_name": "Demo Bottle",
            "target_field": "product_name",
            "current_value": "Bottle",
            "proposed_value": "Demo Trail Bottle",
            "source_fields": ["product_name", "category"],
            "reason": "Human approved clearer title.",
            "confidence": "high",
            "human_review_status": "approved",
            "suggestion_status": "review_required",
        }
    ]

    grouped = split_smart_suggestions_for_export(suggestions)

    assert len(grouped["approved"]) == 1
    assert grouped["approved"].iloc[0]["approved_value"] == "Demo Trail Bottle"
    assert grouped["approved"].iloc[0]["export_status"] == "approved"
    assert len(grouped["pending"]) == 0


def test_pending_proposed_suggestions_are_separated_correctly():
    suggestions = [
        {
            "sku": "SKU-2",
            "field": "description",
            "current_value": "Short",
            "suggested_value": "Longer draft description.",
            "approval_status": "needs_review",
            "suggestion_status": "review_required",
        },
        {
            "sku": "SKU-3",
            "target_field": "bullet_points",
            "approval_status": "draft",
        },
    ]

    grouped = split_smart_suggestions_for_export(suggestions)

    assert len(grouped["pending"]) == 2
    assert grouped["pending"].iloc[0]["approved_value"] == ""
    assert set(grouped["pending"]["export_status"]) == {"pending"}


def test_rejected_and_blocked_suggestions_are_separated_correctly():
    suggestions = [
        {
            "sku": "SKU-4",
            "target_field": "description",
            "human_review_status": "rejected",
        },
        {
            "sku": "SKU-5",
            "target_field": "ean",
            "human_review_status": "approved",
            "suggestion_status": "blocked_insufficient_source",
        },
    ]

    grouped = split_smart_suggestions_for_export(suggestions)

    assert len(grouped["rejected"]) == 1
    assert len(grouped["blocked"]) == 1
    assert grouped["blocked"].iloc[0]["approval_status"] == "blocked"
    assert grouped["blocked"].iloc[0]["approved_value"] == ""


def test_missing_or_unknown_status_is_handled_safely():
    assert normalize_improved_export_status({}) == "unknown"
    assert normalize_improved_export_status({"approval_status": "not sure"}) == "unknown"

    grouped = split_smart_suggestions_for_export([{"sku": "SKU-6"}])

    assert len(grouped["unknown"]) == 1
    assert grouped["unknown"].iloc[0]["export_status"] == "unknown"


def test_smart_suggestions_export_helpers_do_not_mutate_original_input():
    suggestions = [
        {
            "sku": "SKU-7",
            "target_field": "description",
            "source_fields": ["product_name"],
            "approval_status": "needs_review",
        }
    ]
    original = [dict(suggestions[0])]
    original[0]["source_fields"] = list(suggestions[0]["source_fields"])

    split_smart_suggestions_for_export(suggestions)

    assert suggestions == original


def test_missing_optional_fields_do_not_crash_and_columns_stay_stable():
    dataframe = smart_suggestions_to_export_dataframe(
        [
            {
                "sku": "SKU-8",
                "approval_status": "approved",
            }
        ]
    )

    assert list(dataframe.columns) == IMPROVED_PRODUCT_EXPORT_COLUMNS
    assert dataframe.iloc[0]["sku"] == "SKU-8"
    assert dataframe.iloc[0]["field"] == ""
    assert dataframe.iloc[0]["source"] == ""


def test_smart_suggestions_export_helpers_accept_dataframes():
    suggestions_dataframe = pd.DataFrame(
        [
            {
                "sku": "SKU-9",
                "target_field": "description",
                "proposed_value": "Approved text",
                "human_review_status": "approved",
            }
        ]
    )

    grouped = split_smart_suggestions_for_export(suggestions_dataframe)

    assert len(grouped["approved"]) == 1
    assert grouped["approved"].iloc[0]["suggested_value"] == "Approved text"


def test_empty_source_fields_can_fall_back_to_source_value():
    dataframe = smart_suggestions_to_export_dataframe(
        [
            {
                "sku": "SKU-10",
                "target_field": "description",
                "source_fields": [],
                "source": "description",
                "approval_status": "needs_review",
            }
        ]
    )

    assert dataframe.iloc[0]["source"] == "description"
