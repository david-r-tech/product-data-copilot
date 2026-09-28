# Product Data Copilot - Codebase Audit & Refactor Inventory v1

> Refactoring snapshot. Use [current_context.md](current_context.md) and [project_status.md](project_status.md) for the current release state, and verify line counts and locations against the present source before planning changes.

## 1. Current `app.py` Assessment

Current `app.py` size:

- Approximately 1,323 lines.
- One large Streamlit entrypoint currently contains UI rendering, data loading, validation rules, scoring, review workflow, AI prompting, exports, and session-state logic.

Main responsibilities currently mixed together:

- Streamlit page setup and tab rendering
- CSV/XLSX upload
- Sample data loading
- Product data validation helpers
- Product issue detection
- Readiness scoring
- Review status logic
- Review task generation
- Manual review status override via `st.session_state`
- AI prompt building
- OpenAI API call
- AI response parsing
- CSV export buttons
- Excel Management Export generation
- Display-safe dataframe conversion
- Environment variable loading with `.env`

Assessment:

- The app is functional as an MVP.
- The main technical weakness is that too many responsibilities live in one file.
- Future work should extract pure business logic first, then keep the UI as a thin layer.
- A full rewrite or UI replacement should not happen before core logic is tested and modularized.

## 2. Function / Logic Inventory

### Data Loading / Sample Data

Current logic:

- `pd.read_csv("data/sample_products.csv")`
- `pd.read_csv(uploaded_file)`
- `pd.read_excel(uploaded_file)`
- Streamlit file uploader
- `data_source` label
- `row_count`, `column_count`

Current location:

- Bottom execution section of `app.py`

Concerns:

- Data loading is directly tied to Streamlit upload state.
- No separate reader service exists yet.
- Schema handling is implicit through `get_value(...)`.

### Validation Checks / Product Rules

Current helper functions:

- `is_blank`
- `get_value`
- `normalize_text`
- `is_valid_ean`
- `is_valid_price`
- `is_suspicious_image_url`
- `is_generic_product_name`
- `has_useful_attributes`
- `add_issue`

Current rule groups:

- `add_core_data_checks`
- `add_marketplace_checks`
- `add_content_quality_checks`
- `add_translation_checks`
- `add_compliance_checks`
- `add_media_checks`
- `find_product_issues`
- `is_safety_relevant_category`

Current output:

- Pandas DataFrame with:
  - `sku`
  - `issue_type`
  - `field_name`
  - `severity`
  - `message`
  - `recommended_action`

Concerns:

- Rules are mostly pure enough to extract safely.
- Some helpers depend on Pandas behavior, especially `pd.isna`.
- Rules currently output dictionaries/DataFrames instead of typed domain objects.

### Scoring

Current functions:

- `get_readiness_status`
- `score_from_checks`
- `calculate_product_scores`
- `calculate_readiness_scores`

Current score outputs:

- `data_quality_score`
- `marketplace_readiness_score`
- `translation_readiness_score`
- `compliance_readiness_score`
- `ai_content_readiness_score`
- `overall_readiness_score`
- `readiness_status`
- `review_status`

Concerns:

- Scoring is mostly pure business logic and should be testable.
- It depends on helper functions such as `get_value`, `is_blank`, `is_valid_ean`, `is_valid_price`, `has_useful_attributes`, and `is_safety_relevant_category`.
- `calculate_readiness_scores` depends on issue data for review status.

### Issues Table

Current logic:

- `issues = find_product_issues(products)`
- severity counts:
  - Critical
  - Warning
  - Info
- `selected_severities`
- `filtered_issues`
- Streamlit rendering and CSV download

Concerns:

- Issue detection should move to rules.
- Issue filtering for UI can remain in UI or move to a small service later.
- CSV export should move to export layer.

### Review Tasks

Current functions:

- `get_task_type`
- `get_task_priority`
- `create_review_tasks`
- `filter_review_tasks`
- `get_filter_options`

Current review task fields:

- `sku`
- `product_name`
- `issue_type`
- `field_name`
- `task_type`
- `priority`
- `recommended_action`
- `review_status`

Concerns:

- Task mapping is business logic and should move to review service.
- Filter options are UI/helper logic and can move later.
- Review tasks depend on issues and readiness scores.

### Review Workflow / Session State

Current functions / logic:

- `apply_manual_review_overrides`
- Streamlit `st.session_state["manual_review_status_overrides"]`
- manual status selectbox
- save/clear override buttons
- `st.rerun()`

Concerns:

- This is tightly coupled to Streamlit.
- Session-state logic should not be moved first.
- Later architecture should separate review-status rules from UI-specific session storage.

### AI Suggestions

Current functions:

- `get_ai_product_context`
- `build_ai_prompt`
- `generate_ai_suggestions`
- `suggestions_to_dataframe`
- `get_ai_suggestions_export_dataframe`

Current UI/session logic:

- suggestion type multiselect
- missing API key fallback
- prompt preview
- OpenAI call through `OpenAI(api_key=os.getenv("OPENAI_API_KEY"))`
- model through `OPENAI_MODEL`
- `st.session_state["ai_suggestions"]`
- `st.session_state["ai_suggestions_sku"]`

Concerns:

- Prompt building can be extracted safely after tests.
- OpenAI call should be wrapped in an AI service.
- Session-state storage should remain in UI until a proper review/suggestion state model exists.
- Suggested future model should include confidence, source fields, reason, and action status.

### Export Logic

Current functions:

- `create_management_summary`
- `get_ai_suggestions_export_dataframe`
- `create_excel_management_export`
- direct CSV generation via `DataFrame.to_csv(...)`
- Streamlit download buttons

Current Excel sheets:

- Management Summary
- Product Scores
- Issues
- Review Tasks
- AI Suggestions
- Source Products

Concerns:

- Excel export generation is a good extraction candidate.
- Streamlit download buttons should stay in UI.
- Export functions should accept DataFrames or typed results and return bytes/string outputs.

### Streamlit UI Rendering

Current UI sections:

- Page config
- Sidebar input
- Severity filter
- Dashboard tab
- Product Data tab
- Scores tab
- Issues tab
- Review Tasks tab
- Management Export tab
- AI Suggestions tab

Concerns:

- UI rendering starts around the lower third of `app.py`.
- UI is currently coupled to data preparation and service execution.
- Long-term goal: UI calls services and renders results only.

### Config / Secrets / Env Handling

Current logic:

- `load_dotenv()`
- `os.getenv("OPENAI_API_KEY")`
- `os.getenv("OPENAI_MODEL", "gpt-4.1-mini")`

Concerns:

- Configuration should later move to `config.py`.
- Secrets should never be logged or displayed.
- AI service should handle missing key gracefully.

## 3. Refactor Target Mapping

| Current Category | Future Location | Notes |
| --- | --- | --- |
| CSV/XLSX loading | `src/product_data_copilot/io/readers.py` | Keep Streamlit upload object handling in UI; reader functions should handle file-like objects. |
| Sample data loading | `src/product_data_copilot/io/readers.py` | Reader can expose `load_sample_products(path)`. |
| Validation helpers | `src/product_data_copilot/rules/validators.py` | First safe extraction candidate. |
| Product rules | `src/product_data_copilot/rules/` | Split by core, marketplace, translation, compliance, media. |
| Rule orchestration | `src/product_data_copilot/rules/engine.py` | Should return issues in the same structure initially. |
| Readiness scoring | `src/product_data_copilot/scoring/scoring_service.py` | Extract after validators/rules are covered by tests. |
| Review status logic | `src/product_data_copilot/review/review_service.py` | Separate automatic review status from UI manual overrides. |
| Review tasks | `src/product_data_copilot/review/review_service.py` | Task type and priority mapping belong here. |
| AI prompt building | `src/product_data_copilot/ai/prompt_builder.py` | Can be tested without API calls. |
| OpenAI call wrapper | `src/product_data_copilot/ai/ai_service.py` | Keep optional and safe. |
| AI suggestion model | `src/product_data_copilot/models.py` | Later: add source fields, confidence, reason, action status. |
| CSV export | `src/product_data_copilot/export/csv_exporter.py` | Keep `st.download_button` in UI. |
| Excel export | `src/product_data_copilot/export/excel_exporter.py` | Good extraction candidate once export tests exist. |
| Display-safe dataframe helper | `src/product_data_copilot/ui/streamlit_helpers.py` | UI-specific helper. |
| Streamlit tabs/rendering | `src/product_data_copilot/ui/streamlit_app.py` | Move only after core services are extracted. |
| App entrypoint | `app.py` | Later becomes a small wrapper that imports and runs Streamlit UI. |
| Environment config | `src/product_data_copilot/config.py` | Centralize env names/default model. |

## 4. Risk Assessment

### Risky to Move First

- Streamlit UI rendering
- `st.session_state` manual review overrides
- AI suggestions session storage
- Streamlit download buttons
- Complete `app.py` relocation
- OpenAI API call behavior

Reason:

- These areas are coupled to Streamlit runtime behavior and user interaction.
- Moving them early risks breaking the working application.

### Safer to Move First

- `is_valid_ean`
- `is_valid_price`
- `is_suspicious_image_url`
- `is_generic_product_name`
- `has_useful_attributes`
- `is_safety_relevant_category`
- `get_readiness_status`
- `score_from_checks`
- `get_task_priority`
- `get_task_type`

Reason:

- These are small, mostly pure functions.
- They can be covered with lightweight tests before extraction.

### Likely Depends on Streamlit Session State

- `apply_manual_review_overrides`
- manual review status save/clear buttons
- `get_ai_suggestions_export_dataframe`
- AI suggestion display after generation
- selected product/suggestion UI state

### Should Be Tested Before Moving

- validators
- rule output shape
- scoring ranges
- readiness status thresholds
- review task type mapping
- review task priority mapping
- Excel workbook sheet names
- AI prompt safety text

## 5. Recommended Safe Refactor Order

### Step 1: Add Lightweight Tests

- Add pytest.
- Test validators and simple status functions first.
- Do not move code yet.

### Step 2: Extract Validators

- Move pure helpers to `src/product_data_copilot/rules/validators.py`.
- Update imports in `app.py`.
- Keep behavior unchanged.

### Step 3: Extract Review Task Mapping

- Move `get_task_type` and `get_task_priority`.
- Add tests for issue-to-task mapping.

### Step 4: Extract Scoring Logic

- Move scoring helpers and product score calculation.
- Add tests for score ranges and readiness thresholds.

### Step 5: Extract Rule Engine

- Move issue detection groups into rules modules.
- Keep issue DataFrame columns unchanged.
- Add tests for known sample rows or minimal product dictionaries.

### Step 6: Extract Export Logic

- Move management summary and Excel export generation.
- Add tests for expected sheet names.

### Step 7: Extract AI Prompt Builder

- Move prompt construction before moving OpenAI call.
- Add tests for required safety language and source fields.

### Step 8: Thin Streamlit UI

- Move UI to `src/product_data_copilot/ui/streamlit_app.py`.
- Keep root `app.py` as a small compatibility entrypoint.

## 6. First Test Candidates

Recommended first tests:

- `is_valid_ean("4006381333931")` returns `True`
- `is_valid_ean("12345")` returns `False`
- `is_valid_price("19.99")` returns `True`
- `is_valid_price("0")` returns `False`
- `is_suspicious_image_url("images/product.jpg")` returns `True`
- `is_suspicious_image_url("https://cdn.example.local/product.jpg")` returns `False` unless example-domain policy changes
- `get_readiness_status(90)` returns `Ready`
- `get_readiness_status(70)` returns `Needs Review`
- `get_readiness_status(40)` returns `Critical`
- `get_task_priority("Critical")` returns `High`
- `get_task_priority("Warning")` returns `Medium`
- `get_task_priority("Info")` returns `Low`
- invalid EAN issue maps to `Data Completion`
- missing attributes issue maps to `Attribute Enrichment`
- suspicious image URL issue maps to `Media Improvement`

After those pass, add tests for:

- `find_product_issues`
- `calculate_product_scores`
- `create_review_tasks`
- `create_excel_management_export`

## 7. Explicit Non-Goals

Do not implement in this refactor inventory block:

- Code refactor
- File moves
- New app features
- New tests
- Database
- Login
- SaaS backend
- Integrations
- Marketplace presets
- Tkinter UI
- Desktop drag-and-drop
- Automatic mass updates
- AI suggestion auto-apply
- Product data write-back
- New architecture files under `src/`

## 8. Summary Recommendation

The current `app.py` should be treated as a working MVP reference implementation.

The next technical step should not be a full rewrite. The safest next step is to add lightweight tests for pure logic, then extract validators and small mapping functions first. This creates a safety net before moving rules, scoring, exports, AI, and finally UI.
