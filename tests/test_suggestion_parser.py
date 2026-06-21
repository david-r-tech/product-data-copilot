import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.ai.suggestion_parser import (  # noqa: E402
    build_parser_error_record,
    extract_suggestion_records,
    normalize_suggestion_record,
    normalize_suggestion_records,
    parse_and_normalize_suggestions,
    parse_json_response,
)
from product_data_copilot.ai.suggestion_schema import (  # noqa: E402
    APPROVAL_STATUS_NEEDS_REVIEW,
    CONFIDENCE_LOW,
    RISK_LEVEL_HIGH,
    SUGGESTION_STATUS_BLOCKED,
    SUGGESTION_STATUS_REVIEW_REQUIRED,
    validate_suggestion_record,
)


def test_parser_module_imports_safely_and_parses_valid_json():
    parsed = parse_json_response('{"smart_suggestions": []}')

    assert parsed["payload"] == {"smart_suggestions": []}
    assert parsed["error"] == ""


def test_valid_json_list_parses_into_normalized_records():
    raw_response = json.dumps(
        [
            {
                "sku": "SKU-001",
                "product_name": "Trail Backpack",
                "target_field": "description",
                "current_value": "Short text",
                "proposed_value": "Draft description based on existing fields.",
                "source_fields": ["product_name", "attributes"],
                "reason": "Uses product name and attributes only.",
                "confidence": "medium",
                "risk_level": "low",
                "approval_status": "needs_review",
                "suggestion_status": "draft",
            }
        ]
    )

    result = parse_and_normalize_suggestions(raw_response)

    assert result["is_valid_json"] is True
    assert result["errors"] == []
    assert len(result["suggestions"]) == 1
    suggestion = result["suggestions"][0]
    assert suggestion["sku"] == "SKU-001"
    assert suggestion["target_field"] == "description"
    assert suggestion["current_value"] == "Short text"
    assert suggestion["proposed_value"] == "Draft description based on existing fields."
    assert suggestion["source_fields"] == ["product_name", "attributes"]
    assert suggestion["suggestion_status"] == SUGGESTION_STATUS_REVIEW_REQUIRED
    assert validate_suggestion_record(suggestion)


def test_valid_json_object_with_suggestions_key_parses_into_records():
    payload = {
        "smart_suggestions": [
            {
                "sku": "SKU-002",
                "product_name": "Desk Lamp",
                "target_field": "product_name",
                "current_value": "Lamp",
                "proposed_value": "Desk Lamp",
                "source_fields": "product_name, category",
                "reason": "Clarifies the product type using source fields.",
                "confidence": "high",
                "risk_level": "low",
            }
        ]
    }

    result = parse_and_normalize_suggestions(json.dumps(payload))

    assert len(result["suggestions"]) == 1
    assert result["suggestions"][0]["source_fields"] == [
        "product_name",
        "category",
    ]
    assert result["suggestions"][0]["approval_status"] == APPROVAL_STATUS_NEEDS_REVIEW


def test_single_suggestion_dict_payload_is_handled_safely():
    payload = {
        "sku": "SKU-003",
        "product_name": "Headphones",
        "field_name": "product_name",
        "current_value": "Headphones",
        "suggested_value": "Wireless Headphones",
        "source_fields": ["product_name", "attributes"],
        "reason": "Uses existing title and attributes.",
        "confidence": "medium",
        "risk_level": "medium",
    }

    records = extract_suggestion_records(payload)
    normalized = normalize_suggestion_records(records)

    assert len(normalized) == 1
    assert normalized[0]["target_field"] == "product_name"
    assert normalized[0]["proposed_value"] == "Wireless Headphones"
    assert normalized[0]["approval_status"] == APPROVAL_STATUS_NEEDS_REVIEW


def test_invalid_json_returns_safe_error_result_without_crashing():
    result = parse_and_normalize_suggestions("{not valid json")

    assert result["is_valid_json"] is False
    assert result["suggestions"] == []
    assert len(result["errors"]) == 1
    error_record = result["errors"][0]
    assert error_record["target_field"] == "_parser_error"
    assert error_record["approval_status"] == APPROVAL_STATUS_NEEDS_REVIEW
    assert error_record["suggestion_status"] == SUGGESTION_STATUS_BLOCKED
    assert error_record["risk_level"] == RISK_LEVEL_HIGH


def test_empty_and_null_responses_return_safe_empty_results():
    assert parse_and_normalize_suggestions("") == {
        "suggestions": [],
        "errors": [],
        "is_valid_json": True,
    }
    assert parse_and_normalize_suggestions(None) == {
        "suggestions": [],
        "errors": [],
        "is_valid_json": True,
    }
    assert parse_and_normalize_suggestions("null") == {
        "suggestions": [],
        "errors": [],
        "is_valid_json": True,
    }


def test_missing_required_fields_do_not_become_use_ready():
    suggestion = normalize_suggestion_record(
        {
            "sku": "SKU-004",
            "target_field": "description",
            "proposed_value": "Draft text.",
            "confidence": "high",
            "risk_level": "low",
        }
    )

    assert suggestion["suggestion_status"] == SUGGESTION_STATUS_BLOCKED
    assert suggestion["approval_status"] == APPROVAL_STATUS_NEEDS_REVIEW
    assert not validate_suggestion_record(suggestion)


def test_unknown_confidence_risk_and_status_normalize_cautiously():
    suggestion = normalize_suggestion_record(
        {
            "sku": "SKU-005",
            "target_field": "description",
            "source_fields": ["product_name"],
            "reason": "Uses source product title.",
            "confidence": "certain",
            "risk_level": "safe",
            "approval_status": "auto_approved",
            "suggestion_status": "published",
        }
    )

    assert suggestion["confidence"] == CONFIDENCE_LOW
    assert suggestion["risk_level"] == RISK_LEVEL_HIGH
    assert suggestion["approval_status"] == APPROVAL_STATUS_NEEDS_REVIEW
    assert suggestion["suggestion_status"] == SUGGESTION_STATUS_REVIEW_REQUIRED


def test_parser_never_preserves_ai_supplied_approved_status():
    suggestion = normalize_suggestion_record(
        {
            "sku": "SKU-006",
            "target_field": "description",
            "source_fields": ["product_name"],
            "reason": "Uses source product title.",
            "approval_status": "approved",
            "suggestion_status": "draft",
        }
    )

    assert suggestion["approval_status"] == APPROVAL_STATUS_NEEDS_REVIEW
    assert suggestion["requires_human_approval"] is True


def test_parser_requires_source_fields_and_reason_for_valid_suggestions():
    missing_source = normalize_suggestion_record(
        {
            "sku": "SKU-007",
            "target_field": "description",
            "reason": "Has a reason but no source.",
        }
    )
    missing_reason = normalize_suggestion_record(
        {
            "sku": "SKU-008",
            "target_field": "description",
            "source_fields": ["product_name"],
        }
    )

    assert missing_source["suggestion_status"] == SUGGESTION_STATUS_BLOCKED
    assert missing_reason["suggestion_status"] == SUGGESTION_STATUS_BLOCKED
    assert not validate_suggestion_record(missing_source)
    assert not validate_suggestion_record(missing_reason)


def test_build_parser_error_record_is_non_approved_and_review_required():
    error_record = build_parser_error_record("not json", "Invalid JSON")

    assert error_record["raw_response"] == "not json"
    assert error_record["reason"] == "Invalid JSON"
    assert error_record["requires_human_approval"] is True
    assert error_record["approval_status"] == APPROVAL_STATUS_NEEDS_REVIEW
    assert error_record["suggestion_status"] == SUGGESTION_STATUS_BLOCKED
