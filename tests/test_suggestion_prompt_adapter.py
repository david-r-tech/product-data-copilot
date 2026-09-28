import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.ai.suggestion_prompt_adapter import (  # noqa: E402
    build_batch_prompt_context,
    build_issue_context_lines,
    build_product_context_lines,
    build_review_task_context_lines,
    build_smart_suggestion_prompt,
    normalize_prompt_value,
)
from product_data_copilot.ai.suggestion_contract import (  # noqa: E402
    SMART_SUGGESTION_REQUIRED_KEYS,
)


def test_prompt_adapter_module_imports_and_normalizes_prompt_values():
    assert normalize_prompt_value(None) == ""
    assert normalize_prompt_value("") == ""
    assert normalize_prompt_value(" unknown ") == ""
    assert normalize_prompt_value("N/A") == ""
    assert normalize_prompt_value("-") == ""
    assert normalize_prompt_value("  Product title  ") == "Product title"


def test_product_context_lines_skip_blank_unknown_values_and_preserve_field_names():
    product = {
        "sku": "SKU-001",
        "product_name": "Trail Backpack",
        "brand": "unknown",
        "manufacturer": None,
        "attributes": "volume: 20L",
        "description": "",
        "ean": "-",
    }

    lines = build_product_context_lines(
        product,
        allowed_fields=["sku", "product_name", "brand", "attributes", "ean"],
    )

    assert lines == [
        "sku: SKU-001",
        "product_name: Trail Backpack",
        "attributes: volume: 20L",
    ]


def test_issue_context_lines_include_traceable_issue_fields():
    issues = [
        {
            "sku": "SKU-001",
            "issue_type": "Missing description",
            "field_name": "description",
            "severity": "Critical",
            "message": "Product description is missing.",
            "recommended_action": "Add a product description.",
            "ignored": "not included",
        }
    ]

    lines = build_issue_context_lines(issues)

    assert lines == [
        "1. sku: SKU-001; issue_type: Missing description; field_name: description; severity: Critical; message: Product description is missing.; recommended_action: Add a product description."
    ]


def test_review_task_context_lines_include_priority_and_status():
    tasks = [
        {
            "sku": "SKU-001",
            "product_name": "Trail Backpack",
            "issue_type": "Missing translation",
            "field_name": "translation_de",
            "task_type": "Translation",
            "priority": "Medium",
            "recommended_action": "Add German translation.",
            "review_status": "Translation Missing",
        }
    ]

    lines = build_review_task_context_lines(tasks)

    assert "task_type: Translation" in lines[0]
    assert "priority: Medium" in lines[0]
    assert "review_status: Translation Missing" in lines[0]


def test_smart_suggestion_prompt_output_is_deterministic_and_contains_contract():
    product = {
        "sku": "SKU-002",
        "product_name": "Desk Lamp",
        "category": "Office",
        "attributes": "color: black; power: USB",
    }
    issues = [
        {
            "sku": "SKU-002",
            "issue_type": "Short description",
            "field_name": "description",
            "severity": "Warning",
            "message": "Description is too short.",
            "recommended_action": "Add a clearer description.",
        }
    ]
    tasks = [
        {
            "sku": "SKU-002",
            "product_name": "Desk Lamp",
            "issue_type": "Short description",
            "field_name": "description",
            "task_type": "Content Improvement",
            "priority": "Medium",
            "recommended_action": "Improve content.",
            "review_status": "Needs Review",
        }
    ]

    first_prompt = build_smart_suggestion_prompt(product, issues, tasks)
    second_prompt = build_smart_suggestion_prompt(product, issues, tasks)

    assert first_prompt == second_prompt
    assert "Reviewable AI Suggestions output contract" in first_prompt
    assert "smart_suggestions array" in first_prompt
    assert "field-level suggestion" in first_prompt
    for required_key in SMART_SUGGESTION_REQUIRED_KEYS:
        assert required_key in first_prompt


def test_smart_suggestion_prompt_contains_safety_and_human_review_rules():
    prompt = build_smart_suggestion_prompt(
        {"sku": "SKU-003", "product_name": "Toy Set"},
        issue_records=[],
        review_task_records=[],
    )

    assert "Do not invent product facts" in prompt
    assert "Use only existing source fields" in prompt
    assert "Human approval is required before use or export" in prompt
    assert "Do not auto-apply suggestions to product data" in prompt
    assert "source data is missing, weak, unknown, or contradictory" in prompt
    assert "review_required" in prompt


def test_smart_suggestion_prompt_blocks_unsupported_fact_categories():
    prompt = build_smart_suggestion_prompt({"sku": "SKU-004"})

    assert "EANs or GTINs" in prompt
    assert "prices" in prompt
    assert "dimensions" in prompt
    assert "certifications" in prompt
    assert "compliance claims" in prompt
    assert "unsupported translations" in prompt
    assert "AI-generated suggestions must not set approval_status to approved" in prompt


def test_prompt_uses_empty_state_when_context_has_no_usable_values():
    prompt = build_smart_suggestion_prompt(
        {"sku": "", "product_name": ""},
        issue_records=[],
        review_task_records=[],
    )

    assert "- No usable source data provided." in prompt


def test_batch_prompt_context_respects_max_products_and_truncates_safely():
    products = [
        {"sku": "SKU-001", "product_name": "Product 1"},
        {"sku": "SKU-002", "product_name": "Product 2"},
        {"sku": "SKU-003", "product_name": "Product 3"},
    ]

    lines = build_batch_prompt_context(products, max_products=2)

    assert lines == [
        "1. sku: SKU-001; product_name: Product 1",
        "2. sku: SKU-002; product_name: Product 2",
        "... 1 additional product(s) omitted.",
    ]


def test_batch_prompt_context_handles_empty_and_zero_limit_safely():
    assert build_batch_prompt_context([], max_products=5) == []
    assert build_batch_prompt_context(None, max_products=5) == []
    assert build_batch_prompt_context([{"sku": "SKU-001"}], max_products=0) == []
