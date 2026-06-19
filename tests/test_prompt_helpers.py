import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.ai.prompt_helpers import (  # noqa: E402
    ACTION_STATUS_APPROVED,
    ACTION_STATUS_DRAFT,
    ACTION_STATUS_NEEDS_REVIEW,
    ACTION_STATUS_REJECTED,
    AI_SUGGESTION_SCHEMA_FIELDS,
    CONFIDENCE_HIGH,
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    build_product_context_snippet,
    build_safe_prompt_instructions,
    do_not_invent_facts_instruction,
    human_review_instruction,
    is_valid_ai_action_status,
    is_valid_confidence_label,
    normalize_ai_action_status,
    normalize_confidence_label,
    normalize_prompt_value,
    should_include_prompt_field,
    structured_suggestion_schema_description,
)


def test_normalize_prompt_value_removes_empty_and_unknown_values():
    assert normalize_prompt_value(None) == ""
    assert normalize_prompt_value("  ") == ""
    assert normalize_prompt_value("unknown") == ""
    assert normalize_prompt_value("N/A") == ""
    assert normalize_prompt_value("-") == ""
    assert normalize_prompt_value("  Cotton shirt  ") == "Cotton shirt"


def test_should_include_prompt_field():
    assert should_include_prompt_field("Valid source value")
    assert not should_include_prompt_field("")
    assert not should_include_prompt_field("unknown")


def test_build_product_context_snippet_skips_empty_unknown_fields():
    product = {
        "sku": "SKU-001",
        "product_name": "Trail Backpack",
        "brand": "unknown",
        "description": "",
        "attributes": "volume: 20L; color: green",
        "extra": "not requested",
    }

    context = build_product_context_snippet(
        product,
        fields=["sku", "product_name", "brand", "description", "attributes"],
    )

    assert context == {
        "sku": "SKU-001",
        "product_name": "Trail Backpack",
        "attributes": "volume: 20L; color: green",
    }


def test_safety_instruction_contains_anti_hallucination_rules():
    instruction = do_not_invent_facts_instruction()

    assert "Do not invent facts" in instruction
    assert "provided source fields" in instruction
    assert "flag uncertainty" in instruction


def test_human_review_instruction_requires_review_before_use():
    instruction = human_review_instruction()

    assert "draft recommendations" in instruction
    assert "human reviewer" in instruction
    assert "approve, edit, or reject" in instruction


def test_structured_suggestion_schema_description():
    schema = structured_suggestion_schema_description()

    assert schema["fields"] == AI_SUGGESTION_SCHEMA_FIELDS
    assert schema["required"] == AI_SUGGESTION_SCHEMA_FIELDS
    assert schema["confidence_values"] == [
        CONFIDENCE_LOW,
        CONFIDENCE_MEDIUM,
        CONFIDENCE_HIGH,
    ]
    assert schema["action_status_values"] == [
        ACTION_STATUS_DRAFT,
        ACTION_STATUS_NEEDS_REVIEW,
        ACTION_STATUS_APPROVED,
        ACTION_STATUS_REJECTED,
    ]

    schema["fields"].append("extra")
    assert "extra" not in structured_suggestion_schema_description()["fields"]


def test_confidence_label_validation_and_normalization():
    assert is_valid_confidence_label("low")
    assert is_valid_confidence_label("MEDIUM")
    assert is_valid_confidence_label(" high ")
    assert not is_valid_confidence_label("certain")

    assert normalize_confidence_label("MEDIUM") == CONFIDENCE_MEDIUM
    assert normalize_confidence_label("certain") == CONFIDENCE_LOW
    assert normalize_confidence_label(None) == CONFIDENCE_LOW


def test_ai_action_status_validation_and_normalization():
    assert is_valid_ai_action_status("draft")
    assert is_valid_ai_action_status("APPROVED")
    assert is_valid_ai_action_status(" rejected ")
    assert not is_valid_ai_action_status("published")

    assert normalize_ai_action_status("NEEDS_REVIEW") == ACTION_STATUS_NEEDS_REVIEW
    assert normalize_ai_action_status("published") == ACTION_STATUS_DRAFT
    assert normalize_ai_action_status(None) == ACTION_STATUS_DRAFT


def test_build_safe_prompt_instructions_combines_core_safety_rules():
    instructions = build_safe_prompt_instructions()

    assert "Do not invent facts" in instructions
    assert "draft recommendations" in instructions
    assert "Do not claim legal compliance" in instructions
    assert "confidence value" in instructions
