import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.ai.suggestion_schema import (  # noqa: E402
    ALLOWED_APPROVAL_STATUSES,
    ALLOWED_CONFIDENCE_LABELS,
    ALLOWED_RISK_LEVELS,
    ALLOWED_SUGGESTION_STATUSES,
    APPROVAL_STATUS_APPROVED,
    APPROVAL_STATUS_NEEDS_REVIEW,
    CONFIDENCE_HIGH,
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    DEFAULT_APPROVAL_STATUS,
    DEFAULT_CONFIDENCE_LABEL,
    DEFAULT_RISK_LEVEL,
    DEFAULT_SUGGESTION_STATUS,
    REQUIRED_SUGGESTION_FIELDS,
    RISK_LEVEL_HIGH,
    RISK_LEVEL_LOW,
    RISK_LEVEL_MEDIUM,
    SUGGESTION_STATUS_REVIEW_REQUIRED,
    UNSUPPORTED_FACT_TARGET_FIELDS,
    create_review_required_suggestion,
    has_required_source_and_reason,
    is_unsupported_fact_target_field,
    normalize_approval_status,
    normalize_confidence,
    normalize_risk_level,
    normalize_source_fields,
    normalize_suggestion_record,
    normalize_suggestion_status,
    validate_suggestion_record,
)


def test_schema_module_imports_and_exposes_expected_constants():
    assert ALLOWED_CONFIDENCE_LABELS == [
        CONFIDENCE_LOW,
        CONFIDENCE_MEDIUM,
        CONFIDENCE_HIGH,
    ]
    assert ALLOWED_RISK_LEVELS == [
        RISK_LEVEL_LOW,
        RISK_LEVEL_MEDIUM,
        RISK_LEVEL_HIGH,
    ]
    assert APPROVAL_STATUS_NEEDS_REVIEW in ALLOWED_APPROVAL_STATUSES
    assert SUGGESTION_STATUS_REVIEW_REQUIRED in ALLOWED_SUGGESTION_STATUSES
    assert "target_field" in REQUIRED_SUGGESTION_FIELDS
    assert "requires_human_approval" in REQUIRED_SUGGESTION_FIELDS
    assert "ean" in UNSUPPORTED_FACT_TARGET_FIELDS
    assert "price" in UNSUPPORTED_FACT_TARGET_FIELDS
    assert "compliance_claims" in UNSUPPORTED_FACT_TARGET_FIELDS


def test_unknown_confidence_normalizes_to_cautious_low_value():
    assert normalize_confidence("HIGH") == CONFIDENCE_HIGH
    assert normalize_confidence(" medium ") == CONFIDENCE_MEDIUM
    assert normalize_confidence("certain") == DEFAULT_CONFIDENCE_LABEL
    assert normalize_confidence(None) == DEFAULT_CONFIDENCE_LABEL


def test_unknown_risk_normalizes_to_cautious_high_value():
    assert normalize_risk_level("LOW") == RISK_LEVEL_LOW
    assert normalize_risk_level("medium") == RISK_LEVEL_MEDIUM
    assert normalize_risk_level("safe") == DEFAULT_RISK_LEVEL
    assert normalize_risk_level(None) == DEFAULT_RISK_LEVEL


def test_missing_status_values_default_to_review_required():
    assert normalize_approval_status("approved") == APPROVAL_STATUS_APPROVED
    assert normalize_approval_status("published") == DEFAULT_APPROVAL_STATUS
    assert normalize_approval_status(None) == DEFAULT_APPROVAL_STATUS
    assert normalize_suggestion_status("draft") == "draft"
    assert normalize_suggestion_status("published") == DEFAULT_SUGGESTION_STATUS
    assert normalize_suggestion_status(None) == DEFAULT_SUGGESTION_STATUS


def test_source_fields_normalize_from_string_list_and_empty_values():
    assert normalize_source_fields("product_name, description, unknown, -") == [
        "product_name",
        "description",
    ]
    assert normalize_source_fields(["brand", "brand", "attributes", ""]) == [
        "brand",
        "attributes",
    ]
    assert normalize_source_fields(None) == []
    assert normalize_source_fields("-") == []
    assert normalize_source_fields(12345) == []
    assert normalize_source_fields({"field": "description"}) == []


def test_unsupported_fact_target_fields_are_detected_cautiously():
    assert is_unsupported_fact_target_field("EAN")
    assert is_unsupported_fact_target_field(" price ")
    assert is_unsupported_fact_target_field("certifications")
    assert is_unsupported_fact_target_field("compliance_claim")
    assert is_unsupported_fact_target_field("dimensions")
    assert not is_unsupported_fact_target_field("description")
    assert not is_unsupported_fact_target_field("product_name")


def test_records_missing_source_fields_or_reason_are_not_valid():
    base_record = {
        "sku": "SKU-001",
        "product_name": "Trail Backpack",
        "target_field": "description",
        "current_value": "",
        "proposed_value": "Draft description based on source fields.",
        "source_fields": ["product_name", "attributes"],
        "reason": "Uses existing product name and attributes.",
        "confidence": "medium",
        "risk_level": "low",
        "requires_human_approval": True,
        "approval_status": "needs_review",
        "suggestion_status": "review_required",
    }

    assert has_required_source_and_reason(base_record)
    assert validate_suggestion_record(base_record)

    missing_source = base_record | {"source_fields": []}
    missing_reason = base_record | {"reason": ""}

    assert not has_required_source_and_reason(missing_source)
    assert not validate_suggestion_record(missing_source)
    assert not has_required_source_and_reason(missing_reason)
    assert not validate_suggestion_record(missing_reason)


def test_created_review_required_suggestion_requires_human_approval_by_default():
    suggestion = create_review_required_suggestion(
        sku="SKU-002",
        product_name="Desk Lamp",
        target_field="description",
        current_value="Short text",
        proposed_value="Draft description based on source data.",
        source_fields="product_name, attributes",
        reason="Uses only existing source fields.",
        confidence="high",
        risk_level="low",
    )

    assert suggestion["requires_human_approval"] is True
    assert suggestion["approval_status"] == APPROVAL_STATUS_NEEDS_REVIEW
    assert suggestion["suggestion_status"] == SUGGESTION_STATUS_REVIEW_REQUIRED
    assert suggestion["approval_status"] != APPROVAL_STATUS_APPROVED
    assert suggestion["source_fields"] == ["product_name", "attributes"]
    assert validate_suggestion_record(suggestion)


def test_normalized_record_forces_human_approval_and_cautious_defaults():
    record = normalize_suggestion_record(
        {
            "sku": "SKU-003",
            "product_name": "Headphones",
            "target_field": "product_name",
            "source_fields": "brand, category",
            "reason": "Can improve wording using existing fields.",
            "confidence": "unknown",
            "risk_level": "unknown",
            "requires_human_approval": False,
            "approval_status": "auto_approved",
            "suggestion_status": "published",
        }
    )

    assert record["requires_human_approval"] is True
    assert record["confidence"] == CONFIDENCE_LOW
    assert record["risk_level"] == RISK_LEVEL_HIGH
    assert record["approval_status"] == APPROVAL_STATUS_NEEDS_REVIEW
    assert record["suggestion_status"] == SUGGESTION_STATUS_REVIEW_REQUIRED
