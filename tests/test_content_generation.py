import json
from io import BytesIO

import pandas as pd
import pytest
from openpyxl import load_workbook

from product_data_copilot.ai.content_generation import (
    approved_content_export_frames, build_content_prompt, content_export_frames, normalize_content_response,
    product_facts,
)
from product_data_copilot.export.serialization import workbook_bytes


def test_creation_prompt_uses_custom_purchasing_columns_without_inventing_facts():
    product = pd.Series({
        "sku": "A-1", "product_name": "Desk lamp", "merkmale einkauf": "Farbe: blau; Material: Aluminium",
        "ean": "12345", "image_url": "https://example.invalid/a.png",
    })
    prompt = build_content_prompt(product, "create", "fr")
    assert "merkmale einkauf" in prompt
    assert "Aluminium" in prompt
    assert "French" in prompt
    assert "12345" not in prompt
    assert "example.invalid" not in prompt
    assert "space-saving" in prompt
    assert "a cushion cover is not a bedding pillowcase" in prompt
    assert product_facts(product)["merkmale einkauf"].startswith("Farbe")


def test_creation_response_requires_matching_sku_and_keeps_five_bullets():
    payload = {
        "sku": "A-1", "de_html": '<p class="x">Lampe <strong>blau</strong><script>alert(1)</script>.</p>',
        "de_bullets": [f"Merkmal {i}" for i in range(5)],
        "translated_html": "<p>Blue lamp.</p>",
        "translated_bullets": [f"Feature {i}" for i in range(5)],
        "review_note": "All claims have been verified.",
    }
    draft = normalize_content_response(json.dumps(payload), "A-1", "create")
    assert len(draft["de_bullets"]) == 5
    assert "class=" not in draft["de_html"]
    assert "alert" not in draft["de_html"]
    assert draft["review_note"] == ""
    with pytest.raises(ValueError):
        normalize_content_response(json.dumps(payload), "WRONG", "create")


def test_translation_prompt_and_response_preserve_existing_bullet_count():
    product = pd.Series({"sku": "A-1", "description": "<p>Gute Lampe.</p>", "punkte": "Blau|Aus Aluminium"})
    prompt = build_content_prompt(product, "translate", "es", "description", "punkte")
    assert "Spanish" in prompt
    assert "Aus Aluminium" in prompt
    draft = normalize_content_response(json.dumps({
        "sku": "A-1", "translated_html": "<p>Buena lámpara.</p>",
        "translated_bullets": ["Azul", "De aluminio"],
    }), "A-1", "translate", source_bullet_count=2)
    assert draft["translated_bullets"] == ["Azul", "De aluminio"]
    assert not draft["review_note"]


def test_content_workbook_has_two_sheets_and_preserves_source_values():
    source = pd.DataFrame([{"sku": "0001", "product_name": "Box", "description": "=1+1", "price": "12.90"}])
    before = source.copy(deep=True)
    results = {"0001": {
        "de_html": "<p>Box</p>", "de_bullets": ["A", "B", "C", "D", "E"],
        "translated_html": "<p>Box in English</p>",
        "translated_bullets": ["A", "B", "C", "D", "E"],
        "status": "Entwurf – prüfen", "review_note": "",
    }}
    frames = content_export_frames(source, results, "create", "en")
    book = load_workbook(BytesIO(workbook_bytes(frames)))
    assert book.sheetnames == ["Texte & Übersetzungen", "Originaldaten"]
    assert "Produkttext EN (HTML)" in list(book.worksheets[0].values)[0]
    assert book["Originaldaten"]["C2"].value == "=1+1"
    assert book["Originaldaten"]["C2"].data_type == "s"
    assert book["Originaldaten"]["A2"].value == "0001"
    assert book["Originaldaten"]["A2"].data_type == "s"
    assert book["Originaldaten"]["D2"].value == 12.9
    assert book["Originaldaten"]["D2"].data_type == "n"
    pd.testing.assert_frame_equal(source, before)


def test_approved_content_export_excludes_open_and_rejected_texts_and_source_rows():
    products = pd.DataFrame([
        {"sku": "0001", "product_name": "Approved product", "price": "12.90"},
        {"sku": "0002", "product_name": "Open product", "price": "8.50"},
        {"sku": "0003", "product_name": "Rejected product", "price": "4.00"},
    ])
    results = {
        sku: {"de_html": f"<p>{sku}</p>", "translated_html": f"<p>{sku} EN</p>",
              "de_bullets": [], "translated_bullets": [], "review_status": status}
        for sku, status in [("0001", "approved"), ("0002", "pending"), ("0003", "rejected")]
    }
    frames = approved_content_export_frames(products, results, "create", "en")
    assert frames["Texte & Übersetzungen"]["SKU"].tolist() == ["0001"]
    assert frames["Originaldaten"]["sku"].tolist() == ["0001"]
    assert frames["Texte & Übersetzungen"]["Status"].tolist() == ["Freigegeben"]
    assert frames["Originaldaten"]["price"].tolist() == [12.9]
    assert products["price"].tolist() == ["12.90", "8.50", "4.00"]
    with pytest.raises(ValueError, match="keine freigegebenen Texte"):
        approved_content_export_frames(products, {"0002": results["0002"]}, "create", "en")
