import math

import pandas as pd
import pytest

from product_data_copilot.ai.content_generation import build_content_prompt
from product_data_copilot.ai.source_validation import validate_suggestions_against_product
from product_data_copilot.ai.suggestion_prompt_adapter import normalize_prompt_value
from product_data_copilot.ai.suggestion_schema import normalize_text


def candidate(product):
    return {
        "sku": product["sku"], "product_name": product["product_name"], "target_field": "description",
        "current_value": product["description"], "proposed_value": "Blue storage box for office supplies.",
        "source_fields": ["description", "attributes"], "reason": "Shortens the supplied description.",
        "confidence": "medium", "risk_level": "low", "approval_status": "approved",
        "suggestion_status": "review_required",
    }


def test_valid_sources_still_require_human_approval(valid_product):
    record = candidate(valid_product)
    result = validate_suggestions_against_product([record], valid_product)[0]
    assert result["approval_status"] == "needs_review"
    assert result["suggestion_status"] == "review_required"
    assert record["approval_status"] == "approved"


def test_identifier_na_and_literal_current_value_survive_ai_context(valid_product):
    valid_product["sku"] = "NA"
    valid_product["description"] = "unknown"
    record = candidate(valid_product)
    record["source_fields"] = ["attributes", "product_name"]
    result = validate_suggestions_against_product([record], valid_product)[0]
    assert result["sku"] == "NA"
    assert result["current_value"] == "unknown"
    assert result["suggestion_status"] == "review_required"
    prompt = build_content_prompt(pd.Series(valid_product), "create", "en")
    assert 'sku: "NA"' in prompt


@pytest.mark.parametrize("override", [
    {"sku": "WRONG"}, {"target_field": "nonsense_field"}, {"target_field": "price"},
    {"current_value": "invented original"}, {"source_fields": ["nonexistent"]},
    {"source_fields": ["warning_notes"]}, {"source_fields": []}, {"reason": ""}, {"proposed_value": ""},
])
def test_unusable_or_mismatched_suggestions_are_blocked(valid_product, override):
    result = validate_suggestions_against_product([{**candidate(valid_product), **override}], valid_product)[0]
    assert result["suggestion_status"] == "blocked_insufficient_source"
    assert result["risk_level"] == "high"
    assert "Blocked:" in result["reason"]


def test_existing_parser_block_is_not_removed(valid_product):
    result = validate_suggestions_against_product([
        {**candidate(valid_product), "suggestion_status": "blocked_insufficient_source"},
    ], valid_product)[0]
    assert result["suggestion_status"] == "blocked_insufficient_source"


def test_content_prompt_uses_relevant_source_context(valid_product):
    valid_product["warning_notes"] = "Use existing warning text."
    prompt = build_content_prompt(pd.Series(valid_product), "create", "en")
    for field in ["translation_de", "warning_notes"]:
        assert valid_product[field] in prompt
    assert valid_product["ean"] not in prompt
    assert valid_product["image_url"] not in prompt


@pytest.mark.parametrize("value", [None, math.nan, pd.NA])
def test_missing_values_are_not_promoted_to_source_text(value):
    assert normalize_prompt_value(value) == ""
    assert normalize_text(value) == ""
