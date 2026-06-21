import math
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.rules.validators import (  # noqa: E402
    has_min_length,
    has_useful_attributes,
    is_blank,
    is_generic_product_name,
    is_safety_relevant_category,
    is_suspicious_image_url,
    is_valid_ean,
    is_valid_price,
    normalize_text,
)


def test_blank_values_are_detected():
    assert is_blank(None)
    assert is_blank("")
    assert is_blank("   ")
    assert is_blank(math.nan)
    assert is_blank(pd.NA)
    assert not is_blank("Product")


def test_text_normalization_and_min_length():
    assert normalize_text("  Product Name  ") == "Product Name"
    assert normalize_text("") == ""
    assert has_min_length("Long enough title", 10)
    assert not has_min_length("Short", 10)


def test_ean_validation_accepts_expected_lengths():
    assert is_valid_ean("12345678")
    assert is_valid_ean("123456789012")
    assert is_valid_ean("4006381333931")
    assert is_valid_ean("12345678901234")


def test_ean_validation_rejects_invalid_values():
    assert not is_valid_ean("")
    assert not is_valid_ean("12345")
    assert not is_valid_ean("400638133393X")
    assert not is_valid_ean("4006381333931.0")


def test_price_validation():
    assert is_valid_price("19.99")
    assert is_valid_price(1)
    assert not is_valid_price("0")
    assert not is_valid_price(0)
    assert not is_valid_price("-5")
    assert not is_valid_price("free")


def test_suspicious_image_url_detection():
    assert is_suspicious_image_url("images/product.jpg")
    assert is_suspicious_image_url("https://example.com/image.jpg")
    assert not is_suspicious_image_url("")
    assert not is_suspicious_image_url("https://cdn.demo-shop.local/image.jpg")


def test_generic_product_name_detection():
    assert is_generic_product_name("BT")
    assert is_generic_product_name("Product")
    assert not is_generic_product_name("")
    assert not is_generic_product_name("Wireless Charging Pad")


def test_useful_attribute_detection():
    assert has_useful_attributes("material: cotton; color: blue")
    assert not has_useful_attributes("")
    assert not has_useful_attributes("none")
    assert not has_useful_attributes("N/A")
    assert not has_useful_attributes("-")


def test_safety_relevant_category_detection():
    assert is_safety_relevant_category("Electronics")
    assert is_safety_relevant_category("Home & Kitchen")
    assert is_safety_relevant_category("Beauty / Personal Care")
    assert not is_safety_relevant_category("")
    assert not is_safety_relevant_category("Office")
