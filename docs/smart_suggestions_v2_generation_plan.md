# Smart Suggestions v2 - Controlled Runtime Generation Plan

## 1. Goal

Plan the next safe runtime step for Smart Suggestions v2: generate field-level V2 suggestions from OpenAI in a separate experimental flow while preserving AI Suggestions v1 exactly.

This is a planning document only. It does not implement the V2 OpenAI call.

## 2. Current State

The existing `AI Suggestions` tab now contains:

- the unchanged AI Suggestions v1 flow
- a separate `Smart Suggestions v2 (experimental)` section
- a V2 prompt preview built with `build_smart_suggestion_prompt(...)`
- an empty/schema-stable structured suggestions table

V2 currently does not call OpenAI and does not generate runtime suggestions.

## 3. Separate V2 Trigger

Phase 9 should add a separate button inside the V2 section:

`Generate Smart Suggestions v2`

Rules:

- Do not reuse the existing `Generate AI Suggestions` button.
- Do not change the existing V1 button, prompt, session state, or fallback behavior.
- The V2 button should only generate suggestions for the currently selected product.
- No batch generation.
- No automatic approval.
- No product-data write-back.

Recommended UI placement:

1. Existing V2 prompt preview.
2. Missing-key / readiness info.
3. `Generate Smart Suggestions v2` button.
4. Structured suggestions table.
5. Parser errors / raw response expander if needed.

## 4. API-Key and Fallback Pattern

Reuse the current V1 environment pattern:

- Load `OPENAI_API_KEY` from the environment or `.env`.
- Use `OPENAI_MODEL` with the same default model behavior as V1.
- If `OPENAI_API_KEY` is missing, show an info message and keep the prompt preview visible.
- Do not crash.
- Do not call OpenAI when the key is missing.

Recommended missing-key message:

`Smart Suggestions v2 generation is disabled because OPENAI_API_KEY is missing. The structured prompt preview is still available.`

Keep V1 fallback wording unchanged.

## 5. Prompt Construction

Use the existing V2 adapter:

```python
smart_suggestions_v2_prompt = build_smart_suggestion_prompt(
    selected_product_context,
    selected_issues.to_dict(orient="records"),
    selected_review_tasks.to_dict(orient="records"),
)
```

The prompt should use:

- selected product context
- selected product issues
- selected product review tasks
- the Smart Suggestions v2 schema contract
- anti-hallucination and human-review wording already included by the adapter

Do not add new prompt templates in `app.py` unless a very small wrapper is needed for readability.

## 6. Runtime Generation Flow

Recommended helper in `app.py` for Phase 9:

```python
def generate_smart_suggestions_v2(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    response = client.responses.create(model=model, input=prompt)
    return response.output_text.strip()
```

Then:

```python
raw_response = generate_smart_suggestions_v2(smart_suggestions_v2_prompt)
parsed_result = parse_and_normalize_suggestions(raw_response)
```

This keeps provider calling separate from parsing and makes rollback simple.

## 7. Parser and Safety Handling

Always pass the raw V2 response through:

`parse_and_normalize_suggestions(raw_response)`

Then use:

- `parsed_result["suggestions"]` for table rows
- `parsed_result["errors"]` for parser error display
- `parsed_result["is_valid_json"]` for user-facing status

Safety expectations:

- AI-supplied approved statuses are downgraded by the parser.
- Invalid JSON produces parser error records.
- Unsupported factual fields such as EAN or price become blocked or high-risk.
- Missing source fields or reasons become blocked.
- No row should be treated as approved by runtime UI.

## 8. Session State

Use separate V2 keys only:

- `smart_suggestions_v2_sku`
- `smart_suggestions_v2_rows`
- `smart_suggestions_v2_errors`
- `smart_suggestions_v2_raw_response`
- `smart_suggestions_v2_is_valid_json`

Do not modify:

- `ai_suggestions`
- `ai_suggestions_sku`

Display V2 rows only when:

`st.session_state["smart_suggestions_v2_sku"] == selected_sku`

This prevents showing old rows for a newly selected product.

## 9. Display Behavior

If generation succeeds and valid rows exist:

- Show rows in the existing V2 structured suggestions table.
- Keep `approval_status` and `suggestion_status` visible.
- Keep source fields visible.

If generation returns valid JSON but no suggestions:

- Show an info message that no structured suggestions were returned.

If JSON is invalid:

- Show a warning that the V2 response could not be parsed safely.
- Show parser error rows.
- Show raw response in an expander named `Raw Smart Suggestions v2 response`.
- Do not approve or apply anything.

If the OpenAI call fails:

- Show a Streamlit error:
  `Smart Suggestions v2 generation failed. Please check your API key, network connection, or model availability.`
- Put technical details in an expander.
- Do not print secrets.

## 10. No Auto-Approval or Write-Back

Phase 9 must not:

- add approval buttons
- edit source product data
- export improved product data
- update review tasks automatically
- change scores or issue detection
- add mass generation

All V2 records remain draft/review-required/blocked display data.

## 11. Exact Next Implementation Block

### Smart Suggestions v2 - Phase 9: Controlled Runtime Generation

Allowed files:

- `app.py`
- `docs/codex_task_backlog.md`
- `docs/commerce_readiness_ai_project_log.md`
- `docs/project_status.md`
- `docs/current_context.md`

Optional allowed test files only if a helper behavior bug is discovered:

- `tests/test_suggestion_parser.py`
- `tests/test_suggestion_prompt_adapter.py`

Forbidden files:

- `src/product_data_copilot/rules/**`
- `src/product_data_copilot/scoring/**`
- `src/product_data_copilot/review/**`
- `src/product_data_copilot/export/**`
- `src/product_data_copilot/ui/**`
- `requirements.txt`
- `data/sample_products.csv`

Acceptance criteria:

- Existing V1 AI Suggestions button and fallback still work.
- V2 has its own generate button.
- Missing API key disables V2 generation without crashing.
- With a key, V2 calls OpenAI only after the V2 button is clicked.
- V2 response is parsed through `parse_and_normalize_suggestions(...)`.
- V2 rows display in the structured table.
- Invalid/unsafe output is shown as blocked or needs review.
- No V2 row is auto-approved.
- No exports change.
- No source data changes.

## 12. Manual Smoke Test Checklist

After Phase 9 implementation:

1. Run `python -m streamlit run app.py`.
2. Open the `AI Suggestions` tab.
3. Confirm V1 text, controls, missing-key fallback, and CSV download still appear.
4. Confirm `Smart Suggestions v2 (experimental)` appears separately.
5. Without `OPENAI_API_KEY`, confirm V2 generation is disabled and prompt preview remains visible.
6. With `OPENAI_API_KEY`, click `Generate Smart Suggestions v2`.
7. Confirm a V2 structured table appears or a safe parser warning appears.
8. Confirm no row shows `approval_status = approved` unless a later human workflow explicitly supports that.
9. Confirm unsafe rows are `blocked_insufficient_source` or review-required.
10. Confirm product data, scores, issues, review tasks, Management Export, and V1 export still work.

## 13. Rollback Strategy

Keep Phase 9 as one focused commit.

Rollback:

1. Revert the Phase 9 commit.
2. Run `python -m pytest`.
3. Run `python -m py_compile app.py`.
4. Start Streamlit manually.
5. Confirm V1 AI Suggestions and the Phase 7 V2 prompt-preview section still work.

Stop after rollback if V1 behavior is uncertain.

## 14. Future Work After Phase 9

Do not jump directly into approval workflow.

Recommended sequence:

1. Manual smoke test with and without API key.
2. Review actual V2 response quality.
3. Add tests only if helper behavior needs hardening.
4. Plan V2 export/approval separately.
