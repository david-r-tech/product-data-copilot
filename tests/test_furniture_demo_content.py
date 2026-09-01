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
    FURNITURE_DEMO_REVIEW_APPROVED,
    FURNITURE_DEMO_REVIEW_OPEN,
    FURNITURE_DEMO_REVIEW_SECTION_KEYS,
    approve_furniture_demo_review_section,
    count_approved_furniture_demo_sections,
    get_furniture_demo_final_review_status,
    get_furniture_demo_content,
    get_furniture_demo_skus,
    get_next_furniture_demo_position,
    reset_furniture_demo_review_decisions,
    should_advance_furniture_demo_product,
    toggle_furniture_demo_variant,
)
sys.path.insert(0, str(PROJECT_ROOT))

from app import build_furniture_demo_export  # noqa: E402


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


def test_product_is_not_fully_approved_before_three_review_steps():
    decisions = reset_furniture_demo_review_decisions()

    assert count_approved_furniture_demo_sections(decisions) == 0
    assert get_furniture_demo_final_review_status(decisions) == FURNITURE_DEMO_REVIEW_OPEN
    assert not should_advance_furniture_demo_product(decisions)

    decisions = approve_furniture_demo_review_section(decisions, "bulletpoints")

    assert count_approved_furniture_demo_sections(decisions) == 1
    assert get_furniture_demo_final_review_status(decisions) == FURNITURE_DEMO_REVIEW_OPEN
    assert not should_advance_furniture_demo_product(decisions)

    decisions = approve_furniture_demo_review_section(decisions, "html_de")

    assert count_approved_furniture_demo_sections(decisions) == 2
    assert get_furniture_demo_final_review_status(decisions) == FURNITURE_DEMO_REVIEW_OPEN
    assert not should_advance_furniture_demo_product(decisions)


def test_product_is_fully_approved_after_three_review_steps():
    decisions = reset_furniture_demo_review_decisions()
    for section_key in FURNITURE_DEMO_REVIEW_SECTION_KEYS:
        decisions = approve_furniture_demo_review_section(decisions, section_key)

    assert count_approved_furniture_demo_sections(decisions) == 3
    assert (
        get_furniture_demo_final_review_status(decisions)
        == FURNITURE_DEMO_REVIEW_APPROVED
    )
    assert should_advance_furniture_demo_product(decisions)


def test_auto_advance_target_keeps_current_product_until_full_approval():
    decisions = approve_furniture_demo_review_section(
        reset_furniture_demo_review_decisions(),
        "bulletpoints",
    )

    assert not should_advance_furniture_demo_product(decisions)
    assert get_next_furniture_demo_position(0, 10) == 1
    assert get_next_furniture_demo_position(9, 10) == 9


def test_furniture_demo_export_uses_only_single_final_review_status():
    source_dataframe = pd.DataFrame(
        {
            "Product ID": [FURNITURE_DEMO_DEFAULT_SKU],
            "Product Name": ["Nordic Lounge Sofa 3-Sitzer"],
            "Beschreibung": [""],
            "Bulletpoints": [""],
            "Englische Übersetzung": [""],
            "bullet_points_review_status": [FURNITURE_DEMO_REVIEW_APPROVED],
            "html_de_review_status": [FURNITURE_DEMO_REVIEW_APPROVED],
            "html_en_review_status": [FURNITURE_DEMO_REVIEW_APPROVED],
            "human_review_status": [FURNITURE_DEMO_REVIEW_APPROVED],
        }
    )
    decisions = reset_furniture_demo_review_decisions()
    for section_key in FURNITURE_DEMO_REVIEW_SECTION_KEYS:
        decisions = approve_furniture_demo_review_section(decisions, section_key)

    export_dataframe = build_furniture_demo_export(
        source_dataframe,
        review_status_by_sku={FURNITURE_DEMO_DEFAULT_SKU: decisions},
    )

    assert export_dataframe.loc[0, "review_status"] == FURNITURE_DEMO_REVIEW_APPROVED
    assert "bullet_points_review_status" not in export_dataframe.columns
    assert "html_de_review_status" not in export_dataframe.columns
    assert "html_en_review_status" not in export_dataframe.columns
    assert "human_review_status" not in export_dataframe.columns


def test_furniture_demo_export_keeps_partial_review_unapproved():
    source_dataframe = pd.DataFrame(
        {
            "Product ID": [FURNITURE_DEMO_DEFAULT_SKU],
            "Product Name": ["Nordic Lounge Sofa 3-Sitzer"],
            "Beschreibung": [""],
            "Bulletpoints": [""],
            "Englische Übersetzung": [""],
        }
    )
    decisions = approve_furniture_demo_review_section(
        reset_furniture_demo_review_decisions(),
        "bulletpoints",
    )

    export_dataframe = build_furniture_demo_export(
        source_dataframe,
        review_status_by_sku={FURNITURE_DEMO_DEFAULT_SKU: decisions},
    )

    assert export_dataframe.loc[0, "review_status"] == FURNITURE_DEMO_REVIEW_OPEN
