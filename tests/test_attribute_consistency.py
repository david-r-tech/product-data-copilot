import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from product_data_copilot.rules.attribute_consistency import explicit_attribute_conflicts  # noqa: E402


def test_explicit_color_material_and_surface_differences_are_found():
    row = pd.Series({
        "farbe": "Blau", "material": "Baumwolle", "oberfläche": "Matt",
        "attributes": "color: Red; Material: Polyester; surface: glossy; size: M",
    })
    conflicts = explicit_attribute_conflicts(row)
    assert [kind for kind, _, _ in conflicts] == ["material", "color", "surface"]
    assert conflicts[0][1] == ("material", "Baumwolle")
    assert conflicts[0][2] == ("attributes", "Polyester")


def test_equal_or_more_specific_explicit_values_are_not_flagged():
    row = pd.Series({
        "color": "blue", "material": "cotton", "surface": "matte",
        "attributes": "color: dark blue; material: organic cotton; finish: matte",
    })
    assert explicit_attribute_conflicts(row) == []


def test_unstructured_prose_and_missing_values_are_not_guessed():
    row = pd.Series({
        "color": "red", "description": "The product may be blue or red.",
        "material": pd.NA, "attributes": "material: polyester; color: n/a",
    })
    assert explicit_attribute_conflicts(row) == []
