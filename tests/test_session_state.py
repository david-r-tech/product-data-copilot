from product_data_copilot.review.session_state import bind_dataset, replace_smart_response, suggestion_review_key


def test_dataset_switch_removes_decisions_and_generated_content_only():
    state = {
        "dataset_fingerprint": "A", "manual_review_status_overrides": {"same-sku": "Ready for Export"},
        "ai_suggestions": {"text": "old"}, "smart_suggestions_v2_review_decisions": {"x": "approved"},
        "smart_suggestions_v2_records": ["old"], "unrelated_preference": "keep",
    }
    assert not bind_dataset(state, "A")
    assert state["ai_suggestions"]
    assert bind_dataset(state, "B")
    assert state == {"dataset_fingerprint": "B", "unrelated_preference": "keep"}


def test_invalid_dataset_also_clears_previous_decisions():
    state = {"dataset_fingerprint": "A", "manual_review_status_overrides": {"A": "Rejected"}}
    bind_dataset(state, None)
    assert "manual_review_status_overrides" not in state


def test_new_response_always_requires_a_new_review():
    state = {"smart_suggestions_v2_review_decisions": {"old": "approved"}, "smart_suggestions_v2_review_row": 2}
    result = {"suggestions": [{"sku": "A"}], "errors": [], "is_valid_json": True}
    replace_smart_response(state, sku="A", prompt="same prompt", raw_response="same response", result=result)
    assert state["smart_suggestions_v2_review_decisions"] == {}
    assert "smart_suggestions_v2_review_row" not in state


def test_review_identity_changes_with_evidence_and_avoids_delimiter_collisions():
    record = {"sku": "A", "target_field": "description", "current_value": "old", "proposed_value": "new"}
    for change in [{"reason": "changed"}, {"source_fields": ["other"]}, {"risk_level": "high"}]:
        assert suggestion_review_key(record) != suggestion_review_key({**record, **change})
    assert suggestion_review_key({"sku": "A | B", "target_field": "C"}) != suggestion_review_key({"sku": "A", "target_field": "B | C"})
