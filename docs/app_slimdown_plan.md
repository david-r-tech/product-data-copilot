# App Slimdown v1 Plan

## 1. Goal

`app.py` is still the Streamlit entrypoint and currently contains the full application. The goal of App Slimdown v1 is to make the app easier to maintain without changing Streamlit behavior, UI flow, scoring, checks, exports, AI behavior, or file upload behavior.

This plan is intentionally conservative. It prepares small implementation phases instead of moving everything at once.

## 2. Current `app.py` Responsibilities

Current `app.py` has about 1323 lines and mixes these responsibilities:

- Environment and app setup:
  - imports
  - `st.set_page_config`
  - `.env` loading
  - OpenAI client setup inside the AI call
- Constants:
  - review status options
  - AI suggestion type labels
- Data access and input:
  - default sample CSV loading
  - CSV/XLSX upload
  - row/column counting
- Validation and product rules:
  - blank value checks
  - EAN validation
  - price validation
  - generic title checks
  - issue generation helpers
  - grouped product data checks
- Scoring:
  - readiness status
  - product score calculation
  - weighted overall score
- Review workflow:
  - review status derivation
  - manual review overrides in `st.session_state`
  - review task generation
  - review task filters
- AI suggestions:
  - product context creation
  - prompt building
  - OpenAI API call
  - JSON response parsing
  - suggestion DataFrame creation
  - AI session state handling
- Export:
  - CSV downloads
  - management summary
  - Excel management export
  - AI suggestions export DataFrame
- Streamlit UI rendering:
  - sidebar upload
  - severity filter
  - tabs
  - dashboard
  - product data
  - scores
  - issues
  - review tasks
  - management export
  - AI suggestions

## 3. Existing Import-Safe Modules

The project already has tested helper modules:

- `src/product_data_copilot/rules/validators.py`
- `src/product_data_copilot/scoring/scoring_helpers.py`
- `src/product_data_copilot/review/review_helpers.py`
- `src/product_data_copilot/export/export_helpers.py`
- `src/product_data_copilot/ai/prompt_helpers.py`

These modules should be used gradually. Do not wire all of them into `app.py` in one large change.

## 4. Target UI Module

Later, the Streamlit runtime should live in:

- `src/product_data_copilot/ui/streamlit_app.py`

This module should eventually contain:

- `run_app()`
- Streamlit page configuration
- environment loading
- current app orchestration
- sidebar rendering
- tab rendering
- Streamlit session state handling
- calls into tested helper modules

## 5. What Should Stay in Root `app.py`

Longer term, root `app.py` may become a small Streamlit entrypoint:

- ensure `src/` is importable when running `python -m streamlit run app.py`
- import `run_app`
- call `run_app()`

For App Slimdown v1, this was intentionally not completed. Root `app.py` still contains the main app flow and business-sensitive orchestration so behavior stays stable.

## 6. What Should Not Be Moved Yet

Do not move or redesign these too early:

- individual tab renderers into many files
- OpenAI API call into a separate client module
- session state persistence logic
- Excel writer implementation
- file upload behavior
- sample data path handling
- Streamlit tab order or labels
- UI text
- AI prompt behavior
- scoring formulas
- product rule behavior

These areas should move only after the entrypoint wrapper is stable and manually checked.

## 7. Main Risk Areas

- `st.set_page_config` must still run before other Streamlit UI calls.
- `st.session_state` keys must stay unchanged:
  - `manual_review_status_overrides`
  - `ai_suggestions`
  - `ai_suggestions_sku`
- Running through `src/` imports may fail if `app.py` does not handle the local `src` path.
- Relative paths such as `data/sample_products.csv` must still work from the project root.
- Streamlit reruns can behave differently if side effects move into imported modules.
- Download buttons must still receive the same CSV bytes and Excel bytes.
- Missing `OPENAI_API_KEY` fallback must remain unchanged.
- AI Suggestions must not start making API calls during import.
- Tests cannot fully prove Streamlit runtime behavior; manual smoke checks remain required.

## 8. Rollback Strategy

Each phase should be one small commit.

If anything breaks:

1. Stop further changes.
2. Run `git status`.
3. Revert only the latest slimdown commit, for example:

```bash
git revert <commit_hash>
```

4. Confirm:

```bash
python -m py_compile app.py
python -m pytest
```

5. Start the app manually and validate the demo checklist before continuing.

## 9. Decision: Wrapper First, Not UI Section Split First

Decision: create a `run_app()` wrapper first.

Reason:

- It creates a professional app boundary.
- It keeps the Streamlit entrypoint simple.
- It allows later UI section splitting without changing the user workflow and module boundary at the same time.
- It is easier to rollback than splitting every tab at once.

Do not split the tab UI into many section files first. That would create too many moving parts before the entrypoint is stable.

## 10. Implementation Phases

### Phase 1: Create Streamlit Entrypoint Wrapper

Status: Completed as a safer in-file wrapper.

Goal:

- Add a minimal `run_app()` boundary inside root `app.py`.
- Keep behavior unchanged.
- Keep helper logic and main app orchestration in `app.py`.
- Preserve the existing local Streamlit start command.

Important:

- Preserve tab order.
- Preserve UI labels.
- Preserve session state keys.
- Preserve filenames.
- Preserve environment variable names.
- Preserve missing API key fallback.

Completed in Phase 1:

- Wrapped the existing Streamlit runtime in `run_app()` inside `app.py`.
- Did not create `src/product_data_copilot/ui/streamlit_app.py`.
- Did not move tab rendering, data loading, scoring, checks, review, AI, or export logic.

Checks:

```bash
python -m py_compile app.py
python -m pytest
git diff --name-only -- data/sample_products.csv requirements.txt
```

Manual checks:

- Start with `python -m streamlit run app.py`.
- Confirm sample data loads.
- Confirm tabs render in the same order.
- Confirm AI Suggestions missing-key fallback still appears.
- Confirm Management Export download button still renders.

### Phase 2: Extract Layout Setup Helpers

Status: Re-scoped and completed as a safer layout/setup helper extraction.

Completed in Phase 2:

- Added `src/product_data_copilot/ui/streamlit_layout.py`.
- Added import-safe helpers for page configuration, app intro, and sidebar input header.
- Updated `app.py` to call these helpers while keeping the main app flow in `app.py`.
- Added focused tests in `tests/test_streamlit_layout.py`.

Next safest recommendation:

- Continue with a small Phase 3 that extracts only data input / source notice presentation helpers.
- Do not split Streamlit tabs into separate files yet.
- Do not move business logic until each imported helper group has been checked against current app behavior.

### Phase 3: Extract Data Input UI Helpers

Status: Completed.

Completed in Phase 3:

- Added `render_data_input_section(st)` to render the sidebar upload widget and return the uploaded file.
- Added `render_data_source_notice(st, data_source)` to render the existing `Using: ...` data source message.
- Updated `app.py` to call those helpers while keeping CSV/XLSX parsing, sample data loading, validation, scoring, review, AI, export, and tab flow in `app.py`.
- Added focused tests in `tests/test_streamlit_layout.py`.

Next safest recommendation:

- Continue with a small Phase 4 that replaces duplicated pure helper logic with tested imports in small groups.
- Start with the lowest-risk helpers only.
- Do not split Streamlit tabs into files yet.
- Do not move data loading, product checks, scoring, review, AI, or export orchestration in the same phase.

### Phase 4: Extract Status Summary UI Helpers

Status: Completed.

Completed in Phase 4:

- Added presentation helpers for product data row/column summary.
- Added presentation helpers for issue count summary and issue empty states.
- Added presentation helpers for review task intro, count summary, and review task empty states.
- Updated `app.py` to call these helpers while keeping calculations, DataFrame logic, filters, review logic, AI, exports, and tab flow in `app.py`.
- Added focused tests in `tests/test_streamlit_layout.py`.

Next safest recommendation:

- Continue with a small Phase 5 finalization block.
- Review whether App Slimdown v1 has reached a safe stop point before any helper integration begins.
- Do not split Streamlit tabs into files yet.
- Do not move data loading, product checks, scoring, review, AI, or export orchestration in the same phase.

### Phase 5: Finalize App Slimdown v1

Status: Completed.

Goal:

- Confirm App Slimdown v1 has reached a safe stop point.
- Document what was safely extracted.
- Document what intentionally remains in `app.py`.
- Set the next roadmap step to Helper Integration v1 planning.

Completed through Phase 5:

- Root `app.py` now has a minimal `run_app()` boundary while still preserving the main app flow.
- `src/product_data_copilot/ui/streamlit_layout.py` contains small import-safe Streamlit presentation helpers.
- Extracted UI helpers cover page setup, app intro, sidebar upload widget, data source notice, row/column summaries, issue summaries, issue empty states, review task intro, review task summaries, and review task empty states.
- `tests/test_streamlit_layout.py` covers the extracted UI helpers with fake Streamlit objects, without launching Streamlit.

Intentionally still in `app.py`:

- CSV/XLSX loading and parsing
- sample data fallback
- product data checks and issue generation
- scoring calculations
- review task generation
- manual review session state
- AI suggestion orchestration and API call handling
- CSV and Excel export orchestration
- tab layout and main Streamlit workflow

Reason:

- These areas are more behavior-sensitive than presentation helper extraction.
- Moving them should happen only after a dedicated Helper Integration v1 plan compares existing `app.py` behavior against the already extracted helper modules.

Next roadmap step:

- Start with `Helper Integration v1 - Planning`.
- Do not immediately wire all helper modules into `app.py`.
- Plan how validators, scoring helpers, review helpers, export helpers, and AI prompt helpers can be integrated one small group at a time without changing behavior.

Checks:

```bash
python -m py_compile app.py
python -m pytest
git diff --name-only -- data/sample_products.csv requirements.txt
```

Manual checks:

- Start with `python -m streamlit run app.py`.
- Confirm sample/upload flow still works.
- Confirm all tabs still appear.
- Confirm AI Suggestions missing-key fallback still appears.
- Confirm exports still render.
- Confirm review workflow still appears.

### Future Phase: Split Tab Rendering Into Local Functions

Goal:

- Inside `streamlit_app.py`, split each tab into a small render function:
  - `render_dashboard_tab`
  - `render_product_data_tab`
  - `render_scores_tab`
  - `render_issues_tab`
  - `render_review_tasks_tab`
  - `render_management_export_tab`
  - `render_ai_suggestions_tab`

Important:

- Keep these functions in `streamlit_app.py` at first.
- Do not create many UI files yet.
- Do not change tab labels or order.

Checks:

```bash
python -m py_compile app.py
python -m pytest
```

Manual checks:

- Walk through all tabs.
- Confirm filters still update tables.
- Confirm manual review override still works.
- Confirm AI Suggestions does not auto-apply changes.

### Future Phase: Consider UI Submodules Only If Needed

Goal:

- Only after Phase 6 is stable, consider moving larger tab renderers into `src/product_data_copilot/ui/sections/`.

Default recommendation:

- Do not do this unless `streamlit_app.py` is still too large after earlier phases.

## 11. Keeping Streamlit Behavior Unchanged

To preserve behavior:

- Keep the same `st.set_page_config` values.
- Keep the same default data path.
- Keep the same sidebar controls.
- Keep the same tab names and order.
- Keep the same metric labels.
- Keep the same download filenames.
- Keep the same session state keys.
- Keep the same OpenAI environment variable names.
- Keep missing API key behavior unchanged.
- Do not introduce caching during slimdown.
- Do not introduce new dependencies.
- Do not change scoring, rules, or prompt content during the UI move.

## 12. Required Checks After Every Slimdown Phase

Run:

```bash
python -m py_compile app.py
python -m pytest
git diff --name-only -- data/sample_products.csv requirements.txt
git status
```

Manual smoke test:

```bash
python -m streamlit run app.py
```

Then validate:

- sample data loads
- CSV/XLSX upload still works
- dashboard renders
- scores render
- issues render
- review tasks render
- manual review override works
- management export tab renders
- AI Suggestions missing-key fallback works
- no automatic AI write-back occurs

## 13. Non-Goals

Do not include in App Slimdown v1:

- new product features
- UI redesign
- database
- login
- SaaS backend
- marketplace integrations
- marketplace presets
- Tkinter UI
- desktop drag-and-drop
- automatic mass updates
- automatic AI suggestion approval
- legal compliance guarantees
