import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.ai.suggestion_contract import (  # noqa: E402
    SMART_SUGGESTION_REQUIRED_KEYS,
    smart_suggestion_human_review_rules,
    smart_suggestion_json_contract,
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


def test_human_review_rules_require_approval_before_use_or_export():
    rules = smart_suggestion_human_review_rules()

    assert "draft recommendations" in rules
    assert "Human approval is required" in rules
    assert "before use or export" in rules
    assert "Do not auto-apply" in rules
    assert "needs_review" in rules
    assert "review_required" in rules
    assert "must not be treated as approved product data" in rules
