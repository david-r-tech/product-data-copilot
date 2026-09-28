"""Offline regression tests of complete Streamlit reruns, decisions and exports."""

import json

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

import app

APP_WITH_UPLOAD = '''
import io
from unittest.mock import patch
import streamlit as st
import app
uploaded = io.BytesIO(st.session_state["audit_content"])
uploaded.name = st.session_state.get("audit_filename", "products.csv")
with patch.object(app, "render_data_input_section", return_value=uploaded):
    app.run_app()
'''


@pytest.fixture(autouse=True)
def no_provider_calls(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "")
    monkeypatch.setattr(app, "load_dotenv", lambda *args, **kwargs: None)

    def fail_provider(*args, **kwargs):
        raise AssertionError("Tests must not send product data to a provider")

    monkeypatch.setattr(app, "OpenAI", fail_provider)


def start_with_rows(rows):
    at = AppTest.from_string(APP_WITH_UPLOAD, default_timeout=20)
    at.session_state["audit_content"] = pd.DataFrame(rows).to_csv(index=False).encode("utf-8")
    return at.run()


def click(at, label):
    return next(button for button in at.button if button.label == label).click().run()


def click_content_start(at):
    return next(button for button in at.button if button.label.startswith("Jetzt Texte für ")).click().run()


def test_sample_start_and_runtime_have_no_demo_controls():
    at = AppTest.from_string("import app; app.run_app()", default_timeout=20).run()
    assert not at.exception
    assert [tab.label for tab in at.tabs] == [
        "Daten prüfen", "Texte erstellen & übersetzen", "Ergebnisse & Export",
    ]
    assert all("demo" not in button.label.lower() for button in at.button)
    assert not hasattr(app, "load_smart_suggestions_v2_demo_response")
    assert any("fiktive" in element.value for element in at.info)
    assert any(
        element.value == "KI-Entwurf → Quelldaten prüfen → Mensch gibt frei → nur Freigegebenes wird exportiert."
        for element in at.info
    )
    issues_table = next(
        element.value for element in at.dataframe
        if {"Schweregrad", "Problem", "Nächster Schritt"}.issubset(element.value.columns)
    )
    assert issues_table.iloc[0]["Schweregrad"] == "Kritisch"
    assert any(
        {"SKU", "Produkt", "Schweregrad", "Problem", "Nächster Schritt"}.issubset(table.value.columns)
        for table in at.dataframe
    )


def test_visible_issue_messages_are_german_but_internal_identifiers_stay_stable(valid_product):
    products = pd.DataFrame([{**valid_product, "description": "", "price": "0"}])
    issues = app.find_product_issues(products).set_index("issue_type")
    assert issues.loc["Missing description", "message"] == "Produktbeschreibung fehlt."
    assert issues.loc["Missing description", "recommended_action"] == (
        "Eine aussagekräftige Produktbeschreibung ergänzen."
    )
    assert issues.loc["Invalid price", "message"] == "Der Produktpreis muss größer als 0 sein."
    assert issues.loc["Invalid price", "severity"] == "Warning"


def test_display_labels_are_german_without_renaming_source_columns():
    source = pd.DataFrame([{
        "product_name": "Box", "category": "Aufbewahrung", "description": "Text",
        "brand": "Marke", "manufacturer": "Hersteller", "attributes": "Farbe: Blau",
        "price": "10", "severity": "Warning", "priority": "Medium",
        "recommended_action": "Prüfen", "review_status": "Needs Review",
        "readiness_status": "Needs Review", "overall_readiness_score": 80,
    }])
    original_columns = source.columns.tolist()
    displayed = app.prepare_display_dataframe(source)
    assert displayed.columns.tolist() == [
        "Produkt", "Kategorie", "Beschreibung", "Marke", "Hersteller", "Merkmale",
        "Preis", "Schweregrad", "Priorität", "Nächster Schritt", "Prüfstatus",
        "Readiness-Status", "Gesamt-Score",
    ]
    assert displayed.iloc[0]["Prüfstatus"] == "Prüfung nötig"
    assert displayed.iloc[0]["Readiness-Status"] == "Prüfung nötig"
    assert source.columns.tolist() == original_columns
    assert source.iloc[0]["review_status"] == "Needs Review"


def test_explicit_supplier_attribute_conflict_appears_in_correction_list(valid_product):
    at = start_with_rows([{**valid_product, "material": "Polyester", "farbe": "Rot",
                           "attributes": "material: cotton; color: blue"}])
    assert not at.exception
    correction_list = next(
        element.value for element in at.dataframe
        if {"Schweregrad", "Problem", "Nächster Schritt"}.issubset(element.value.columns)
    )
    problems = correction_list["Problem"].tolist()
    assert any("Material unterschiedlich" in problem for problem in problems)
    assert any("Farbe unterschiedlich" in problem for problem in problems)


def _content_response(sku):
    return json.dumps({
        "sku": sku,
        "de_html": "<p>Eine praktische Aufbewahrungsbox für Büromaterial.</p>",
        "de_bullets": [f"Merkmal {i}" for i in range(1, 6)],
        "translated_html": "<p>A practical storage box for office supplies.</p>",
        "translated_bullets": [f"Feature {i}" for i in range(1, 6)],
        "review_note": "",
    })


def test_content_generation_covers_whole_uploaded_file_before_review(valid_product, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-placeholder")
    second = {**valid_product, "sku": "SECOND", "product_name": "Second Storage Box"}
    calls = []
    def provider(prompt):
        calls.append(prompt)
        return _content_response("SECOND" if 'sku: "SECOND"' in prompt else valid_product["sku"])
    monkeypatch.setattr(app, "request_content_draft", provider)
    at = start_with_rows([valid_product, second])
    assert any("zuerst einen deutschen HTML-Text" in element.value for element in at.info)
    assert any("Auswahlregel wird für jeden Artikel einzeln angewendet" in element.value for element in at.caption)
    assert any("2 Artikel" in button.label for button in at.button if button.label.startswith("Jetzt Texte für "))
    click_content_start(at)
    assert not at.exception
    assert len(calls) == 2
    job = next(iter(at.session_state["content_jobs"].values()))
    assert set(job) == {valid_product["sku"], "SECOND"}
    assert len(job["SECOND"]["de_bullets"]) == 5
    assert any(button.label == "Text freigeben" for button in at.button)
    assert any("Gib mindestens einen Artikel" in element.value for element in at.info)
    assert all(not button.label.startswith("Jetzt Texte für ") for button in at.button)


def test_bulk_drafts_are_reviewed_per_article_before_export(valid_product, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-placeholder")
    second = {**valid_product, "sku": "SECOND", "product_name": "Second Storage Box"}
    monkeypatch.setattr(
        app, "request_content_draft",
        lambda prompt: _content_response("SECOND" if 'sku: "SECOND"' in prompt else valid_product["sku"]),
    )
    at = start_with_rows([valid_product, second])
    click_content_start(at)
    assert not at.exception
    assert any("Gib mindestens einen Artikel" in element.value for element in at.info)
    click(at, "Text freigeben")
    job = next(iter(at.session_state["content_jobs"].values()))
    assert job[valid_product["sku"]]["review_status"] == "approved"
    at.selectbox(key="content_preview_sku").select("SECOND").run()
    click(at, "Text ablehnen")
    assert job["SECOND"]["review_status"] == "rejected"
    assert not any("Gib mindestens einen Artikel" in element.value for element in at.info)
    at.selectbox(key="content_preview_sku").select(valid_product["sku"]).run()
    click(at, "Entscheidung zurücknehmen")
    assert "review_status" not in job[valid_product["sku"]]
    assert any("Gib mindestens einen Artikel" in element.value for element in at.info)


def test_content_generation_single_product_and_language(valid_product, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-placeholder")
    second = {**valid_product, "sku": "SECOND", "product_name": "Second Storage Box"}
    calls = []
    monkeypatch.setattr(app, "request_content_draft", lambda prompt: calls.append(prompt) or _content_response("SECOND"))
    at = start_with_rows([valid_product, second])
    at.radio(key="content_scope").set_value("Einzelner Artikel").run()
    at.selectbox(key="content_product").select(at.selectbox(key="content_product").options[1]).run()
    at.selectbox(key="content_language").select("fr").run()
    click_content_start(at)
    assert not at.exception
    assert len(calls) == 1
    assert "French" in calls[0]
    job = next(iter(at.session_state["content_jobs"].values()))
    assert set(job) == {"SECOND"}


def test_content_source_transparency_matches_creation_selection(valid_product):
    product = {**valid_product, "material_einkauf": "Aluminium", "price": "19.90",
               "ean": "4006381333931", "image_url": "https://example.invalid/image.jpg"}
    at = start_with_rows([product])
    at.radio(key="content_scope").set_value("Einzelner Artikel").run()
    assert not at.exception
    assert any("Welche Daten werden an OpenAI gesendet?" in item.value for item in at.markdown)
    transparency = next(
        element.value for element in at.dataframe
        if list(element.value.columns) == ["Feld", "Gesendeter Wert"]
    )
    sent_fields = transparency["Feld"].tolist()
    assert "sku" in sent_fields
    assert "material_einkauf" in sent_fields
    assert "price" not in sent_fields
    assert "ean" not in sent_fields
    assert "image_url" not in sent_fields
    assert any("Erstellen-Button" in item.value for item in at.caption)


def test_translation_source_transparency_names_only_selected_inputs(valid_product):
    at = start_with_rows([{**valid_product, "punkte": "A|B"}])
    at.radio(key="content_task").set_value("Vorhandene Texte übersetzen").run()
    at.selectbox(key="content_bullet_column").select("punkte").run()
    assert not at.exception
    message = next(item.value for item in at.caption if "Übersetzen-Button" in item.value)
    assert "description" in message
    assert "punkte" in message
    assert "Preis" not in message


def test_translation_mode_skips_missing_source_without_provider_call(valid_product, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-placeholder")
    monkeypatch.setattr(app, "request_content_draft", lambda prompt: pytest.fail("Provider must not be called"))
    at = start_with_rows([{**valid_product, "description": ""}])
    at.radio(key="content_task").set_value("Vorhandene Texte übersetzen").run()
    click(at, "Jetzt 1 Artikel übersetzen")
    assert not at.exception
    job = next(iter(at.session_state["content_jobs"].values()))
    assert job[valid_product["sku"]]["status"] == "Quelltext fehlt"


@pytest.mark.parametrize("content,filename", [
    (b"", "file.csv"), (b"sku,product_name\n", "file.csv"),
    (b"sku,product_name\n,Product\n", "file.csv"),
    (b"sku,product_name\nSAME,First\nSAME,Second", "file.csv"),
    (b"not Excel", "file.xlsx"), (b"unknown,columns\nA,B", "file.csv"),
])
def test_bad_uploads_show_an_error_without_a_traceback(content, filename):
    at = AppTest.from_string(APP_WITH_UPLOAD, default_timeout=20)
    at.session_state["audit_content"] = content
    at.session_state["audit_filename"] = filename
    at.run()
    assert not at.exception
    assert len(at.error) == 1
    assert len(at.tabs) == 0
    assert all(
        english not in at.error[0].value
        for english in ("The file", "Upload", "Missing required", "Every product", "Use a", "Row ")
    )
    assert any("Korrigiere die Datei" in element.value for element in at.info)


def test_file_switch_clears_content_drafts_for_same_sku(valid_product):
    at = start_with_rows([valid_product])
    assert not at.exception
    at.selectbox(key="manual_review_status").select("Ready for Export")
    click(at, "Prüfstatus speichern")
    at.session_state["content_jobs"] = {"job": {valid_product["sku"]: {"translated_html": "OLD FILE DRAFT"}}}
    changed = {**valid_product, "product_name": "Different Product", "ean": ""}
    at.session_state["audit_content"] = pd.DataFrame([changed]).to_csv(index=False).encode()
    at.run()
    assert not at.exception
    assert at.session_state["manual_review_status_overrides"] == {}
    assert "content_jobs" not in at.session_state
    assert not any("OLD FILE DRAFT" in element.value for element in at.markdown)
    assert "Ready for Export" not in at.selectbox(key="manual_review_status").options


def test_manual_status_form_follows_selected_product_and_clear(valid_product):
    second = {**valid_product, "sku": "SECOND", "product_name": "Second Storage Box"}
    at = start_with_rows([valid_product, second])
    at.selectbox(key="manual_review_status").select("Rejected")
    click(at, "Prüfstatus speichern")
    choices = at.selectbox(key="manual_review_product").options
    at.selectbox(key="manual_review_product").select(choices[1]).run()
    assert at.selectbox(key="manual_review_status").value == "Ready for Export"
    at.selectbox(key="manual_review_product").select(choices[0]).run()
    assert at.selectbox(key="manual_review_status").value == "Rejected"
    click(at, "Prüfstatus zurücksetzen")
    assert not at.exception
    assert at.selectbox(key="manual_review_status").value == "Ready for Export"


def test_control_characters_and_long_cells_do_not_crash_the_app(valid_product):
    at = start_with_rows([{**valid_product, "description": "Before\x0bAfter"}])
    assert not at.exception
    at = start_with_rows([{**valid_product, "description": "x" * 32768}])
    assert not at.exception
    assert any("32.767" in element.value for element in at.error)


def test_critical_issues_cannot_be_averaged_into_ready(valid_product):
    products = pd.DataFrame([{**valid_product, "ean": ""}])
    issues = app.find_product_issues(products)
    scores = app.calculate_readiness_scores(products, issues)
    assert scores.iloc[0]["overall_readiness_score"] > 85
    assert scores.iloc[0]["readiness_status"] == "Critical"
    assert scores.iloc[0]["review_status"] == "Missing Data"
    products.loc[0, "ean"] = valid_product["ean"]
    products.loc[0, "description"] = "x"
    issues = app.find_product_issues(products)
    scores = app.calculate_readiness_scores(products, issues)
    assert scores.iloc[0]["readiness_status"] == "Needs Review"
    assert scores.iloc[0]["review_status"] == "Needs Review"


def test_empty_task_filter_means_no_tasks(valid_product):
    products = pd.DataFrame([{**valid_product, "ean": ""}])
    issues = app.find_product_issues(products)
    tasks = app.create_review_tasks(issues, app.calculate_readiness_scores(products, issues))
    assert not tasks.empty
    assert app.filter_review_tasks(tasks, [], ["Data Completion"], ["Missing Data"]).empty


def test_review_tasks_keep_the_correct_product_name_and_priority(valid_product):
    second = {**valid_product, "sku": "SECOND", "product_name": "Second Storage Box", "ean": ""}
    products = pd.DataFrame([valid_product, second])
    issues = app.prioritize_issues(app.find_product_issues(products))
    scores = app.calculate_readiness_scores(products, issues)
    tasks = app.create_review_tasks(issues, scores)
    assert tasks.iloc[0]["sku"] == "SECOND"
    assert tasks.iloc[0]["product_name"] == "Second Storage Box"
    assert tasks.iloc[0]["priority"] == "High"
