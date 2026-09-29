"""Focused regression tests for reusable Streamlit display helpers."""

import inspect

import pandas as pd

import app
from product_data_copilot.ui import display


class FakeColumnConfig:
    def NumberColumn(self, label, **options):
        return {"kind": "number", "label": label, **options}

    def TextColumn(self, label, **options):
        return {"kind": "text", "label": label, **options}


class FakeStreamlit:
    def __init__(self):
        self.column_config = FakeColumnConfig()


class FakeContainer:
    def __init__(self):
        self.calls = []

    def dataframe(self, dataframe, **options):
        self.calls.append((dataframe, options))


def test_app_uses_extracted_display_helpers_without_duplicate_logic():
    assert app.prepare_display_dataframe is display.prepare_display_dataframe
    assert app.get_display_column_config is display.get_display_column_config
    assert app.render_readable_dataframe is display.render_readable_dataframe
    assert app.get_image_data_uri is display.get_image_data_uri
    assert app.DISPLAY_COLUMN_LABELS is display.DISPLAY_COLUMN_LABELS
    app_source = inspect.getsource(app)
    assert "def prepare_display_dataframe" not in app_source
    assert "def render_readable_dataframe" not in app_source
    assert "DISPLAY_COLUMN_LABELS = {" not in app_source


def test_display_dataframe_preparation_preserves_labels_order_and_source():
    source = pd.DataFrame([{
        "price": 10,
        "product_name": "Box",
        "readiness_status": "Ready",
        "review_status": "Translation Missing",
        "description": None,
    }])
    before = source.copy(deep=True)

    prepared = display.prepare_display_dataframe(
        source,
        preferred_columns=["product_name", "review_status", "missing"],
    )

    assert prepared.columns.tolist() == [
        "Produkt", "Prüfstatus", "Preis", "Readiness-Status", "Beschreibung",
    ]
    assert prepared.iloc[0].to_dict() == {
        "Produkt": "Box",
        "Prüfstatus": "Übersetzung fehlt",
        "Preis": 10,
        "Readiness-Status": "Bereit",
        "Beschreibung": "",
    }
    pd.testing.assert_frame_equal(source, before)


def test_display_labels_and_column_configuration_remain_unchanged(monkeypatch):
    assert display.DISPLAY_COLUMN_LABELS["overall_readiness_score"] == "Gesamt-Score"
    assert display.DISPLAY_VALUE_LABELS["review_status"]["Ready for Export"] == (
        "Keine offenen Regelverstöße"
    )
    monkeypatch.setattr(display, "st", FakeStreamlit())
    dataframe = pd.DataFrame(columns=["Gesamt-Score", "Beschreibung", "SKU", "Produkt"])

    config = display.get_display_column_config(dataframe)

    assert config == {
        "Gesamt-Score": {
            "kind": "number", "label": "Gesamt-Score", "format": "%d", "width": "small",
        },
        "Beschreibung": {"kind": "text", "label": "Beschreibung", "width": "large"},
        "SKU": {"kind": "text", "label": "SKU", "width": "small"},
        "Produkt": {"kind": "text", "label": "Produkt", "width": "medium"},
    }


def test_render_helper_remains_compatible_with_app_usage(monkeypatch):
    monkeypatch.setattr(display, "st", FakeStreamlit())
    container = FakeContainer()
    source = pd.DataFrame([{"sku": "A-1", "product_name": "Box"}])

    display.render_readable_dataframe(
        source,
        preferred_columns=["product_name", "sku"],
        height=430,
        container=container,
    )

    assert len(container.calls) == 1
    rendered, options = container.calls[0]
    assert rendered.columns.tolist() == ["Produkt", "SKU"]
    assert rendered.iloc[0].tolist() == ["Box", "A-1"]
    assert options == {
        "width": "stretch",
        "hide_index": True,
        "height": 430,
        "column_config": {
            "Produkt": {"kind": "text", "label": "Produkt", "width": "medium"},
            "SKU": {"kind": "text", "label": "SKU", "width": "small"},
        },
    }


def test_logo_data_uri_behavior_is_preserved(tmp_path):
    logo = tmp_path / "logo.png"
    logo.write_bytes(b"\x00\x01\x02")

    assert display.get_image_data_uri(logo) == "data:image/png;base64,AAEC"
    assert display.get_image_data_uri(tmp_path / "missing.png") == ""
