# Product Data Copilot - Master Product & Architecture Blueprint v1

## 1. Product Vision

Product Data Copilot should become a professional product-data review and improvement tool for e-commerce teams.

In simple language: the tool helps teams upload product data, understand what is missing or risky, receive safe AI-supported improvement suggestions, review every suggestion manually, and export cleaner product data for operational follow-up.

The product should not replace human review. It should make product data work faster, clearer, and safer.

## 2. Recommended Product Name Options

Current target name:

- Product Data Copilot

Other name options considered:

- Commerce Data Copilot
- Catalog Readiness AI
- Marketplace Readiness Copilot
- Product Data Review Assistant
- Catalog Quality Copilot
- Commerce Content Copilot

Recommended direction:

- Use **Product Data Copilot** as the forward-looking product name.
- Treat **Commerce Readiness AI** as the original MVP/project name during the transition.

## 3. Target Users and Business Use Cases

### Target Users

- Product Data Managers
- Marketplace Managers
- E-commerce Operations Teams
- Category Managers
- Content Managers
- Translation Teams
- Compliance or Quality Review Teams
- Small merchants preparing product files for marketplace upload

### Real Business Use Cases

- Review product data before marketplace upload.
- Detect missing required product fields.
- Identify products with weak titles, descriptions, or attributes.
- Find products missing translation fields.
- Flag safety-relevant products that need warning-note review.
- Create review tasks for operational teams.
- Generate draft content suggestions for human review.
- Export an Excel report for managers or product-data teams.
- Prepare product data for later PIM, marketplace, or shop-system workflows.

## 4. Core User Workflow

1. User opens the local tool.
2. User loads sample data or uploads a CSV/XLSX product file.
3. Tool validates and normalizes the input structure.
4. Tool runs product data checks.
5. User reviews dashboard metrics.
6. User reviews product readiness scores.
7. User inspects data quality issues.
8. Tool generates review tasks from detected issues.
9. User optionally requests AI suggestions for selected product fields.
10. AI suggestions are shown as draft recommendations with confidence, reason, and source fields.
11. User approves, rejects, or keeps suggestions pending.
12. User exports reports and, later, improved product data.

## 5. Long-Term Product Capabilities

Potential long-term capabilities:

- Rule-based product data checks
- Configurable rule catalog
- Marketplace-specific rule presets
- Product data readiness scoring
- Review task workflow
- AI-supported title, description, attribute, and translation suggestions
- Human approval workflow for every AI suggestion
- Export of original and improved product data
- Excel Management Export
- Audit trail for AI suggestions and approvals
- Saved review sessions
- Optional database persistence
- Product comparison across uploads
- Batch review workflow with safeguards
- User roles only if the product becomes multi-user
- Integrations with PIM or marketplace systems later

Important: these are long-term capabilities, not immediate MVP requirements.

## 6. AI Safety Rules

AI support must be designed as a controlled review assistant, not an autonomous product-data editor.

Rules:

- No invented facts.
- AI may only use provided source fields.
- Source fields must be shown for every suggestion.
- Confidence level must be provided for every suggestion.
- Reason must be provided for every suggestion.
- AI suggestions must never be auto-applied without user approval.
- Compliance or safety-related suggestions must include human review warnings.
- AI must not claim legal compliance.
- AI must not claim a product is safe, certified, or approved unless explicitly present in source data.
- AI must not generate missing technical attributes as facts.
- AI should say when source data is insufficient.

Recommended confidence values:

- High
- Medium
- Low

Recommended action statuses:

- Pending Review
- Approved
- Rejected
- Needs More Source Data

## 7. Suggested Data Model for AI Suggestions

Suggested fields:

| Field | Purpose |
| --- | --- |
| `sku` | Product identifier. |
| `field_name` | Product field being improved, such as `product_name`, `description`, or `translation_de`. |
| `original_value` | Current value from the product data. |
| `suggested_value` | AI-generated draft suggestion. |
| `source_fields` | Source fields used to create the suggestion. |
| `confidence` | Confidence level: High, Medium, or Low. |
| `reason` | Explanation for why the suggestion was made. |
| `action_status` | Human review status, such as Pending Review, Approved, or Rejected. |

Example:

```text
sku: ELC-004
field_name: description
original_value: Qi-compatible wireless charging pad for smartphones and earbuds.
suggested_value: Compact Qi-compatible wireless charging pad for smartphones and earbuds, designed for everyday desk or bedside charging.
source_fields: product_name, category, description, attributes
confidence: Medium
reason: Suggestion only expands the existing description using available source data.
action_status: Pending Review
```

## 8. Professional Target Architecture

Recommended package structure:

```text
commerce-readiness-ai/
  pyproject.toml
  README.md
  requirements.txt
  data/
    sample_products.csv
  src/
    product_data_copilot/
      __init__.py
      models.py
      config.py
      logging_config.py
      io/
        readers.py
        writers.py
      rules/
        base.py
        core_rules.py
        marketplace_rules.py
        translation_rules.py
        compliance_rules.py
        media_rules.py
        engine.py
      scoring/
        scoring_service.py
      review/
        review_service.py
      ai/
        prompt_builder.py
        ai_service.py
      export/
        csv_exporter.py
        excel_exporter.py
      ui/
        streamlit_app.py
        tkinter_app.py
        tkinter_views.py
  tests/
    test_rules.py
    test_scoring.py
    test_review_tasks.py
    test_io.py
  docs/
    ...
```

### Architecture Principles

- UI should not contain business logic.
- Rule checks should be testable without Streamlit.
- Scoring should be testable without Streamlit.
- Exports should be testable without Streamlit.
- AI prompt building should be separate from the UI.
- Services should return structured data, not directly write to UI.
- Keep early abstractions small and understandable.
- Avoid building enterprise architecture before there is a real need.

### Suggested Module Responsibilities

`models.py`

- Product
- Issue
- ReadinessScore
- ReviewTask
- AiSuggestion
- AuditResult

`io/readers.py`

- Load CSV
- Load XLSX
- Validate expected columns
- Normalize missing optional fields

`rules/`

- Product data validation rules
- Rule engine that returns issues

`scoring/scoring_service.py`

- Calculate sub-scores
- Calculate weighted overall score
- Assign readiness status

`review/review_service.py`

- Create review tasks
- Assign task priority
- Assign review status
- Handle manual review status state later

`ai/`

- Build prompts
- Call OpenAI only when configured
- Parse structured AI suggestions
- Enforce safety rules

`export/`

- CSV export
- Excel Management Export
- Later: improved product data export

`ui/`

- Streamlit interface now
- Tkinter desktop interface later, if still needed

## 9. Refactor Roadmap in Safe Phases

### Phase 1: Architecture Plan and Tests

- Keep current app working.
- Add target architecture documentation.
- Add pytest and first tests for utility functions.
- Do not move UI yet.

### Phase 2: Extract Pure Utility and Validation Logic

- Move basic validators into `src/product_data_copilot/rules/` or `validators.py`.
- Add tests for EAN, price, image URL, generic title, and attributes.
- Keep Streamlit behavior unchanged.

### Phase 3: Extract Rule Engine

- Move product issue detection into rules modules.
- Introduce small rule functions or rule classes.
- Keep output structure compatible with current app.
- Add tests for issue detection.

### Phase 4: Extract Scoring and Review Services

- Move score calculation into `scoring_service.py`.
- Move review task creation into `review_service.py`.
- Add tests for score ranges, statuses, and task mappings.

### Phase 5: Extract Export and AI Services

- Move Excel/CSV export into `export/`.
- Move prompt building and AI response parsing into `ai/`.
- Keep OpenAI calls optional and safe.
- Add tests for export structure and prompt safety where practical.

### Phase 6: Shrink Streamlit App

- Streamlit app becomes a UI layer that calls services.
- `app.py` should become a small entrypoint or wrapper.
- Main UI file can live in `src/product_data_copilot/ui/streamlit_app.py`.

### Phase 7: Desktop UI Exploration

- Only after core logic is modular and tested.
- Evaluate whether Tkinter adds real value over Streamlit.
- If yes, build a small Tkinter prototype using the same services.

### Phase 8: Packaging

- Add `pyproject.toml`.
- Define package metadata.
- Add development dependencies.
- Consider CLI entrypoints later.

## 10. Testing Strategy with Pytest

Recommended test areas:

- Validators:
  - valid EAN
  - invalid EAN
  - valid price
  - invalid price
  - suspicious image URL
- Rules:
  - missing product name creates Critical issue
  - invalid EAN creates Critical issue
  - missing translation creates Warning issue
  - safety category without warning notes creates Warning issue
- Scoring:
  - scores stay between 0 and 100
  - clean product gets high score
  - product with missing required fields gets lower score
- Review tasks:
  - Critical issue maps to High priority
  - missing translation maps to Translation task
  - suspicious image URL maps to Media Improvement task
- Exports:
  - Management Export contains expected sheet names
  - empty issues/tasks do not crash export
- AI:
  - prompt includes source fields
  - prompt includes human review requirement
  - missing API key does not crash service

Recommended first tests:

- `test_validators.py`
- `test_rules.py`
- `test_scoring.py`
- `test_review_tasks.py`

## 11. Tooling Strategy

### Now

- Keep `requirements.txt` for simple local setup.
- Add `pytest` when automated tests are introduced.
- Add tests gradually.

### Next

- Add `pyproject.toml`.
- Move source code to `src/product_data_copilot/`.
- Use pytest test discovery.

### Later

- Add `ruff` for linting and formatting.
- Add type hints more consistently.
- Consider `mypy` only if type discipline becomes useful.
- Consider `pre-commit` only after the project structure stabilizes.

Do not add tooling just to look professional. Add it when it improves maintainability.

## 12. UX Strategy

The UX should guide users through a review workflow:

1. Load data
2. Review dashboard
3. Inspect product data
4. Review issues
5. Review scores
6. Work through review tasks
7. Generate AI suggestions where useful
8. Approve or reject suggestions
9. Export report or improved data

UX principles:

- Keep statuses clear.
- Separate detected issues from review decisions.
- Never hide original source data.
- Show why a product has a low score.
- Show why an AI suggestion was made.
- Require review before export of improved values.
- Avoid overwhelming users with too many rule settings too early.

Suggested statuses:

- Ready for Export
- Needs Review
- Missing Data
- Translation Missing
- Compliance Check Required
- AI Suggestion Created
- Approved
- Rejected

## 13. What Should Not Be Built Yet

Do not build yet:

- Database
- Login
- User roles
- SaaS backend
- Billing
- Deployment pipeline
- Shopware integration
- Shopify integration
- Plentymarkets integration
- Marketplace-specific rule presets
- Full desktop rewrite
- Tkinter drag-and-drop production UI
- Automatic mass AI generation
- Automatic write-back to product data
- Legal compliance guarantees
- Complex rule configuration UI
- Large plugin architecture

These can be considered later only after the modular core is stable.

## 14. Risks and How to Avoid Overengineering

### Risk: Too much architecture too early

Avoid by extracting current logic step by step and keeping behavior unchanged.

### Risk: Tkinter rewrite distracts from core quality

Avoid by modularizing and testing the core first. Build Tkinter only if it clearly improves the product.

### Risk: Rule engine becomes too abstract

Avoid by starting with simple rule functions or small rule classes. Do not build a generic enterprise rules platform.

### Risk: AI suggestions create unsafe product data

Avoid by requiring source fields, confidence, reasons, and manual approval.

### Risk: Portfolio project becomes too large to explain

Avoid by keeping a clear MVP story: product data audit, readiness scoring, review tasks, safe AI suggestions, exports.

### Risk: Tests are added after architecture changes

Avoid by adding first tests before major refactoring.

## 15. Definition of Portfolio-Ready and Almost Sellable

### Portfolio-Ready

The project is portfolio-ready when:

- The app runs locally.
- README explains the problem, setup, features, and scope.
- Sample data demonstrates the workflow.
- Requirements and acceptance criteria are documented.
- Demo checklist and testing notes exist.
- No secrets are committed.
- Code is not perfect, but the next architecture direction is clearly documented.
- Screenshots are available or planned.

Current status: mostly portfolio-ready.

### Almost Sellable

The product becomes almost sellable when:

- Core logic is modularized into services.
- Important logic is covered by tests.
- AI suggestions use the structured suggestion model.
- Users can approve/reject suggestions.
- Export can include approved improved data.
- Errors are handled consistently.
- Excel output is polished enough for business users.
- The tool can process realistic customer files reliably.
- Security and secret handling are documented and verified.

Current status: not almost sellable yet, but the path is clear.

## Recommended Next Step

Do not start with Tkinter.

Start with:

1. Add lightweight pytest tests for current validators and scoring.
2. Extract pure validation/rule logic from `app.py`.
3. Keep Streamlit as the UI until the core is modular.

Only after the core is clean and tested should a Tkinter desktop UI be considered.
