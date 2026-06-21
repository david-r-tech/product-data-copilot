import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.ai.suggestion_contract import (  # noqa: E402
    FORBIDDEN_UNSUPPORTED_FACT_CATEGORIES,
    REVIEW_REQUIRED_SOURCE_CONDITIONS,
    SMART_SUGGESTION_REQUIRED_KEYS,
    smart_suggestion_blocked_fact_categories,
    smart_suggestion_human_review_rules,
    smart_suggestion_json_contract,
    smart_suggestion_prompt_contract_block,
    smart_suggestion_review_required_conditions,
    smart_suggestion_safety_rules,
)


def test_contract_module_imports_and_contains_required_keys():
    assert "sku" in SMART_SUGGESTION_REQUIRED_KEYS
    assert "target_field" in SMART_SUGGESTION_REQUIRED_KEYS
    assert "source_fields" in SMART_SUGGESTION_REQUIRED_KEYS
    assert "reason" in SMART_SUGGESTION_REQUIRED_KEYS
    assert "confidence" in SMART_SUGGESTION_REQUIRED_KEYS
    assert "risk_level" in SMART_SUGGESTION_REQUIRED_KEYS
    assert "approval_status" in SMART_SUGGESTION_REQUIRED_KEYS
    assert "requires_human_approval" in SMART_SUGGESTION_REQUIRED_KEYS


def test_json_contract_returns_copy_of_required_keys():
    contract = smart_suggestion_json_contract()

    assert contract["root_key"] == "smart_suggestions"
    assert contract["item_type"] == "field_level_suggestion"
    assert contract["required_keys"] == SMART_SUGGESTION_REQUIRED_KEYS
    assert contract["confidence_values"] == ["low", "medium", "high"]
    assert contract["risk_level_values"] == ["low", "medium", "high"]
    assert "needs_review" in contract["approval_status_values"]
    assert "review_required" in contract["suggestion_status_values"]

    contract["required_keys"].append("extra")
    assert "extra" not in smart_suggestion_json_contract()["required_keys"]


def test_safety_rules_block_invented_facts_and_unverifiable_claims():
    rules = smart_suggestion_safety_rules()

    assert "Do not invent product facts" in rules
    assert "unverifiable EANs" in rules
    assert "prices" in rules
    assert "dimensions" in rules
    assert "certifications" in rules
    assert "compliance claims" in rules
    assert "Use only existing source fields" in rules
    assert "missing, weak, unknown, or contradictory" in rules
    assert "source_fields" in rules
    assert "reason" in rules
    assert "confidence" in rules
    assert "risk_level" in rules
    assert "Never claim legal compliance" in rules


def test_human_review_rules_require_approval_before_use_or_export():
    rules = smart_suggestion_human_review_rules()

    assert "draft recommendations" in rules
    assert "Human approval is required" in rules
    assert "before use or export" in rules
    assert "Do not auto-apply" in rules
    assert "needs_review" in rules
    assert "review_required" in rules
    assert "must not be treated as approved product data" in rules


def test_blocked_fact_categories_cover_unsafe_product_facts():
    categories = smart_suggestion_blocked_fact_categories()

    assert categories == FORBIDDEN_UNSUPPORTED_FACT_CATEGORIES
    assert "EANs or GTINs" in categories
    assert "prices" in categories
    assert "dimensions" in categories
    assert "certifications" in categories
    assert "compliance claims" in categories
    assert "unsupported translations" in categories

    categories.append("extra")
    assert "extra" not in smart_suggestion_blocked_fact_categories()


def test_review_required_conditions_cover_missing_or_contradictory_source_data():
    conditions = smart_suggestion_review_required_conditions()

    assert conditions == REVIEW_REQUIRED_SOURCE_CONDITIONS
    assert "source data is missing" in conditions
    assert "source data is weak" in conditions
    assert "source data is unknown" in conditions
    assert "source data is contradictory" in conditions
    assert any("price" in condition for condition in conditions)
    assert any("EAN" in condition for condition in conditions)

    conditions.append("extra")
    assert "extra" not in smart_suggestion_review_required_conditions()


def test_prompt_contract_block_is_deterministic_and_strict():
    first_contract = smart_suggestion_prompt_contract_block()
    second_contract = smart_suggestion_prompt_contract_block()

    assert first_contract == second_contract
    assert "Return only valid JSON" in first_contract
    assert "smart_suggestions array" in first_contract
    assert "field-level suggestion" in first_contract
    assert "sku" in first_contract
    assert "target_field" in first_contract
    assert "source_fields" in first_contract
    assert "reason" in first_contract
    assert "confidence" in first_contract
    assert "risk_level" in first_contract
    assert "requires_human_approval" in first_contract
    assert "AI-generated suggestions must not set approval_status to approved" in first_contract
    assert "Do not invent product facts" in first_contract
    assert "unsupported translations" in first_contract
    assert "source data is missing" in first_contract
    assert "source data is contradictory" in first_contract
    assert "Human approval is required before use or export" in first_contract


def test_contract_defaults_match_parser_safety_expectations():
    contract = smart_suggestion_json_contract()

    assert contract["root_key"] == "smart_suggestions"
    assert contract["approval_status_values"] == [
        "needs_review",
        "approved",
        "rejected",
    ]
    assert contract["suggestion_status_values"] == [
        "draft",
        "review_required",
        "blocked_insufficient_source",
    ]

    prompt_contract = smart_suggestion_prompt_contract_block()
    assert "AI-generated suggestions must not set approval_status to approved" in prompt_contract
    assert "blocked_insufficient_source" in prompt_contract
