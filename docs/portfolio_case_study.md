# Product Data Copilot - Portfolio Case Study

Product Data Copilot is a portfolio-grade product prototype for e-commerce product data audits. It is a local Streamlit MVP that helps teams inspect product files, detect data quality issues, calculate readiness scores, create review tasks, generate safe AI draft suggestions, and export review-ready workbooks.

The project is not positioned as a finished SaaS platform. It is a realistic local product workflow that demonstrates product thinking, professional Python structure, AI safety design, and practical e-commerce data operations.

## 1. Short Product Summary

Product Data Copilot turns CSV/XLSX product data into a structured audit workflow. Users can load sample data or upload their own product file, review detected issues, compare readiness scores, work through review tasks, generate AI-assisted draft suggestions for selected products, and export results for business handoff.

The core design principle is safety before automation. AI suggestions are draft recommendations, human approval is required, approved suggestions are export candidates only, and original product data is never overwritten automatically.

## 2. Problem Statement

E-commerce teams often prepare product data through spreadsheets, supplier files, PIM exports, marketplace templates, and manual review processes. Before publishing products, teams need to know whether product information is complete, understandable, safe, and ready for marketplace or shop usage.

Common operational problems include:

- Missing product names, descriptions, categories, brands, manufacturers, or attributes
- Missing or invalid EAN/GTIN values
- Weak or generic product titles
- Short product descriptions
- Missing translations
- Missing or suspicious image URLs
- Missing warning notes for safety-relevant categories
- No clear prioritization of which product rows need work first
- Spreadsheet-heavy handoff between operations, content, translation, and management teams

Without a structured audit workflow, teams spend too much time manually scanning rows and too little time fixing the most important issues.

## 3. Target Users

Product Data Copilot is designed for teams that work with product data before publication or marketplace submission:

- Product Data Managers who need to identify missing or invalid product fields.
- Marketplace Managers who need to understand whether product listings are ready for review.
- E-commerce Operations Teams who need a repeatable quality-control workflow.
- Category Managers who need a business-friendly overview of product readiness.
- Content and Translation Teams who need prioritized improvement tasks.
- Recruiters or technical reviewers who want to see a practical, documented, testable AI-assisted workflow.

## 4. Product Idea

The product idea is simple: turn a product spreadsheet into an actionable audit, review, and export workflow.

Instead of only displaying rows, Product Data Copilot adds structure around the work:

1. Load product data from a sample file, CSV, or Excel file.
2. Detect rule-based data quality issues.
3. Calculate readiness scores that explain where a product is strong or weak.
4. Convert issues into review tasks.
5. Use AI carefully to draft field-level suggestions when useful.
6. Require human review before anything becomes an export candidate.
7. Export management and improvement workbooks without changing the source data.

This keeps the workflow realistic for business users while showing engineering discipline around safety and scope.

## 5. Key Workflows

### Upload and Sample Data

The app starts with a built-in sample product dataset so the workflow is immediately demoable. Users can also upload CSV or XLSX product files.

The sample dataset includes realistic product categories and intentional quality issues, so the dashboard, issue detection, review tasks, and export flows are meaningful without external setup.

### Product Data Checks

The app checks product rows for common e-commerce data quality issues, including missing names, short descriptions, missing categories, missing or invalid EAN values, invalid prices, missing attributes, missing translations, suspicious image URLs, and missing warning notes for safety-relevant categories.

Each issue is represented with a stable structure:

- `sku`
- `issue_type`
- `field_name`
- `severity`
- `message`
- `recommended_action`

This makes the output understandable for both UI display and exports.

### Readiness Scoring

Product Data Copilot calculates multiple explainable readiness scores:

- `data_quality_score`
- `marketplace_readiness_score`
- `translation_readiness_score`
- `compliance_readiness_score`
- `ai_content_readiness_score`
- `overall_readiness_score`

The goal is not to create a black-box score. The score helps users quickly compare products while still being able to inspect the issues behind the result.

### Issues and Review Tasks

Detected issues are shown in an Issues table with severity filtering. The same issue data is used to generate Review Tasks with task types, priorities, recommended actions, and review statuses.

This moves the workflow from "what is wrong?" to "what should the team do next?"

### AI Suggestions and Smart Suggestions v2

AI Suggestions v1 supports draft content suggestions for one selected product. If no `OPENAI_API_KEY` is configured, the app shows a safe fallback instead of crashing.

Smart Suggestions v2 adds a more structured experimental model for field-level suggestions. It uses schema-driven output, parser normalization, source fields, reasons, confidence/risk information, and safe statuses. A deterministic demo fixture lets the review workflow be tested without an API key.

AI suggestions remain draft recommendations. They are not applied automatically.

### Human Approval

Smart Suggestions v2 includes a session-only human review workflow. Users can review one suggestion at a time and mark it as approved or rejected. Blocked suggestions cannot be approved.

Important boundaries:

- AI cannot approve itself.
- Approval is session-only in the current MVP.
- Approved suggestions are export candidates only.
- Product source data is not changed.

### Improved Excel Export

The improved export workflow groups Smart Suggestions v2 records into approved, pending, rejected, blocked, and unknown categories. The Excel download includes an original source snapshot so reviewers can compare improvement candidates against unchanged source data.

The export is a business handoff artifact, not an automatic data update.

## 6. Architecture Overview

Product Data Copilot started as a Streamlit MVP and has been gradually structured into smaller, testable helper modules.

High-level structure:

- `app.py` remains the Streamlit runtime and main app flow.
- `src/product_data_copilot/rules/` contains validation-oriented helpers.
- `src/product_data_copilot/scoring/` contains scoring helpers.
- `src/product_data_copilot/review/` contains review status and task mapping helpers.
- `src/product_data_copilot/export/` contains export preparation helpers.
- `src/product_data_copilot/ai/` contains prompt, schema, parser, and Smart Suggestions v2 helpers.
- `src/product_data_copilot/ui/` contains small Streamlit presentation helpers.
- `tests/` contains pytest coverage for pure helper logic.
- `docs/` contains planning, QA, project status, workflow, and portfolio documentation.

The architecture is intentionally pragmatic. The app is still local-first and Streamlit-based, but core helper logic has been extracted where it can be tested safely without launching the UI.

## 7. AI Safety Design

The AI design follows a human-in-the-loop approach.

Safety principles:

- No invented facts policy: AI should work from available source fields.
- Source fields are required for structured suggestions.
- Reasons and confidence/risk indicators are visible to the user.
- Parser normalization prevents unsafe AI-supplied statuses from becoming approved automatically.
- Blocked suggestions remain non-approvable.
- Users must review suggestions before they become export candidates.
- Approved suggestions do not update product data automatically.
- Missing API keys and failed AI calls are handled safely.

This is especially important because product data can affect marketplace publication, customer expectations, legal wording, and brand quality.

## 8. Export Safety

Export safety is a central design choice.

The improved export workflow separates:

- Source product data
- Proposed AI suggestions
- Approved improvements
- Rejected suggestions
- Blocked suggestions
- Unknown or unsupported suggestion states

The Excel workbook can include:

- Export Summary
- Approved Improvements
- Pending Suggestions
- Rejected Suggestions
- Blocked Suggestions
- Unknown Suggestions
- Original Source Snapshot

Approved suggestions are prepared as export candidates only. The original uploaded data remains unchanged, and the app does not write changes back to the source file.

## 9. Testing and Quality

The project includes automated tests and manual QA documentation.

Quality practices include:

- Pytest coverage for pure helper modules.
- Tests for validators, scoring helpers, review helpers, export helpers, AI prompt helpers, Smart Suggestions v2 schema/parser behavior, and export preparation.
- Deterministic Smart Suggestions v2 fixture data for testing approval states without an API key.
- Manual QA checklists for demo flow, UX clarity, improved export behavior, and AI approval workflows.
- Project logs and task backlog documents that track decisions and completed blocks.
- Scope boundaries that prevent the MVP from drifting into SaaS, database, integrations, or automatic AI write-back too early.

Current known test state from the project status is `122` passing pytest tests.

## 10. Current Limitations

The project is intentionally not presented as a finished enterprise platform.

Current limitations:

- It is not a SaaS product.
- There is no production database.
- There are no user accounts, login, roles, or multi-user workflows.
- Marketplace integrations are not implemented.
- Marketplace-specific rule presets are not implemented.
- Smart Suggestions v2 approval state is session-only.
- AI suggestions require human review.
- AI correctness is not guaranteed.
- There is no automatic product data write-back.
- There is no legal compliance guarantee.

These limitations are deliberate for the current local MVP. They keep the project focused, reviewable, and safe.

## 11. Roadmap / Next Steps

Near-term portfolio steps:

1. Capture final screenshots for the case study.
2. Add screenshot captions and visual references.
3. Link the case study from the README if useful.
4. Run a full manual demo QA pass.

Potential product improvements:

1. Expand pytest coverage around key business rules.
2. Improve Excel workbook formatting and column sizing.
3. Improve Smart Suggestions v2 result review UX after manual testing.
4. Add optional persistence only after the session workflow is proven useful.
5. Plan marketplace presets only after the generic rule workflow is stable.
6. Keep integrations and production deployment as later productization work.

## 12. Screenshots To Capture Later

Screenshots should be added after final manual UI QA.

Suggested placeholders:

- TODO: Landing / upload area - show product name, local workflow, and sample/upload path.
- TODO: Dashboard - show management-level readiness metrics.
- TODO: Readiness Scores - show explainable product-level scores.
- TODO: Issues Table - show rule-based product data problems and severity.
- TODO: Review Tasks - show operational task prioritization.
- TODO: AI Suggestions v1 - show draft AI support and safe API-key fallback or generated result.
- TODO: Smart Suggestions v2 - show structured field-level suggestions.
- TODO: Human Approval UI - show pending, approved, rejected, and blocked review states.
- TODO: Improved Product Data Export Preview - show approved/pending/rejected/blocked grouping.
- TODO: Excel Export Workbook - show workbook sheets and original source snapshot.

Each screenshot should include a short caption explaining what the viewer should notice and why it matters.

## 13. Summary

Product Data Copilot is a local, portfolio-ready product prototype that combines e-commerce data quality checks, readiness scoring, review tasks, AI-assisted draft suggestions, human approval, and safe exports.

The strongest part of the project is not only the feature list. It is the workflow discipline: rule-based checks before AI, human review before export, source data protection, tested helper modules, and clear documentation around limitations and next steps.
