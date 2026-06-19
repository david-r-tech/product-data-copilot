import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.review.review_helpers import (  # noqa: E402
    REVIEW_STATUS_COMPLIANCE_CHECK_REQUIRED,
    REVIEW_STATUS_MISSING_DATA,
    REVIEW_STATUS_NEEDS_REVIEW,
    REVIEW_STATUS_OK,
    REVIEW_STATUS_READY_FOR_EXPORT,
    REVIEW_STATUS_TRANSLATION_MISSING,
    TASK_PRIORITY_HIGH,
    TASK_PRIORITY_LOW,
    TASK_PRIORITY_MEDIUM,
    TASK_TYPE_ATTRIBUTE_ENRICHMENT,
    TASK_TYPE_COMMERCIAL_REVIEW,
    TASK_TYPE_COMPLIANCE_REVIEW,
    TASK_TYPE_CONTENT_IMPROVEMENT,
    TASK_TYPE_DATA_COMPLETION,
    TASK_TYPE_GENERAL_REVIEW,
    TASK_TYPE_MEDIA_IMPROVEMENT,
    TASK_TYPE_TRANSLATION,
    derive_review_status,
    is_allowed_review_status,
    is_ready_for_export,
    issue_to_task_type,
    needs_review,
    normalize_review_status,
    severity_to_task_priority,
)


def test_severity_to_task_priority():
    assert severity_to_task_priority("Critical") == TASK_PRIORITY_HIGH
    assert severity_to_task_priority("Warning") == TASK_PRIORITY_MEDIUM
    assert severity_to_task_priority("Info") == TASK_PRIORITY_LOW
    assert severity_to_task_priority("Unknown") == TASK_PRIORITY_LOW


def test_critical_issue_maps_to_data_completion_task():
    assert issue_to_task_type("Missing ean", "Critical") == TASK_TYPE_DATA_COMPLETION


def test_issue_to_task_type_maps_known_issue_types():
    assert issue_to_task_type("Missing manufacturer") == TASK_TYPE_DATA_COMPLETION
    assert issue_to_task_type("Missing price") == TASK_TYPE_COMMERCIAL_REVIEW
    assert issue_to_task_type("Invalid price") == TASK_TYPE_COMMERCIAL_REVIEW
    assert issue_to_task_type("Missing attributes") == TASK_TYPE_ATTRIBUTE_ENRICHMENT
    assert issue_to_task_type("Missing translation_de") == TASK_TYPE_TRANSLATION
    assert issue_to_task_type("Missing translation_en") == TASK_TYPE_TRANSLATION
    assert issue_to_task_type("Missing warning_notes") == TASK_TYPE_COMPLIANCE_REVIEW
    assert issue_to_task_type("Short product_name") == TASK_TYPE_CONTENT_IMPROVEMENT
    assert issue_to_task_type("Short description") == TASK_TYPE_CONTENT_IMPROVEMENT
    assert issue_to_task_type("Generic product_name") == TASK_TYPE_CONTENT_IMPROVEMENT
    assert issue_to_task_type("Missing image_url") == TASK_TYPE_MEDIA_IMPROVEMENT
    assert issue_to_task_type("Image URL suspicious") == TASK_TYPE_MEDIA_IMPROVEMENT


def test_unknown_issue_type_maps_to_general_review():
    assert issue_to_task_type("Unexpected issue") == TASK_TYPE_GENERAL_REVIEW


def test_review_status_validation_and_normalization():
    assert is_allowed_review_status(REVIEW_STATUS_OK)
    assert is_allowed_review_status(REVIEW_STATUS_READY_FOR_EXPORT)
    assert not is_allowed_review_status("Done")
    assert normalize_review_status(REVIEW_STATUS_OK) == REVIEW_STATUS_OK
    assert normalize_review_status("Done") == REVIEW_STATUS_NEEDS_REVIEW
    assert normalize_review_status(None) == REVIEW_STATUS_NEEDS_REVIEW


def test_ready_for_export_helpers():
    assert is_ready_for_export(REVIEW_STATUS_READY_FOR_EXPORT)
    assert not is_ready_for_export(REVIEW_STATUS_NEEDS_REVIEW)
    assert not is_ready_for_export("Done")
    assert not needs_review(REVIEW_STATUS_READY_FOR_EXPORT)
    assert needs_review(REVIEW_STATUS_NEEDS_REVIEW)


def test_derive_review_status_priority_order():
    assert (
        derive_review_status(
            ["Missing warning_notes", "Missing translation_de"],
            ["Critical", "Warning"],
            "Ready",
        )
        == REVIEW_STATUS_MISSING_DATA
    )
    assert (
        derive_review_status(
            ["Missing warning_notes", "Missing translation_de"],
            ["Warning"],
            "Ready",
        )
        == REVIEW_STATUS_COMPLIANCE_CHECK_REQUIRED
    )
    assert (
        derive_review_status(["Missing translation_en"], ["Warning"], "Ready")
        == REVIEW_STATUS_TRANSLATION_MISSING
    )
    assert derive_review_status([], [], "Ready") == REVIEW_STATUS_READY_FOR_EXPORT
    assert derive_review_status([], [], "Needs Review") == REVIEW_STATUS_NEEDS_REVIEW
