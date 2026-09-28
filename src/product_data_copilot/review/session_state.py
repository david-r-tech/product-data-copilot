"""Explicit lifetimes for dataset decisions and individual AI responses."""

import hashlib
import json

DATASET_STATE_PREFIXES = ("manual_", "ai_", "smart_suggestions_v2_", "batch_ai_", "content_")


def bind_dataset(state, fingerprint):
    """Clear dataset-dependent state when the complete input changes or fails."""
    changed = fingerprint is None or state.get("dataset_fingerprint") != fingerprint
    if changed:
        for key in list(state):
            if str(key).startswith(DATASET_STATE_PREFIXES):
                del state[key]
        state["dataset_fingerprint"] = fingerprint
    return changed


def suggestion_review_key(suggestion):
    """Include the evidence reviewed by the user, not just the proposed text."""
    fields = (
        "sku", "product_name", "target_field", "current_value", "proposed_value",
        "source_fields", "reason", "confidence", "risk_level", "suggestion_status",
    )
    payload = {field: suggestion.get(field, "") for field in fields}
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    ).hexdigest()


def replace_smart_response(state, *, sku, prompt, raw_response, result):
    """Every response replaces its predecessor and starts a fresh review."""
    state["smart_suggestions_v2_sku"] = sku
    state["smart_suggestions_v2_prompt"] = prompt
    state["smart_suggestions_v2_raw_response"] = raw_response
    state["smart_suggestions_v2_records"] = result["suggestions"]
    state["smart_suggestions_v2_error"] = result["errors"]
    state["smart_suggestions_v2_is_valid_json"] = result["is_valid_json"]
    state["smart_suggestions_v2_review_decisions"] = {}
    state.pop("smart_suggestions_v2_review_row", None)
