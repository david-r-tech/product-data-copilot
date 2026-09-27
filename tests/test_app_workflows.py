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


def suggestions_table(at):
    return next(element.value for element in at.dataframe if "Human Review Status" in element.value.columns)


def test_sample_start_and_runtime_have_no_demo_controls():
    at = AppTest.from_string("import app; app.run_app()", default_timeout=20).run()
    assert not at.exception
    assert len(at.tabs) == 7
    assert all("demo" not in button.label.lower() for button in at.button)
    assert not hasattr(app, "load_smart_suggestions_v2_demo_response")
    assert any("fictional" in element.value for element in at.info)
    issues_table = next(
        element.value for element in at.dataframe
        if {"Severity", "Issue"}.issubset(element.value.columns)
    )
    assert issues_table.iloc[0]["Severity"] == "Critical"


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


def test_file_switch_clears_approval_and_v1_text_for_same_sku(valid_product):
    at = start_with_rows([valid_product])
    assert not at.exception
    at.selectbox(key="manual_review_status").select("Ready for Export")
    click(at, "Save Review Status")
    at.session_state["ai_suggestions_sku"] = valid_product["sku"]
    at.session_state["ai_suggestions"] = {"improved_product_title": "OLD FILE DRAFT"}
    changed = {**valid_product, "product_name": "Different Product", "ean": ""}
    at.session_state["audit_content"] = pd.DataFrame([changed]).to_csv(index=False).encode()
    at.run()
    assert not at.exception
    assert at.session_state["manual_review_status_overrides"] == {}
    assert "ai_suggestions" not in at.session_state
    assert not any("OLD FILE DRAFT" in element.value for element in at.markdown)
    assert "Ready for Export" not in at.selectbox(key="manual_review_status").options


def test_manual_status_form_follows_selected_product_and_clear(valid_product):
    second = {**valid_product, "sku": "SECOND", "product_name": "Second Storage Box"}
    at = start_with_rows([valid_product, second])
    at.selectbox(key="manual_review_status").select("Rejected")
    click(at, "Save Review Status")
    choices = at.selectbox(key="manual_review_product").options
    at.selectbox(key="manual_review_product").select(choices[1]).run()
    assert at.selectbox(key="manual_review_status").value == "Ready for Export"
    at.selectbox(key="manual_review_product").select(choices[0]).run()
    assert at.selectbox(key="manual_review_status").value == "Rejected"
    click(at, "Clear Review Status")
    assert not at.exception
    assert at.selectbox(key="manual_review_status").value == "Ready for Export"


def test_generation_approval_rejection_pending_and_regeneration(valid_product, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-placeholder")
    record = {
        "sku": valid_product["sku"], "target_field": "description", "current_value": valid_product["description"],
        "proposed_value": "Blue storage box for office supplies.", "source_fields": ["description"],
        "reason": "Shortens the original description.", "confidence": "medium", "risk_level": "low",
    }
    response = {"smart_suggestions": [record]}
    monkeypatch.setattr(app, "generate_smart_suggestions_v2", lambda prompt: json.dumps(response))
    at = start_with_rows([valid_product])
    click(at, "Generate Smart Suggestions v2")
    assert not at.exception
    assert suggestions_table(at).iloc[0]["Human Review Status"] == "pending"
    click(at, "Approve")
    assert suggestions_table(at).iloc[0]["Human Review Status"] == "approved"
    click(at, "Reject")
    assert suggestions_table(at).iloc[0]["Human Review Status"] == "rejected"
    click(at, "Mark Pending")
    assert suggestions_table(at).iloc[0]["Human Review Status"] == "pending"
    click(at, "Approve")
    record["risk_level"] = "high"
    record["reason"] = "New reason, same proposed text."
    click(at, "Generate Smart Suggestions v2")
    assert not at.exception
    assert suggestions_table(at).iloc[0]["Human Review Status"] == "pending"
    assert at.session_state["smart_suggestions_v2_review_decisions"] == {}
    record["source_fields"] = ["nonexistent"]
    click(at, "Generate Smart Suggestions v2")
    assert suggestions_table(at).iloc[0]["Human Review Status"] == "blocked"
    assert all(button.label != "Approve" for button in at.button)


def test_generation_failure_clears_old_suggestions_without_exposing_provider_details(valid_product, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-placeholder")
    def failed_response(prompt):
        raise RuntimeError("provider detail containing private data")
    monkeypatch.setattr(app, "generate_smart_suggestions_v2", failed_response)
    at = start_with_rows([valid_product])
    at.session_state["smart_suggestions_v2_review_decisions"] = {"old": {"approval_state": "approved"}}
    click(at, "Generate Smart Suggestions v2")
    assert not at.exception
    assert at.session_state["smart_suggestions_v2_records"] == []
    assert at.session_state["smart_suggestions_v2_review_decisions"] == {}
    assert not any("private data" in item.value for item in at.markdown)


def test_control_characters_and_long_cells_do_not_crash_the_app(valid_product):
    at = start_with_rows([{**valid_product, "description": "Before\x0bAfter"}])
    assert not at.exception
    at = start_with_rows([{**valid_product, "description": "x" * 32768}])
    assert not at.exception
    assert any("32,767" in element.value for element in at.error)


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
