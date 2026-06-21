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

After the first safe slimdown phase, root `app.py` should become a small Streamlit entrypoint:

- ensure `src/` is importable when running `python -m streamlit run app.py`
- import `run_app`
- call `run_app()`

Root `app.py` should not contain business logic after the entrypoint phase is complete.

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

Goal:

- Add `src/product_data_copilot/ui/__init__.py`.
- Add `src/product_data_copilot/ui/streamlit_app.py`.
- Move the current Streamlit app runtime into `run_app()`.
- Keep behavior unchanged.
- Keep helper logic together during the first move if needed.
- Make root `app.py` a thin launcher that imports and calls `run_app()`.

Important:

- Preserve tab order.
- Preserve UI labels.
- Preserve session state keys.
- Preserve filenames.
- Preserve environment variable names.
- Preserve missing API key fallback.

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

### Phase 2: Replace Duplicated Pure Helpers With Tested Imports

Goal:

- Replace duplicated validator helper logic in the UI module with imports from `rules/validators.py`.
- Replace simple scoring helper logic with imports from `scoring/scoring_helpers.py` where safe.
- Replace review mapping helpers with imports from `review/review_helpers.py` where safe.
- Replace export preparation constants/helpers with imports from `export/export_helpers.py` where safe.
- Replace AI prompt safety text helpers with imports from `ai/prompt_helpers.py` where safe.

Important:

- Do this in small groups.
- Do not change outputs.
- If a helper in `app.py` has slightly different behavior than the extracted helper, either keep the app behavior or add a test before changing it.

Checks:

```bash
python -m py_compile app.py
python -m pytest
git diff --name-only -- data/sample_products.csv requirements.txt
```

Manual checks:

- Product checks still create expected issues.
- Scores still appear.
- Review tasks still appear.
- Downloads still work.
- AI prompt preview still renders without API key.

### Phase 3: Split Tab Rendering Into Local Functions

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

### Phase 4: Consider UI Submodules Only If Needed

Goal:

- Only after Phase 3 is stable, consider moving larger tab renderers into `src/product_data_copilot/ui/sections/`.

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
