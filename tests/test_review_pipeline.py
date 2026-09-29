"""Focused regression tests for extracted review orchestration."""

import inspect

import pandas as pd

import app
from product_data_copilot.review import review_pipeline
from product_data_copilot.review.review_helpers import ALLOWED_REVIEW_STATUSES


def test_app_uses_extracted_review_pipeline_without_duplicate_business_rules():
    assert app.create_review_tasks is review_pipeline.create_review_tasks
    assert app.filter_review_tasks is review_pipeline.filter_review_tasks
    assert app.get_filter_options is review_pipeline.get_filter_options
    assert app.get_task_type is review_pipeline.get_task_type
    assert app.allowed_manual_review_statuses is review_pipeline.allowed_manual_review_statuses
    app_source = inspect.getsource(app)
    assert "def create_review_tasks" not in app_source
    assert "def filter_review_tasks" not in app_source
    override_wrapper = inspect.getsource(app.apply_manual_review_overrides)
    assert "apply_review_overrides" in override_wrapper
    assert "readiness_status" not in override_wrapper


def test_manual_overrides_preserve_readiness_gate_and_do_not_mutate_input():
    scores = pd.DataFrame([
        {"sku": "READY", "readiness_status": "Ready", "review_status": "Ready for Export"},
        {"sku": "OPEN", "readiness_status": "Needs Review", "review_status": "Needs Review"},
        {"sku": "CRITICAL", "readiness_status": "Critical", "review_status": "Missing Data"},
    ])
    before = scores.copy(deep=True)

    updated = review_pipeline.apply_manual_review_overrides(
        scores,
        {"READY": "OK", "OPEN": "Ready for Export", "CRITICAL": "Rejected"},
    ).set_index("sku")

    assert updated.loc["READY", "review_status"] == "OK"
    assert updated.loc["OPEN", "review_status"] == "Needs Review"
    assert updated.loc["CRITICAL", "review_status"] == "Rejected"
    pd.testing.assert_frame_equal(scores, before)


def test_ok_and_ready_for_export_are_both_blocked_when_not_ready():
    scores = pd.DataFrame([
        {"sku": "OPEN", "readiness_status": "Needs Review", "review_status": "Translation Missing"},
    ])

    for protected_status in ("OK", "Ready for Export"):
        updated = review_pipeline.apply_manual_review_overrides(
            scores, {"OPEN": protected_status}
        )
        assert updated.iloc[0]["review_status"] == "Translation Missing"


def test_allowed_manual_statuses_preserve_order_and_restrictions():
    assert review_pipeline.allowed_manual_review_statuses("Ready") == ALLOWED_REVIEW_STATUSES
    assert review_pipeline.allowed_manual_review_statuses("Needs Review") == [
        status for status in ALLOWED_REVIEW_STATUSES
        if status not in {"OK", "Ready for Export"}
    ]


def test_review_task_construction_preserves_mapping_and_fallbacks():
    issues = pd.DataFrame([
        {
            "sku": "KNOWN", "issue_type": "Missing ean", "field_name": "ean",
            "severity": "Critical", "recommended_action": "EAN ergänzen.",
        },
        {
            "sku": "UNKNOWN", "issue_type": "Missing image_url", "field_name": "image_url",
            "severity": "Info", "recommended_action": "Bild ergänzen.",
        },
    ])
    scores = pd.DataFrame([
        {"sku": "KNOWN", "product_name": "Known product", "review_status": "Missing Data"},
    ])

    tasks = review_pipeline.create_review_tasks(issues, scores)

    assert tasks.columns.tolist() == [
        "sku", "product_name", "issue_type", "field_name", "task_type", "priority",
        "recommended_action", "review_status",
    ]
    assert tasks.iloc[0].to_dict() == {
        "sku": "KNOWN", "product_name": "Known product", "issue_type": "Missing ean",
        "field_name": "ean", "task_type": "Data Completion", "priority": "High",
        "recommended_action": "EAN ergänzen.", "review_status": "Missing Data",
    }
    assert tasks.iloc[1].to_dict() == {
        "sku": "UNKNOWN", "product_name": "", "issue_type": "Missing image_url",
        "field_name": "image_url", "task_type": "Media Improvement", "priority": "Low",
        "recommended_action": "Bild ergänzen.", "review_status": "Needs Review",
    }


def test_review_task_options_and_filtering_keep_existing_behavior():
    tasks = pd.DataFrame([
        {"sku": "A", "priority": "High", "task_type": "Data Completion", "review_status": "Missing Data"},
        {"sku": "B", "priority": "Low", "task_type": "Media Improvement", "review_status": "Needs Review"},
        {"sku": "C", "priority": "High", "task_type": "Data Completion", "review_status": "Missing Data"},
    ])

    assert review_pipeline.get_filter_options(tasks, "priority") == ["High", "Low"]
    assert review_pipeline.get_filter_options(tasks, "missing") == []
    filtered = review_pipeline.filter_review_tasks(
        tasks, ["High"], ["Data Completion"], ["Missing Data"]
    )
    assert filtered["sku"].tolist() == ["A", "C"]
    filtered.loc[:, "priority"] = "Changed"
    assert tasks["priority"].tolist() == ["High", "Low", "High"]
