"""Pure parser helpers for future Smart Suggestions AI responses."""

import json

from product_data_copilot.ai.suggestion_schema import (
    APPROVAL_STATUS_APPROVED,
    DEFAULT_APPROVAL_STATUS,
    RISK_LEVEL_HIGH,
    SUGGESTION_STATUS_BLOCKED,
    SUGGESTION_STATUS_REVIEW_REQUIRED,
    normalize_suggestion_record as normalize_schema_suggestion_record,
    normalize_text,
    validate_suggestion_record,
)

SUGGESTION_ROOT_KEYS = [
    "smart_suggestions",
    "suggestions",
    "records",
    "items",
]


def parse_json_response(raw_response):
    """Parse a raw AI response into JSON without raising parser exceptions."""
    if raw_response is None:
        return {"payload": None, "error": ""}

    response_text = str(raw_response).strip()
    if response_text == "":
        return {"payload": None, "error": ""}

    try:
        return {"payload": json.loads(response_text), "error": ""}
    except json.JSONDecodeError as error:
        return {
            "payload": None,
            "error": f"Invalid JSON response: {error.msg}",
        }


def looks_like_suggestion_record(value):
    """Return True when a dictionary resembles one field-level suggestion."""
    if not isinstance(value, dict):
        return False

    suggestion_markers = {
        "sku",
        "target_field",
        "field_name",
        "source_fields",
        "reason",
        "proposed_value",
        "suggested_value",
    }
    return any(marker in value for marker in suggestion_markers)


def extract_suggestion_records(parsed_payload):
    """Extract raw suggestion dictionaries from safe payload shapes."""
    if parsed_payload is None:
        return []

    if isinstance(parsed_payload, list):
        return [record for record in parsed_payload if isinstance(record, dict)]

    if not isinstance(parsed_payload, dict):
        return []

    for root_key in SUGGESTION_ROOT_KEYS:
        root_value = parsed_payload.get(root_key)
        if isinstance(root_value, list):
            return [record for record in root_value if isinstance(record, dict)]
        if isinstance(root_value, dict):
            return [root_value]

    if looks_like_suggestion_record(parsed_payload):
        return [parsed_payload]

    return []


def normalize_suggestion_record(record):
    """Normalize one parsed suggestion and keep it review-required by default."""
    normalized = normalize_schema_suggestion_record(_map_legacy_field_names(record))

    if normalized["approval_status"] == APPROVAL_STATUS_APPROVED:
        normalized["approval_status"] = DEFAULT_APPROVAL_STATUS

    if not validate_suggestion_record(normalized):
        normalized["suggestion_status"] = SUGGESTION_STATUS_BLOCKED
    elif normalized["suggestion_status"] == "draft":
        normalized["suggestion_status"] = SUGGESTION_STATUS_REVIEW_REQUIRED

    return normalized


def normalize_suggestion_records(records):
    """Normalize a list of raw suggestion records."""
    return [
        normalize_suggestion_record(record)
        for record in records
        if isinstance(record, dict)
    ]


def parse_and_normalize_suggestions(raw_response):
    """Parse a raw AI response and return safe normalized suggestions."""
    parsed = parse_json_response(raw_response)
    if parsed["error"]:
        return {
            "suggestions": [],
            "errors": [
                build_parser_error_record(raw_response, parsed["error"]),
            ],
            "is_valid_json": False,
        }

    raw_records = extract_suggestion_records(parsed["payload"])
    return {
        "suggestions": normalize_suggestion_records(raw_records),
        "errors": [],
        "is_valid_json": True,
    }


def build_parser_error_record(raw_response, error_message):
    """Return a safe, non-approved record describing a parser failure."""
    return {
        "sku": "",
        "product_name": "",
        "target_field": "_parser_error",
        "current_value": "",
        "proposed_value": "",
        "source_fields": [],
        "reason": normalize_text(error_message),
        "confidence": "low",
        "risk_level": RISK_LEVEL_HIGH,
        "requires_human_approval": True,
        "approval_status": DEFAULT_APPROVAL_STATUS,
        "suggestion_status": SUGGESTION_STATUS_BLOCKED,
        "raw_response": str(raw_response) if raw_response is not None else "",
    }


def _map_legacy_field_names(record):
    """Map likely AI response aliases into the canonical schema fields."""
    mapped = dict(record)

    if "target_field" not in mapped and "field_name" in mapped:
        mapped["target_field"] = mapped["field_name"]

    if "proposed_value" not in mapped and "suggested_value" in mapped:
        mapped["proposed_value"] = mapped["suggested_value"]

    if "approval_status" not in mapped and "action_status" in mapped:
        mapped["approval_status"] = mapped["action_status"]

    return mapped
