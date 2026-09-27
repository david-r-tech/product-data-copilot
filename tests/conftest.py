"""Shared import paths and a small, fully specified product fixture."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


@pytest.fixture
def valid_product():
    return {
        "sku": "000123", "product_name": "Office Storage Box", "category": "Office",
        "description": "A blue storage box for organizing everyday office supplies.",
        "brand": "Example Brand", "manufacturer": "Example Manufacturer",
        "attributes": "color: blue", "ean": "4006381333931", "language": "en",
        "price": "12.50", "image_url": "https://images.example.org/storage-box.png",
        "warning_notes": "", "translation_de": "Blaue Aufbewahrungsbox",
        "translation_en": "Blue storage box",
    }
