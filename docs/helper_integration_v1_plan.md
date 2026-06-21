# Helper Integration v1 Plan

## 1. Goal

Helper Integration v1 should wire already extracted, tested helper modules into `app.py` step by step without changing behavior.

This is a planning document only. It does not authorize immediate code integration. The next implementation blocks should each be small, reversible, and focused on one helper area at a time.

## 2. Current `app.py` Logic Map

`app.py` is still the Streamlit entrypoint and main app orchestration file. It currently contains these logic groups:

- Setup and configuration:
  - imports
  - `SRC_PATH` setup
  - `.env` loading
  - Streamlit page setup through existing UI helpers
- Constants:
  - `REVIEW_STATUS_OPTIONS`
  - `AI_SUGGESTION_TYPES`
- Validation helpers:
  - `is_blank`
  - `normalize_text`
  - `is_valid_ean`
  - `is_valid_price`
  - `is_suspicious_image_url`
  - `is_generic_product_name`
  - `has_useful_attributes`
  - `is_safety_relevant_category`
- Product issue generation:
  - `add_issue`
  - `add_core_data_checks`
  - `add_marketplace_checks`
  - `add_content_quality_checks`
  - `add_translation_checks`
  - `add_compliance_checks`
  - `add_media_checks`
  - `find_product_issues`
- Scoring:
  - `get_readiness_status`
  - `score_from_checks`
  - `calculate_product_scores`
  - `calculate_readiness_scores`
- Review workflow:
  - `get_review_status`
  - `apply_manual_review_overrides`
  - `get_task_type`
  - `get_task_priority`
  - `create_review_tasks`
  - `get_filter_options`
  - `filter_review_tasks`
- AI suggestions:
  - `get_product_option`
  - `get_ai_product_context`
  - `build_ai_prompt`
  - `generate_ai_suggestions`
  - `suggestions_to_dataframe`
- Export:
  - `create_management_summary`
  - `get_ai_suggestions_export_dataframe`
  - `create_excel_management_export`
- UI orchestration:
  - `run_app`
  - tab layout
  - dashboard metrics
  - dataframes
  - filters
  - download buttons
  - manual status override UI

## 3. Already Available Helper Modules

The project already has these import-safe, tested modules:

- `src/product_data_copilot/rules/validators.py`
- `src/product_data_copilot/scoring/scoring_helpers.py`
- `src/product_data_copilot/review/review_helpers.py`
- `src/product_data_copilot/export/export_helpers.py`
- `src/product_data_copilot/ai/prompt_helpers.py`
- `src/product_data_copilot/ui/streamlit_layout.py`

The UI helpers are already wired into `app.py`. The other helper modules should be integrated only after behavior comparison.

## 4. Current Overlap Between `app.py` and Helpers

### Validators

Likely overlaps:

- `app.py:is_blank` overlaps `validators.is_blank`
- `app.py:normalize_text` overlaps `validators.normalize_text`
- `app.py:is_valid_ean` overlaps `validators.is_valid_ean`
- `app.py:is_valid_price` overlaps `validators.is_valid_price`
- `app.py:is_suspicious_image_url` overlaps `validators.is_suspicious_image_url`
- `app.py:is_generic_product_name` overlaps `validators.is_generic_product_name`
- `app.py:has_useful_attributes` overlaps `validators.has_useful_attributes`
- `app.py:is_safety_relevant_category` overlaps `validators.is_safety_relevant_category`

Notes:

- This is the safest first implementation phase.
- `app.py:is_blank` currently depends on `pandas.isna`; the extracted helper has custom NaN handling. Tests should confirm identical behavior for project-relevant values before replacing imports.

### Scoring

Likely overlaps:

- `app.py:get_readiness_status` overlaps `scoring_helpers.readiness_status_from_score`
- `app.py:score_from_checks` overlaps `scoring_helpers.score_from_checks`

Notes:

- `calculate_product_scores` and `calculate_readiness_scores` should stay in `app.py` during early integration because they combine product fields, issue context, and app-specific score columns.
- The helper `score_from_checks` clamps to 0-100, while the current app version returns a rounded ratio. This should be behavior-compatible for normal boolean check lists, but it must be tested before replacement.

### Review

Likely overlaps:

- `app.py:get_review_status` overlaps `review_helpers.derive_review_status`
- `app.py:get_task_type` overlaps `review_helpers.issue_to_task_type`
- `app.py:get_task_priority` overlaps `review_helpers.severity_to_task_priority`
- `REVIEW_STATUS_OPTIONS` overlaps `review_helpers.ALLOWED_REVIEW_STATUSES`

Notes:

- This phase is safe only after validators and scoring are stable.
- Manual override behavior should remain in `app.py` because it depends on `st.session_state`.
- `create_review_tasks` should remain in `app.py` until review helper integration is proven with regression tests.

### Export

Likely overlaps:

- management export filename and sheet names overlap `export_helpers` constants
- AI suggestion export column list overlaps `export_helpers.AI_SUGGESTIONS_EXPORT_COLUMNS`

Notes:

- `create_excel_management_export` should remain in `app.py` during v1 integration because it coordinates Streamlit download bytes, Pandas ExcelWriter, and current DataFrames.
- Only constants and small validation helpers should be integrated first.

### AI Prompt

Likely overlaps:

- `build_ai_prompt` contains safety instructions that overlap `prompt_helpers.build_safe_prompt_instructions`
- `get_ai_product_context` overlaps `prompt_helpers.build_product_context_snippet`

Notes:

- This is higher risk because prompt wording changes can change AI behavior.
- Do not alter prompt text in the first AI integration phase unless tests lock the expected text.
- OpenAI API calls must stay in `app.py` for now.

## 5. Safest Integration Order

Recommended order:

1. Validators integration only
2. Scoring helper integration only
3. Review helper integration only
4. Export helper integration only
5. AI prompt helper integration planning or narrow integration only

Reason:

- Validators are small, pure, and used by product checks and scoring.
- Scoring helpers are pure but affect visible readiness scores.
- Review helpers affect task labels and review status.
- Export helpers affect generated business artifacts.
- AI prompt helpers affect generated text behavior and should be integrated last.

## 6. Recommended Future Phases

### Phase 1: Validators Integration

Status: Completed.

Goal:

- Replace duplicated validation helper bodies in `app.py` with imports from `rules/validators.py`.

Result:

- Integrated these validator helpers into `app.py`:
  - `is_blank`
  - `is_valid_ean`
  - `is_valid_price`
  - `is_suspicious_image_url`
  - `is_generic_product_name`
  - `has_useful_attributes`
  - `is_safety_relevant_category`
- Removed the corresponding duplicated inline helper implementations from `app.py`.
- Kept issue construction, check groups, issue names, severity labels, issue messages, scoring inputs, review tasks, AI behavior, and export behavior unchanged.
- Added validator test coverage for `pandas.NA` blank-value behavior.

Stayed inline:

- `get_value`, because it is app-specific row access logic.
- `make_display_safe`, because it is Streamlit display preparation, not product validation.
- issue generation and check-group functions, because they still belong to the current app orchestration.

Mismatch found:

- `app.py` treated `pandas.NA` as blank through `pandas.isna`, while the extracted validator did not.
- This was fixed in `rules/validators.py` before integration so existing blank-value behavior stays preserved.

Allowed future files:

- `app.py`
- `tests/test_validators.py`
- `docs/commerce_readiness_ai_project_log.md`
- `docs/codex_task_backlog.md`

Required tests:

- `python -m py_compile app.py`
- `python -m pytest`
- Add regression cases if `app.py` currently handles a value not covered in `tests/test_validators.py`

Manual checks:

- Sample data still produces issues.
- Missing/invalid EAN, invalid price, suspicious image URL, generic title, missing attributes, and safety category checks still appear as before.

Stop if:

- Any issue count changes without an explicit accepted reason.
- `pandas.NA`, empty strings, numeric EANs, or uploaded file edge cases behave differently.

### Phase 2: Scoring Helpers Integration

Status: Completed.

Goal:

- Replace `get_readiness_status` with `readiness_status_from_score`.
- Replace `score_from_checks` with `scoring_helpers.score_from_checks` only after confirming identical outputs for current score inputs.

Result:

- Integrated `readiness_status_from_score` into `app.py` as `get_readiness_status` to preserve existing call sites.
- Integrated `score_from_checks` from `scoring_helpers.py`.
- Removed the corresponding duplicated inline scoring helper implementations from `app.py`.
- Added test coverage for app-relevant rounded boolean check ratios.
- Kept `calculate_product_scores` and `calculate_readiness_scores` in `app.py`.

Stayed inline:

- weighted overall score formula
- individual sub-score calculation inputs
- readiness score DataFrame assembly
- review status derivation

Mismatch found:

- No mismatch found for current app usage. The helper functions are equivalent for the numeric readiness scores and boolean check lists used by `app.py`.

Allowed future files:

- `app.py`
- `tests/test_scoring_helpers.py`
- optional new regression test file if app-level expected scores are captured
- `docs/commerce_readiness_ai_project_log.md`
- `docs/codex_task_backlog.md`

Required tests:

- `python -m py_compile app.py`
- `python -m pytest`
- A sample-data score regression check is recommended before and after the change.

Manual checks:

- Dashboard average overall score remains sensible.
- Product Readiness Scores table still shows the same statuses and score ranges.

Stop if:

- Score values change unexpectedly.
- Readiness labels change unexpectedly.

### Phase 3: Review Helpers Integration

Status: Completed.

Goal:

- Replace task priority mapping with `severity_to_task_priority`.
- Replace task type mapping with `issue_to_task_type`.
- Consider replacing review status derivation with `derive_review_status` only after checking exact priority order.
- Consider importing `ALLOWED_REVIEW_STATUSES` for manual override options.

Result:

- Imported `ALLOWED_REVIEW_STATUSES` into `app.py` as `REVIEW_STATUS_OPTIONS` to preserve the existing UI variable name.
- Integrated `derive_review_status` through the existing `get_review_status(product_issues, readiness_status)` app wrapper.
- Integrated `issue_to_task_type` through the existing `get_task_type(issue)` app wrapper.
- Integrated `severity_to_task_priority` as `get_task_priority` to preserve existing call sites.
- Added test coverage for the manual review status option order used by the override UI.
- Kept `create_review_tasks` and manual review session state handling in `app.py`.

Stayed inline:

- `apply_manual_review_overrides`, because it depends on `st.session_state`.
- `create_review_tasks`, because it assembles the app-specific task DataFrame and joins against readiness scores.
- review task filtering helpers, because they are UI/dataframe filtering logic rather than pure review mapping.

Mismatch found:

- No mismatch found for current app usage. The helper functions match the app's review status priority, task type mapping, task priority mapping, and status option order.

Allowed future files:

- `app.py`
- `tests/test_review_helpers.py`
- optional review regression tests
- `docs/commerce_readiness_ai_project_log.md`
- `docs/codex_task_backlog.md`

Required tests:

- `python -m py_compile app.py`
- `python -m pytest`
- Review task type and priority regression coverage for the current sample issue types.

Manual checks:

- Review Tasks table still shows expected task types and priorities.
- Manual review status override still applies to scores and tasks.

Stop if:

- `review_status` priority changes.
- Manual override state keys change.
- Review task CSV output changes unexpectedly.

### Phase 4: Export Helpers Integration

Status: Completed.

Goal:

- Import export constants such as management export filename, sheet names, and AI suggestion export columns where they exactly match existing app behavior.
- Optionally use `ordered_columns` only if there is a clear existing column-ordering need.

Result:

- Imported `AI_SUGGESTIONS_EXPORT_COLUMNS` into `app.py` for empty AI Suggestions export DataFrame creation.
- Imported `MANAGEMENT_EXPORT_SHEETS` into `app.py` for management workbook sheet names.
- Imported `MANAGEMENT_EXPORT_FILENAME` into `app.py` for the Excel management download filename.
- Added test coverage to pin the management export filename, sheet order, and AI Suggestions export columns.
- Kept CSV download filenames, download labels, export DataFrame contents, and Excel writer orchestration unchanged.

Stayed inline:

- `create_management_summary`, because it calculates app-specific business metrics from current DataFrames.
- `get_ai_suggestions_export_dataframe`, because it reads `st.session_state`.
- `create_excel_management_export`, because it coordinates current app DataFrames and in-memory Excel bytes.
- CSV download filenames for readiness scores, issues, review tasks, and AI suggestions, because they are not currently helper constants.

Mismatch found:

- No mismatch found for current app usage. The helper constants match the existing management workbook filename, sheet names, and AI Suggestions export column order.

Allowed future files:

- `app.py`
- `tests/test_export_helpers.py`
- optional export regression tests
- `docs/commerce_readiness_ai_project_log.md`
- `docs/codex_task_backlog.md`

Required tests:

- `python -m py_compile app.py`
- `python -m pytest`
- Manual management export download and workbook sheet check.

Manual checks:

- Existing CSV downloads still work.
- Management Excel Export still creates the same expected sheets.
- AI Suggestions sheet still exists even when no suggestion was generated.

Stop if:

- Download filenames change unexpectedly.
- Sheet names change unexpectedly.
- Empty DataFrame handling changes.

### Phase 5: AI Prompt Helpers Integration

Status: Completed.

Goal:

- Plan or narrowly integrate prompt safety helpers without changing the generated prompt meaning.
- Only use helpers where text can be preserved or explicitly locked with tests.

Result:

- Integrated `do_not_invent_facts_instruction()` into `build_ai_prompt`.
- Integrated `human_review_instruction()` into `build_ai_prompt`.
- Added prompt-helper tests to lock down stronger anti-hallucination, source-field, compliance-claim, human-review, confidence, and reason wording.
- Kept OpenAI provider calls, model selection, API-key fallback, prompt preview UI, AI response parsing, session-state storage, and CSV export behavior unchanged.

Stayed inline:

- `get_ai_product_context`, because the helper context builder removes unknown/empty fields and does not include score/status context currently included by the app.
- `build_ai_prompt` structure, because the app's current selected suggestion types, issues, scores, and JSON output keys are app-specific.
- current JSON output schema keys, because `structured_suggestion_schema_description()` describes the future field-level suggestion model and does not match the current app output.
- `generate_ai_suggestions`, because it owns the OpenAI call and response parsing.
- `suggestions_to_dataframe`, because it maps the current app-specific suggestion payload to export columns.

Mismatch found:

- `build_safe_prompt_instructions()` includes confidence and reason requirements that are useful for the target product direction, but using it directly could change the current JSON output expectations.
- `build_product_context_snippet()` filters empty/unknown fields and omits current score/status context, so it was not integrated in this phase.
- `structured_suggestion_schema_description()` targets a future field-level suggestion schema and was not integrated into the current app prompt.

Allowed future files:

- `app.py`
- `tests/test_prompt_helpers.py`
- optional prompt snapshot/regression tests
- `docs/commerce_readiness_ai_project_log.md`
- `docs/codex_task_backlog.md`

Required tests:

- `python -m py_compile app.py`
- `python -m pytest`
- Prompt text regression test before changing prompt composition.

Manual checks:

- Missing API key fallback still appears.
- No OpenAI API call occurs without pressing the Generate button.
- Suggestions remain drafts and are not automatically applied.

Stop if:

- Prompt meaning changes unintentionally.
- OpenAI code would be called during import or tests.
- API key handling changes.

## 7. Behavior Preservation Strategy

Before each integration phase:

1. Identify the exact `app.py` functions being replaced.
2. Compare app behavior with helper behavior using existing tests.
3. Add missing helper tests before replacing app code.
4. Keep the old app function name as a thin wrapper if that reduces risk.
5. Run the full pytest suite.
6. Manually smoke-test the affected tab after code changes.

Recommended wrapper pattern for early phases:

```python
from product_data_copilot.rules.validators import is_valid_ean
```

Avoid changing call sites and business functions in the same commit. First replace imports or helper bodies, then test.

## 8. Rollback Strategy

Each integration phase should be one commit.

If behavior changes unexpectedly:

1. Stop immediately.
2. Do not continue into another helper group.
3. Run `git status`.
4. Revert only the latest integration commit.
5. Rerun:

```bash
python -m py_compile app.py
python -m pytest
```

6. Manually start the app with:

```bash
python -m streamlit run app.py
```

## 9. Risks / No-Go Areas

Main risks:

- Helper functions may look equivalent but differ subtly on `NaN`, numeric strings, or uploaded file values.
- Score helper changes could change visible readiness scores.
- Review helper changes could change task priorities or manual override expectations.
- Export helper changes could change filenames, sheet names, or column order.
- AI prompt helper changes could alter AI output behavior.

No-go areas during Helper Integration v1:

- Do not change rule definitions or issue messages.
- Do not change scoring weights.
- Do not change review status priority.
- Do not change manual override session state keys.
- Do not change AI prompt intent or API call behavior.
- Do not change export filenames or sheet names unless explicitly requested.
- Do not split Streamlit tabs.
- Do not create `streamlit_app.py`.
- Do not add new features.

## 10. Explicit Not In Scope

Helper Integration v1 does not include:

- new product checks
- new scoring logic
- UI redesign
- marketplace presets
- database
- login or user roles
- SaaS backend
- Shopware, Shopify, or Plentymarkets integrations
- Tkinter UI
- desktop drag-and-drop
- automatic mass AI generation
- automatic acceptance or write-back of AI suggestions
- legal compliance guarantees

## 11. Definition of Done for Helper Integration v1

Helper Integration v1 is complete when:

- already tested helpers are used by `app.py` where behavior is confirmed equivalent
- `app.py` is smaller and less duplicated
- all existing Streamlit user workflows still work
- pytest passes
- manual smoke test passes
- project log and backlog are updated
- no forbidden product scope was added

The immediate next block should be:

`Helper Integration v1 - Phase 1: Validators`
