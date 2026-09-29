"""Focused regression tests for the extracted product-check pipeline."""

import inspect

import pandas as pd

import app
from product_data_copilot.rules import product_checks


def test_app_uses_extracted_product_check_pipeline():
    assert app.find_product_issues is product_checks.find_product_issues
    assert app.prioritize_issues is product_checks.prioritize_issues
    app_source = inspect.getsource(app)
    assert "def find_product_issues" not in app_source
    assert "def add_core_data_checks" not in app_source
    assert "def add_attribute_consistency_checks" not in app_source


def test_valid_product_and_empty_optional_warning_stay_issue_free(valid_product):
    issues = product_checks.find_product_issues(pd.DataFrame([valid_product]))
    assert issues.empty
    assert issues.columns.tolist() == [
        "sku", "issue_type", "field_name", "severity", "message", "recommended_action",
    ]


def test_multiple_existing_issues_and_priority_order_are_preserved(valid_product):
    product = {
        **valid_product,
        "product_name": "Product",
        "description": "",
        "brand": "",
        "ean": "123",
        "category": "Toys",
        "manufacturer": "",
        "price": "0",
        "attributes": "",
        "translation_de": "",
        "translation_en": "",
        "warning_notes": "",
        "image_url": "ftp://internal/image.png",
    }

    issues = product_checks.prioritize_issues(
        product_checks.find_product_issues(pd.DataFrame([product]))
    )

    assert issues[["issue_type", "severity"]].to_records(index=False).tolist() == [
        ("Missing description", "Critical"),
        ("Invalid ean", "Critical"),
        ("Short product_name", "Warning"),
        ("Missing brand", "Warning"),
        ("Missing manufacturer", "Warning"),
        ("Invalid price", "Warning"),
        ("Missing attributes", "Warning"),
        ("Missing translation_de", "Warning"),
        ("Missing translation_en", "Warning"),
        ("Missing warning_notes", "Warning"),
        ("Image URL suspicious", "Info"),
    ]


def test_attribute_consistency_issue_is_preserved(valid_product):
    product = {
        **valid_product,
        "material": "Polyester",
        "attributes": "material: cotton; color: blue",
    }
    issues = product_checks.find_product_issues(pd.DataFrame([product]))
    conflict = issues.loc[issues["issue_type"] == "Different material values"].iloc[0]

    assert conflict["field_name"] == "material"
    assert conflict["severity"] == "Warning"
    assert conflict["message"] == (
        "Material unterschiedlich angegeben: material = Polyester; attributes = cotton."
    )


def test_pipeline_calls_existing_validators(monkeypatch, valid_product):
    calls = {"ean": [], "price": [], "image": []}
    original_ean = product_checks.is_valid_ean
    original_price = product_checks.is_valid_price
    original_image = product_checks.is_suspicious_image_url

    monkeypatch.setattr(
        product_checks,
        "is_valid_ean",
        lambda value: calls["ean"].append(value) or original_ean(value),
    )
    monkeypatch.setattr(
        product_checks,
        "is_valid_price",
        lambda value: calls["price"].append(value) or original_price(value),
    )
    monkeypatch.setattr(
        product_checks,
        "is_suspicious_image_url",
        lambda value: calls["image"].append(value) or original_image(value),
    )

    product_checks.find_product_issues(pd.DataFrame([valid_product]))

    assert calls == {
        "ean": [valid_product["ean"]],
        "price": [valid_product["price"]],
        "image": [valid_product["image_url"]],
    }
