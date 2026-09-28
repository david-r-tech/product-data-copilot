import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.export.export_helpers import (  # noqa: E402
    IMPROVED_EXCEL_EXPORT_FILENAME,
    IMPROVED_EXCEL_EXPORT_SHEETS,
    IMPROVED_EXPORT_SUMMARY_COLUMNS,
    IMPROVED_EXPORT_STATUS_GROUPS,
    IMPROVED_PRODUCT_EXPORT_COLUMNS,
    MANAGEMENT_EXPORT_SHEETS,
    MANAGEMENT_EXPORT_FILENAME,
    build_export_filename,
    build_improved_excel_export_sheets,
    build_improved_export_summary,
    dataframe_has_columns,
    dataframe_has_rows,
    has_required_sheets,
    missing_required_sheets,
    normalize_improved_export_status,
    ordered_columns,
    required_improved_excel_export_sheets,
    required_management_export_sheets,
    safe_sheet_name,
    source_products_to_snapshot_dataframe,
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
        "Source Products",
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
    suggestions = pd.DataFrame(columns=["sku", "target_field", "proposed_value"])
    assert dataframe_has_columns(suggestions, ["sku", "proposed_value"])
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
    assert normalize_improved_export_status({"approval_status": "approved"}) == "pending"
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


def _improved_excel_export_suggestions():
    return [
        {
            "sku": "SKU-11",
            "product_name": "Demo Bottle",
            "target_field": "product_name",
            "current_value": "Bottle",
            "proposed_value": "Demo Trail Bottle",
            "source_fields": ["product_name", "category"],
            "reason": "User approved clearer title.",
            "confidence": "high",
            "human_review_status": "approved",
            "suggestion_status": "review_required",
        },
        {
            "sku": "SKU-12",
            "product_name": "Office Lamp",
            "target_field": "description",
            "current_value": "Lamp",
            "proposed_value": "Adjustable office lamp for desks.",
            "approval_status": "needs_review",
            "suggestion_status": "review_required",
        },
        {
            "sku": "SKU-13",
            "product_name": "Rejected Shirt",
            "target_field": "description",
            "human_review_status": "rejected",
        },
        {
            "sku": "SKU-14",
            "product_name": "Blocked Toy",
            "target_field": "warning_notes",
            "human_review_status": "approved",
            "suggestion_status": "blocked_insufficient_source",
        },
        {
            "sku": "SKU-15",
            "product_name": "Unknown Item",
            "target_field": "description",
            "approval_status": "unclear",
        },
    ]


def test_improved_excel_export_filename_and_sheet_order_are_stable():
    assert IMPROVED_EXCEL_EXPORT_FILENAME == "product_data_copilot_improved_export.xlsx"
    assert IMPROVED_EXCEL_EXPORT_SHEETS == [
        "Export Summary",
        "Reviewed Product Data",
        "Approved Improvements",
        "Pending Suggestions",
        "Rejected Suggestions",
        "Blocked Suggestions",
        "Unknown Suggestions",
        "Original Source Snapshot",
    ]
    assert required_improved_excel_export_sheets() == IMPROVED_EXCEL_EXPORT_SHEETS


def test_required_improved_excel_export_sheets_returns_copy():
    sheets = required_improved_excel_export_sheets()
    sheets.append("Extra")

    assert "Extra" not in required_improved_excel_export_sheets()


def test_build_improved_excel_export_sheets_contains_all_expected_sheets():
    sheets = build_improved_excel_export_sheets(_improved_excel_export_suggestions())

    assert list(sheets.keys()) == IMPROVED_EXCEL_EXPORT_SHEETS
    assert has_required_sheets(sheets, IMPROVED_EXCEL_EXPORT_SHEETS)


def test_improved_export_summary_counts_status_groups():
    summary = build_improved_export_summary(_improved_excel_export_suggestions())
    summary_values = dict(zip(summary["metric"], summary["value"]))

    assert list(summary.columns) == IMPROVED_EXPORT_SUMMARY_COLUMNS
    assert summary_values["total_reviewable_suggestions"] == 5
    assert summary_values["approved_improvement_count"] == 1
    assert summary_values["pending_suggestion_count"] == 1
    assert summary_values["rejected_suggestion_count"] == 1
    assert summary_values["blocked_suggestion_count"] == 1
    assert summary_values["unknown_suggestion_count"] == 1
    assert summary_values["source_data_changed"] == "No"
    assert summary_values["write_back_enabled"] == "No"


def test_original_source_snapshot_is_included_when_source_data_provided():
    source_products = pd.DataFrame(
        [
            {
                "sku": "SKU-11",
                "product_name": "Bottle",
                "description": "Original product data",
            }
        ]
    )

    sheets = build_improved_excel_export_sheets(
        _improved_excel_export_suggestions(),
        source_products=source_products,
    )
    snapshot = sheets["Original Source Snapshot"]

    assert len(snapshot) == 1
    assert snapshot.iloc[0]["product_name"] == "Bottle"


def test_missing_source_data_creates_safe_empty_snapshot():
    snapshot = source_products_to_snapshot_dataframe()
    sheets = build_improved_excel_export_sheets(_improved_excel_export_suggestions())

    assert isinstance(snapshot, pd.DataFrame)
    assert len(snapshot) == 0
    assert isinstance(sheets["Original Source Snapshot"], pd.DataFrame)
    assert len(sheets["Original Source Snapshot"]) == 0


def test_improved_excel_export_helpers_do_not_mutate_inputs():
    suggestions = _improved_excel_export_suggestions()
    source_products = [
        {
            "sku": "SKU-11",
            "product_name": "Bottle",
            "description": "Original product data",
        }
    ]
    original_suggestions = [dict(record) for record in suggestions]
    original_source = [dict(record) for record in source_products]

    build_improved_excel_export_sheets(suggestions, source_products)

    assert suggestions == original_suggestions
    assert source_products == original_source


def test_approved_suggestions_are_not_applied_to_original_source_rows():
    source_products = [
        {
            "sku": "SKU-11",
            "product_name": "Bottle",
            "description": "Original product data",
        }
    ]

    sheets = build_improved_excel_export_sheets(
        _improved_excel_export_suggestions(),
        source_products=source_products,
    )

    approved = sheets["Approved Improvements"]
    snapshot = sheets["Original Source Snapshot"]

    assert approved.iloc[0]["approved_value"] == "Demo Trail Bottle"
    assert snapshot.iloc[0]["product_name"] == "Bottle"


def test_reviewed_product_data_applies_only_matching_human_approved_edits():
    source = pd.DataFrame([{
        "sku": "ONE", "product_name": "Bottle", "description": "Original text",
        "translation_de": "",
    }])
    suggestions = [
        {"sku": "ONE", "target_field": "description", "current_value": "Original text",
         "proposed_value": "Clear product text", "human_review_status": "approved"},
        {"sku": "ONE", "target_field": "translation_de", "current_value": "",
         "proposed_value": "Deutscher Text", "human_review_status": "pending"},
    ]
    sheets = build_improved_excel_export_sheets(suggestions, source)
    assert sheets["Reviewed Product Data"].iloc[0]["description"] == "Clear product text"
    assert sheets["Reviewed Product Data"].iloc[0]["translation_de"] == ""
    assert sheets["Original Source Snapshot"].iloc[0]["description"] == "Original text"
    assert source.iloc[0]["description"] == "Original text"


def test_empty_suggestion_input_returns_stable_improved_excel_sheets():
    sheets = build_improved_excel_export_sheets()
    summary_values = dict(zip(sheets["Export Summary"]["metric"], sheets["Export Summary"]["value"]))

    assert list(sheets.keys()) == IMPROVED_EXCEL_EXPORT_SHEETS
    assert summary_values["total_reviewable_suggestions"] == 0
    for sheet_name in IMPROVED_EXCEL_EXPORT_SHEETS:
        assert isinstance(sheets[sheet_name], pd.DataFrame)

    for sheet_name in [
        "Approved Improvements",
        "Pending Suggestions",
        "Rejected Suggestions",
        "Blocked Suggestions",
        "Unknown Suggestions",
    ]:
        assert list(sheets[sheet_name].columns) == IMPROVED_PRODUCT_EXPORT_COLUMNS


def test_improved_excel_export_sheets_are_dataframes():
    sheets = build_improved_excel_export_sheets(
        _improved_excel_export_suggestions(),
        source_products=[{"sku": "SKU-11", "product_name": "Bottle"}],
    )

    assert all(isinstance(sheet, pd.DataFrame) for sheet in sheets.values())
