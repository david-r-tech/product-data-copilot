import sys
from io import BytesIO
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from product_data_copilot.demo.furniture_demo_content import (  # noqa: E402
    FURNITURE_DEMO_CONTENT,
    FURNITURE_DEMO_DEFAULT_SKU,
    get_furniture_demo_content,
    get_furniture_demo_skus,
    toggle_furniture_demo_variant,
)


def test_default_demo_sku_has_prepared_content():
    content = get_furniture_demo_content(FURNITURE_DEMO_DEFAULT_SKU)

    assert content is not None
    assert content["bulletpoints_de"]
    assert content["html_de"]
    assert content["html_en"]


def test_all_demo_variants_have_exactly_five_bulletpoints():
    for sku in get_furniture_demo_skus():
        for variant in ["variant_a", "variant_b"]:
            content = get_furniture_demo_content(sku, variant)

            assert len(content["bulletpoints_de"]) == 5


def test_variant_a_and_b_are_visible_different():
    variant_a = get_furniture_demo_content(FURNITURE_DEMO_DEFAULT_SKU, "variant_a")
    variant_b = get_furniture_demo_content(FURNITURE_DEMO_DEFAULT_SKU, "variant_b")

    assert variant_a["bulletpoints_de"] != variant_b["bulletpoints_de"]
    assert variant_a["html_de"] != variant_b["html_de"]
    assert variant_a["html_en"] != variant_b["html_en"]


def test_variant_toggle_is_deterministic():
    assert toggle_furniture_demo_variant("variant_a") == "variant_b"
    assert toggle_furniture_demo_variant("variant_b") == "variant_a"
    assert toggle_furniture_demo_variant("unknown") == "variant_b"


def test_prepared_content_avoids_unbacked_claim_examples():
    blocked_claims = [
        "fsc",
        "zertifikat",
        "zertifiziert",
        "herkunft",
        "belastbarkeit",
        "kratzfest",
        "wasserfest",
        "handgefertigt",
        "ergonomisch",
        "premium",
        "besonders stabil",
    ]
    all_text = " ".join(
        str(value)
        for product in FURNITURE_DEMO_CONTENT.values()
        for variant in product.values()
        for value in [
            *variant["bulletpoints_de"],
            variant["html_de"],
            variant["html_en"],
        ]
    ).lower()

    for blocked_claim in blocked_claims:
        assert blocked_claim not in all_text


def test_demo_workbook_contains_unicode_umlauts():
    dataframe = pd.read_excel(PROJECT_ROOT / "data" / "moebel_demo_upload.xlsx")
    combined_text = " ".join(
        dataframe.fillna("").astype(str).to_numpy().flatten().tolist()
    )

    assert dataframe.shape == (10, 14)
    assert "PDC-MOB-001" in dataframe["Product ID"].tolist()
    assert "Türen" in combined_text
    assert "für" in combined_text
    assert "Möbel" in combined_text


def test_xlsx_unicode_roundtrip_stays_readable():
    dataframe = pd.DataFrame(
        {
            "Beschreibung": ["Sideboard mit 3 Türen"],
            "Bulletpoints": ["Geeignet für geprüfte Demo-Inhalte"],
        }
    )
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False)

    reread = pd.read_excel(BytesIO(output.getvalue()))

    assert reread.loc[0, "Beschreibung"] == "Sideboard mit 3 Türen"
    assert reread.loc[0, "Bulletpoints"] == "Geeignet für geprüfte Demo-Inhalte"
