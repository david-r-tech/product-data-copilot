# Smart Suggestions v2 - Runtime Integration Plan

## 1. Goal

Plan the safest path for wiring Smart Suggestions v2 into the existing Streamlit app without changing current AI Suggestions v1 behavior yet.

The next implementation block should create visible app value by adding an experimental structured-suggestions area to the existing AI Suggestions tab.

## 2. Current Runtime Shape

Current AI Suggestions v1 lives in the existing `AI Suggestions` tab in `app.py`.

It currently:

- selects one product
- shows selected product context
- shows current issues for that product
- lets the user choose broad suggestion types
- uses `build_ai_prompt(...)`
- calls OpenAI only when `Generate AI Suggestions` is clicked
- stores one product-level suggestion payload in `st.session_state["ai_suggestions"]`
- shows product-level sections such as improved title, description, bullet points, translation, compliance note, and human review notes
- exports the V1 payload as `ai_suggestions.csv`

Smart Suggestions v2 helpers already exist but are not wired into runtime:

- `build_smart_suggestion_prompt(...)` from `suggestion_prompt_adapter.py`
- `parse_and_normalize_suggestions(...)` from `suggestion_parser.py`
- schema defaults and normalization from `suggestion_schema.py`

## 3. Placement in the Existing Tab

V2 should appear inside the existing `AI Suggestions` tab, below the current V1 flow.

Recommended structure:

1. Keep the existing V1 section unchanged.
2. Add a divider.
3. Add a section titled `Experimental Smart Suggestions v2`.
4. Reuse the already selected product, selected issues, selected score, and review tasks for that SKU.
5. Add a separate button: `Generate Smart Suggestions v2`.
6. Show parsed V2 suggestions as a table.

This avoids adding new tabs, avoids redesign, and makes the improvement visible without breaking the current demo workflow.

## 4. How V1 Remains Unchanged

The implementation phase must not replace:

- `build_ai_prompt(...)`
- `generate_ai_suggestions(...)`
- `suggestions_to_dataframe(...)`
- V1 session-state keys:
  - `ai_suggestions`
  - `ai_suggestions_sku`
- V1 UI labels and CSV download

V2 should use separate names, for example:

- `generate_smart_suggestions_v2(...)`
- `smart_suggestions_v2`
- `smart_suggestions_v2_sku`
- `smart_suggestions_v2_errors`
- `smart_suggestions_v2_raw_response`

## 5. Helper Connection

Recommended runtime flow:

1. Build prompt input from the selected product and current audit context.
2. Use `build_smart_suggestion_prompt(product_record, issue_records, review_task_records)`.
3. Call OpenAI only after the user clicks the V2 button and only when `OPENAI_API_KEY` exists.
4. Pass the raw response text into `parse_and_normalize_suggestions(raw_response)`.
5. Store normalized rows and parser metadata in `st.session_state`.
6. Convert normalized rows to a DataFrame for display and optional CSV export.

Minimal pseudocode:

```python
prompt = build_smart_suggestion_prompt(
    selected_product_context,
    selected_issues.to_dict(orient="records"),
    selected_review_tasks.to_dict(orient="records"),
)
raw_response = call_openai(prompt)
parsed = parse_and_normalize_suggestions(raw_response)
suggestions_df = pd.DataFrame(parsed["suggestions"])
```

The OpenAI provider call can reuse the same model/env behavior as V1.

## 6. DataFrame Shape

The V2 table should use stable schema columns from the normalized suggestions:

- `sku`
- `product_name`
- `target_field`
- `current_value`
- `proposed_value`
- `source_fields`
- `reason`
- `confidence`
- `risk_level`
- `requires_human_approval`
- `approval_status`
- `suggestion_status`

For Streamlit display, convert `source_fields` lists into readable strings such as `", ".join(source_fields)`.

If no rows are returned, show a clear info message instead of an empty confusing table.

## 7. Review-Required Defaults

All V2 suggestions must start as human-review items because:

- AI output can be incomplete or wrong.
- Product data changes affect marketplace quality and business operations.
- Safety/compliance-relevant content must be reviewed by a person.
- Source data can be weak or missing.
- The app must not imply automatic approval or automatic write-back.

The parser already downgrades AI-supplied approved-like statuses to review-required defaults. Runtime UI should reinforce this with copy such as:

`Smart Suggestions v2 are experimental draft records. They are not applied to product data and require human review.`

## 8. Invalid or Unsafe AI Output

If V2 output is invalid JSON:

- Do not crash.
- Show an error/info message in the V2 section.
- Show parser errors in a compact table or expander.
- Preserve raw response in an expander called `Raw Smart Suggestions v2 response`.
- Do not create approved suggestions.

If output is valid but unsafe/incomplete:

- Display normalized rows.
- Blocked rows should show `suggestion_status = blocked_insufficient_source`.
- High-risk rows should remain review-required.
- Unsupported factual target fields such as EAN or price should not become proposed factual updates.

## 9. Session State

Recommended session-state keys:

- `smart_suggestions_v2_sku`
- `smart_suggestions_v2_rows`
- `smart_suggestions_v2_errors`
- `smart_suggestions_v2_raw_response`
- `smart_suggestions_v2_is_valid_json`

V2 state should be scoped to the currently selected SKU. If the selected SKU changes, old rows should not be shown as if they belong to the new product.

## 10. Export Behavior for Phase 7

Phase 7 should add only an optional CSV download for the current V2 table if implementation remains small.

Do not change:

- existing V1 AI CSV export
- Excel Management Export
- product data exports
- approved-only improved-data export

Management Export integration should remain a later phase after the V2 runtime table is stable.

## 11. Exact Next Implementation Phase

### Smart Suggestions v2 - Phase 7: Experimental UI Wiring

Goal:

Add an experimental V2 section to the existing AI Suggestions tab that generates, parses, displays, and optionally downloads field-level Smart Suggestions for one selected product.

Allowed files:

- `app.py`
- optional `docs/commerce_readiness_ai_project_log.md`
- optional `docs/codex_task_backlog.md`
- optional `docs/current_context.md`
- optional `docs/project_status.md`

Do not modify:

- existing V1 behavior
- `src/product_data_copilot/ai/**` unless a small helper bug is discovered and covered by tests
- exports outside the optional V2 CSV download
- sample data
- requirements

Acceptance criteria:

- Existing V1 AI Suggestions still work.
- Missing-key fallback still works.
- V2 appears clearly as experimental.
- V2 uses the prompt adapter and parser helpers.
- V2 suggestions display as a table.
- Invalid JSON does not crash the app.
- All V2 rows remain review-required or blocked.
- Product data is not overwritten.
- No mass generation is added.

## 12. Manual Smoke Test Checklist

After Phase 7 implementation:

1. Start the app with `python -m streamlit run app.py`.
2. Confirm sample data loads.
3. Open the `AI Suggestions` tab.
4. Confirm V1 section still appears and current copy is unchanged.
5. Confirm V2 section appears below V1 and is labeled experimental.
6. Without `OPENAI_API_KEY`, confirm the app does not crash and shows a helpful disabled/fallback message.
7. With `OPENAI_API_KEY`, generate V2 suggestions for one product.
8. Confirm a field-level table appears.
9. Confirm `approval_status` is not approved by default.
10. Confirm blocked/unsafe rows are visible as review-required or blocked.
11. Confirm V1 CSV download still works.
12. If V2 CSV is included, confirm it downloads the current V2 rows only.
13. Confirm product data, scores, issues, review tasks, and Management Export still render.

## 13. Rollback Strategy

Keep Phase 7 as one small commit.

Rollback steps:

1. Revert the Phase 7 commit.
2. Run `python -m pytest`.
3. Run `python -m py_compile app.py`.
4. Start the app manually.
5. Confirm the original V1 AI Suggestions tab is restored.

Do not continue into export or approval workflow changes until Phase 7 is manually verified.

## 14. Not in Scope

Do not implement in Phase 7:

- approved-only improved product data export
- Management Export V2 sheet integration
- database persistence
- multi-user review state
- mass generation
- automatic write-back
- marketplace presets
- legal/compliance guarantees
- full UI redesign
