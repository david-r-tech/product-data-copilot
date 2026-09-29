"""Focused regression tests for the extracted product-scoring pipeline."""

import inspect

import pandas as pd
import pytest

import app
from product_data_copilot.data.product_input import ProductInputError
from product_data_copilot.rules.product_checks import find_product_issues
from product_data_copilot.scoring import product_scoring


def test_app_uses_extracted_product_scoring_pipeline():
    assert app.calculate_product_scores is product_scoring.calculate_product_scores
    assert app.calculate_readiness_scores is product_scoring.calculate_readiness_scores
    assert app.get_review_status is product_scoring.get_review_status
    app_source = inspect.getsource(app)
    assert "def calculate_product_scores" not in app_source
    assert "def calculate_readiness_scores" not in app_source
    assert "def get_review_status" not in app_source


def test_existing_complete_product_scores_remain_unchanged(valid_product):
    assert product_scoring.calculate_product_scores(pd.Series(valid_product)) == {
        "data_quality_score": 100,
        "marketplace_readiness_score": 100,
        "translation_readiness_score": 100,
        "compliance_readiness_score": 100,
        "ai_content_readiness_score": 100,
        "overall_readiness_score": 100,
    }


def test_weighted_score_and_component_rounding_remain_unchanged(valid_product):
    product = {
        **valid_product,
        "description": "x",
        "brand": "",
        "manufacturer": "",
        "ean": "",
        "image_url": "",
        "category": "Toys",
        "price": "0",
        "attributes": "",
        "translation_de": "",
        "translation_en": "",
        "warning_notes": "",
    }

    assert product_scoring.calculate_product_scores(pd.Series(product)) == {
        "data_quality_score": 57,
        "marketplace_readiness_score": 38,
        "translation_readiness_score": 0,
        "compliance_readiness_score": 0,
        "ai_content_readiness_score": 33,
        "overall_readiness_score": 33,
    }


def test_readiness_and_review_statuses_remain_unchanged(valid_product):
    products = pd.DataFrame([valid_product])
    no_issues = find_product_issues(products)
    ready = product_scoring.calculate_readiness_scores(products, no_issues).iloc[0]
    assert ready["readiness_status"] == "Ready"
    assert ready["review_status"] == "Ready for Export"

    warning_issues = pd.DataFrame([
        {"sku": valid_product["sku"], "issue_type": "Short description", "severity": "Warning"},
    ])
    needs_review = product_scoring.calculate_readiness_scores(products, warning_issues).iloc[0]
    assert needs_review["overall_readiness_score"] == 100
    assert needs_review["readiness_status"] == "Needs Review"
    assert needs_review["review_status"] == "Needs Review"

    critical_issues = pd.DataFrame([
        {"sku": valid_product["sku"], "issue_type": "Missing ean", "severity": "Critical"},
    ])
    critical = product_scoring.calculate_readiness_scores(products, critical_issues).iloc[0]
    assert critical["overall_readiness_score"] == 100
    assert critical["readiness_status"] == "Critical"
    assert critical["review_status"] == "Missing Data"


def test_missing_optional_columns_keep_existing_defaults():
    product = pd.Series({"sku": "A-1", "product_name": "Product name"})
    assert product_scoring.calculate_product_scores(product) == {
        "data_quality_score": 29,
        "marketplace_readiness_score": 12,
        "translation_readiness_score": 0,
        "compliance_readiness_score": 100,
        "ai_content_readiness_score": 17,
        "overall_readiness_score": 30,
    }


@pytest.mark.parametrize("products", [
    pd.DataFrame([
        {"sku": "DUPLICATE", "product_name": "First"},
        {"sku": "DUPLICATE", "product_name": "Second"},
    ]),
    pd.DataFrame([{"sku": " ", "product_name": "Blank identity"}]),
])
def test_readiness_pipeline_rejects_ambiguous_product_identity(products):
    issues = pd.DataFrame(columns=["sku", "issue_type", "severity"])

    with pytest.raises(ProductInputError):
        product_scoring.calculate_readiness_scores(products, issues)
