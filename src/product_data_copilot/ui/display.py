"""Reusable Streamlit display and table-formatting helpers."""

import base64

import streamlit as st


DISPLAY_COLUMN_LABELS = {
    "sku": "SKU",
    "product_name": "Produkt",
    "category": "Kategorie",
    "description": "Beschreibung",
    "brand": "Marke",
    "manufacturer": "Hersteller",
    "attributes": "Merkmale",
    "ean": "EAN",
    "language": "Sprache",
    "price": "Preis",
    "image_url": "Bild-URL",
    "warning_notes": "Warnhinweise",
    "translation_de": "Übersetzung DE",
    "translation_en": "Übersetzung EN",
    "data_quality_score": "Datenqualität",
    "marketplace_readiness_score": "Marktplatz-Reife",
    "translation_readiness_score": "Übersetzungs-Reife",
    "compliance_readiness_score": "Compliance-Reife",
    "ai_content_readiness_score": "KI-Content-Reife",
    "overall_readiness_score": "Gesamt-Score",
    "readiness_status": "Readiness-Status",
    "review_status": "Prüfstatus",
    "issue_type": "Art der Auffälligkeit",
    "field_name": "Feld",
    "severity": "Schweregrad",
    "message": "Auffälligkeit",
    "recommended_action": "Nächster Schritt",
    "task_type": "Aufgabentyp",
    "priority": "Priorität",
    "products": "Artikel",
    "tasks": "Aufgaben",
    "metric": "Kennzahl",
    "value": "Wert",
    "target_field": "Feld",
    "field": "Feld",
    "current_value": "Aktueller Wert",
    "proposed_value": "Vorgeschlagener Wert",
    "suggested_value": "Vorgeschlagener Wert",
    "original_value": "Originalwert",
    "approved_value": "Freigegebener Wert",
    "source_fields": "Quellfelder",
    "reason": "Begründung",
    "confidence": "Konfidenz",
    "risk_level": "Risiko",
    "human_review_status": "Menschlicher Prüfstatus",
    "suggestion_status": "Vorschlagsstatus",
    "approval_status": "Freigabestatus",
    "export_status": "Exportstatus",
    "suggestion_id": "Vorschlags-ID",
    "source": "Quelle",
}

TEXT_HEAVY_COLUMNS = {
    "Beschreibung",
    "Merkmale",
    "Bild-URL",
    "Warnhinweise",
    "Übersetzung DE",
    "Übersetzung EN",
    "Begründung",
    "Quellfelder",
    "Vorgeschlagener Wert",
    "Originalwert",
    "Freigegebener Wert",
    "Aktueller Wert",
    "Wert",
    "Quelle",
}
SMALL_COLUMNS = {
    "SKU",
    "Feld",
    "EAN",
    "Preis",
    "Sprache",
    "Schweregrad",
    "Priorität",
    "Risiko",
    "Konfidenz",
    "Artikel",
    "Aufgaben",
    "Exportstatus",
}
SCORE_COLUMNS = {
    "Datenqualität",
    "Marktplatz-Reife",
    "Übersetzungs-Reife",
    "Compliance-Reife",
    "KI-Content-Reife",
    "Gesamt-Score",
}

DISPLAY_VALUE_LABELS = {
    "readiness_status": {
        "Ready": "Bereit",
        "Critical": "Kritisch",
        "Needs Review": "Prüfung nötig",
    },
    "review_status": {
        "OK": "OK",
        "Needs Review": "Prüfung nötig",
        "Missing Data": "Daten fehlen",
        "AI Suggestion Created": "KI-Entwurf vorhanden",
        "Translation Missing": "Übersetzung fehlt",
        "Compliance Check Required": "Fachprüfung nötig",
        "Ready for Export": "Keine offenen Regelverstöße",
        "Rejected": "Abgelehnt",
    },
}


def get_image_data_uri(image_path):
    """Return a base64 data URI for a local PNG image."""
    if not image_path.exists():
        return ""

    encoded_image = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded_image}"


def make_display_safe(dataframe):
    display_dataframe = dataframe.copy()

    for column in display_dataframe.columns:
        if display_dataframe[column].dtype == "object":
            display_dataframe[column] = display_dataframe[column].fillna("").astype(str)

    return display_dataframe


def prepare_display_dataframe(dataframe, preferred_columns=None):
    """Return a display-only copy with business labels and prioritized columns."""
    display_dataframe = make_display_safe(dataframe)

    if preferred_columns:
        preferred_existing_columns = [
            column for column in preferred_columns if column in display_dataframe.columns
        ]
        remaining_columns = [
            column
            for column in display_dataframe.columns
            if column not in preferred_existing_columns
        ]
        display_dataframe = display_dataframe[
            preferred_existing_columns + remaining_columns
        ]

    for column, labels in DISPLAY_VALUE_LABELS.items():
        if column in display_dataframe:
            display_dataframe[column] = display_dataframe[column].replace(labels)

    return display_dataframe.rename(columns=DISPLAY_COLUMN_LABELS)


def get_display_column_config(display_dataframe):
    """Return Streamlit column config for readable, display-only tables."""
    column_config = {}

    for column_name in display_dataframe.columns:
        if column_name in SCORE_COLUMNS:
            column_config[column_name] = st.column_config.NumberColumn(
                column_name,
                format="%d",
                width="small",
            )
        elif column_name in TEXT_HEAVY_COLUMNS:
            column_config[column_name] = st.column_config.TextColumn(
                column_name,
                width="large",
            )
        elif column_name in SMALL_COLUMNS:
            column_config[column_name] = st.column_config.TextColumn(
                column_name,
                width="small",
            )
        else:
            column_config[column_name] = st.column_config.TextColumn(
                column_name,
                width="medium",
            )

    return column_config


def render_readable_dataframe(
    dataframe,
    preferred_columns=None,
    height=420,
    container=None,
):
    """Render a DataFrame with display-only labels, ordering, and hidden index."""
    streamlit_target = container or st
    display_dataframe = prepare_display_dataframe(dataframe, preferred_columns)
    streamlit_target.dataframe(
        display_dataframe,
        width="stretch",
        hide_index=True,
        height=height,
        column_config=get_display_column_config(display_dataframe),
    )
