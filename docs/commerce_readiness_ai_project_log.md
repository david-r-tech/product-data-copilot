# Commerce Readiness AI - Project Log

## 1. Project Overview

Commerce Readiness AI is a beginner-friendly Streamlit MVP for checking e-commerce product data quality.

The product is for merchants, marketplace operators, catalog managers, and e-commerce teams who need a quick way to review product data before publishing or improving listings.

It helps identify common product data problems such as missing names, weak descriptions, missing EANs, missing translations, missing images, and missing warning notes for safety-relevant products.

The current MVP goal is to provide a simple CSV/XLSX-based product readiness checker that can load product data, detect rule-based issues, show dashboard metrics, calculate readiness scores, support review tasks, and export results.

## 2. Current App Status

Currently implemented:

* Streamlit app
* Sample product data
* CSV upload
* Excel upload
* Product data table
* Data quality issue detection
* Product Data Checks v2
* Dashboard metrics
* Multiple product readiness scores
* Severity filter
* CSV export buttons
* Improved page layout with sidebar controls
* Product review status
* Review workflow with task filters, overview metrics, manual status overrides, and CSV export
* Excel management export
* Optional AI suggestions for one selected product
* GitHub-ready README and demo documentation
* Screenshot planning document

Completed major blocks:

* Initial Streamlit setup
* CSV and Excel upload
* Product Data Checks v2 - Step 1
* Multiple Readiness Scores v1
* Review Workflow v1
* AI Suggestions v1
* Excel Management Export v1
* Demo Dataset & Portfolio Polish v1
* Streamlit Compatibility & DataFrame Type Cleanup v1
* Final GitHub Readiness v1

## 3. Current File Structure

Important current files:

* `app.py` - Main Streamlit application.
* `requirements.txt` - Python package dependencies.
* `README.md` - Basic project overview and run instructions.
* `data/sample_products.csv` - Sample product dataset used when no CSV is uploaded.
* `.env.example` - Template for local environment variables.
* `start_app.bat` - Windows double-click launcher for the Streamlit app.
* `docs/commerce_readiness_ai_project_log.md` - Central project log and progress document.
* `docs/demo_test_checklist.md` - Manual demo and smoke-test checklist.
* `docs/demo_script.md` - Step-by-step demo walkthrough script.
* `docs/portfolio_case_study.md` - Portfolio case study draft.
* `docs/product_requirements.md` - Current product requirements, scope, and acceptance criteria.
* `docs/testing_notes.md` - Technical and manual verification notes.
* `docs/screenshots_to_capture.md` - Screenshot planning list for GitHub and portfolio use.

## 4. Current Data Columns

The current sample data uses these columns:

* `sku`
* `product_name`
* `category`
* `description`
* `brand`
* `ean`
* `language`
* `price`
* `image_url`
* `warning_notes`
* `translation_de`
* `translation_en`
* `manufacturer`
* `attributes`

## 5. Current Data Quality Checks

The app currently checks for:

* Missing `product_name`
* Short `product_name`
* Missing `description`
* Short `description`
* Missing `brand`
* Missing `ean`
* Invalid `ean`
* Missing `category`
* Missing or invalid `price`
* Missing `image_url`
* Suspicious `image_url`
* Missing `manufacturer`
* Missing `attributes`
* Missing `translation_de`
* Missing `translation_en`
* Missing `warning_notes` for safety-relevant categories

## 6. Current Scoring Logic

The app calculates multiple explainable readiness scores for each product:

* `data_quality_score` - Checks core data such as SKU, product name, description, brand, EAN, and category.
* `marketplace_readiness_score` - Checks marketplace listing fields such as product name, description, brand, EAN, image URL, and category.
* `translation_readiness_score` - Checks German and English translations.
* `compliance_readiness_score` - Checks warning notes for safety-relevant categories.
* `ai_content_readiness_score` - Checks whether basic content fields are present and whether the description is long enough.
* `overall_readiness_score` - Weighted score based on the score categories above.

Overall score weighting:

* 35% Data Quality
* 25% Marketplace Readiness
* 15% Translation Readiness
* 15% Compliance Readiness
* 10% AI Content Readiness

Readiness status logic:

* 85+ = Ready
* 60-84 = Needs Review
* Below 60 = Critical

## 7. Change Log

### Initial Streamlit Setup

* Date: TODO
* Change: Created the first working Streamlit app with `app.py`, `requirements.txt`, `README.md`, `.gitignore`, and initial sample data.
* Why it matters: Established the basic project foundation and made the app runnable.
* How to test: Run `python -m streamlit run app.py` and confirm the app opens.

### Sample CSV Data

* Date: TODO
* Change: Added `data/sample_products.csv` as the default dataset.
* Why it matters: Allows the app to show useful data immediately without requiring an upload.
* How to test: Start the app without uploading a file and confirm sample data appears.

### CSV Upload

* Date: TODO
* Change: Added a CSV file uploader.
* Why it matters: Allows users to analyze their own product data.
* How to test: Upload a CSV file and confirm the displayed product table changes.

### Realistic Demo Dataset

* Date: TODO
* Change: Replaced the starter dataset with a realistic e-commerce demo dataset and richer product columns.
* Why it matters: Provides better demo data and includes intentional data quality problems for testing.
* How to test: Start the app with no uploaded file and confirm the sample products and expected columns appear.

### Data Quality Checks

* Date: TODO
* Change: Added rule-based checks for missing and weak product data.
* Why it matters: Turns the app from a simple viewer into a useful product readiness checker.
* How to test: Start the app and confirm the Data Quality Issues table appears below the product table.

### Dashboard Metrics

* Date: TODO
* Change: Added metrics for total products, total issues, critical issues, warning issues, info issues, and products affected.
* Why it matters: Gives users a quick summary of catalog health.
* How to test: Start the app and confirm the Dashboard section is visible.

### Readiness Scoring

* Date: TODO
* Change: Added product-level readiness scores and readiness statuses.
* Why it matters: Helps users quickly identify which products are ready and which need review.
* How to test: Start the app and confirm the Product Readiness Scores table is visible.

### Severity Filter

* Date: TODO
* Change: Added a severity filter for Critical, Warning, and Info issues.
* Why it matters: Lets users focus on the issue types that matter most.
* How to test: Change the selected severities and confirm the displayed issue table updates.

### CSV Exports

* Date: TODO
* Change: Added CSV download buttons for product readiness scores and data quality issues.
* Why it matters: Allows users to save analysis results and share them outside the app.
* How to test: Click both download buttons and confirm the CSV files download.

### Layout Improvement

* Date: TODO
* Change: Improved the Streamlit layout with a wide page setting, sidebar controls for upload and issue filtering, clearer dashboard sections, dividers, captions, and full-width data tables.
* Why it matters: Makes the MVP easier to scan and more useful for reviewing product data, scores, and issues.
* How to test: Run `python -m streamlit run app.py` and confirm the upload/filter controls appear in the sidebar, dashboard metrics appear near the top, and the product, score, and issue tables are clearly separated.
* Next recommended step: Add a simple review status workflow for issues or products.

### Review Workflow and Task List

* Date: TODO
* Change: Added product-level `review_status` values and a new Review Tasks table based on detected issues, including task type, priority, recommended action, and CSV export.
* Why it matters: Helps users move from issue detection to practical review work by showing what needs to be fixed next for each product.
* How to test: Run `python -m streamlit run app.py`, confirm the Product Readiness Scores table includes `review_status`, confirm the Review Tasks table appears below Data Quality Issues, and download `review_tasks.csv`.
* Next recommended step: Add a simple manual review status field or filter so users can track which tasks have been reviewed.

### Multiple Readiness Scores v1

* Date: TODO
* Change: Replaced the single readiness score view with multiple explainable score columns: data quality, marketplace readiness, translation readiness, compliance readiness, AI content readiness, and weighted overall readiness. Also added Excel upload support for `.xlsx` files and updated README documentation.
* Why it matters: Gives users a clearer picture of why a product is or is not ready, instead of relying on one unexplained score.
* How to test: Run `python -m streamlit run app.py`, confirm Product Readiness Scores contains all score columns, upload CSV or `.xlsx` product data, and confirm exports still work.
* Next recommended step: Add filters for review tasks by priority, task type, or review status.

### AI Suggestions v1

* Date: TODO
* Change: Added an AI Suggestions tab where a user can select one product and generate suggested title, description, bulletpoints, and a short review note. Added `.env` support, `.env.example`, OpenAI dependencies, and README instructions.
* Why it matters: Adds a human-in-the-loop content improvement step without automatically changing product data or running mass generation.
* How to test: Run `python -m streamlit run app.py`, open the AI Suggestions tab, confirm the missing API key message appears without `OPENAI_API_KEY`, then add a local `.env` file and generate suggestions for one product.
* Next recommended step: Add manual review tracking for accepted or rejected AI suggestions.

### Windows Start Script

* Date: TODO
* Change: Added `start_app.bat` in the project root and documented Windows double-click startup in the README.
* Why it matters: Makes the Streamlit MVP easier to start on Windows without typing terminal commands every time.
* How to test: Double-click `start_app.bat` or inspect it to confirm it changes into the project folder with `%~dp0` and runs `python -m streamlit run app.py`.
* Next recommended step: Add a short troubleshooting section for common local setup issues.

### AI Suggestions Default Selection

* Date: TODO
* Change: Updated the AI Suggestions tab so the product with the lowest `overall_readiness_score` is selected by default, with a short UI explanation.
* Why it matters: Helps demos and reviews focus AI support on the product that most needs attention instead of defaulting to the first product.
* How to test: Run `python -m streamlit run app.py`, open the AI Suggestions tab, and confirm the default selected product has the lowest readiness score.
* Next recommended step: Add filters for AI suggestion candidates, such as only products with Critical status or missing descriptions.

### AI Suggestions Error Handling

* Date: TODO
* Change: Improved AI Suggestions error handling with a friendly failure message, technical details expander, human-review warning, and raw AI response display when the response cannot be parsed as JSON.
* Why it matters: Makes the demo safer and easier to understand when the API key is invalid, the API is unavailable, or the response format is unexpected.
* How to test: Run `python -m streamlit run app.py`, open the AI Suggestions tab, test without an API key, and optionally test with an invalid key to confirm the friendly error message and technical details expander appear.
* Next recommended step: Add a small validation checklist for AI suggestions before a user accepts or copies them.

### Quality Check and README Cleanup

* Date: TODO
* Change: Ran a short project quality check and corrected an outdated README sentence about AI features.
* Why it matters: Keeps the documentation aligned with the current MVP, including optional AI Suggestions.
* How to test: Review the README and run `python -m py_compile app.py`.
* Next recommended step: Do a quick browser walkthrough of all tabs before sharing the portfolio demo.

### Demo Test Checklist

* Date: TODO
* Change: Added `docs/demo_test_checklist.md` with a short manual demo and smoke-test checklist, and linked it from the README.
* Why it matters: Makes it faster to validate the local portfolio demo after changes.
* How to test: Open `docs/demo_test_checklist.md` and walk through the checklist with the running Streamlit app.
* Next recommended step: Use the checklist before recording screenshots or sharing the demo.

### Codex Working Rules Update

* Date: TODO
* Change: Updated `AGENTS.md` with stronger strategic context, development mode, product priorities, scope control, workflow rules, documentation rules, testing rules, security rules, and current important files.
* Why it matters: Helps future Codex work stay focused on building a useful enterprise demo tool without drifting into release, SaaS, or over-engineered architecture work.
* How to test: Open `AGENTS.md` and confirm the updated rules reflect the current product direction.
* Next recommended step: Use the updated rules before planning the next larger product increment, such as Excel management export or Rule Engine v2.

### Excel Management Export v1

* Date: TODO
* Change: Added a Management Export tab with a downloadable Excel workbook containing Management Summary, Product Scores, Issues, Review Tasks, AI Suggestions, and Source Products sheets.
* Why it matters: Turns the MVP output into a more useful business artifact for e-commerce managers and operations teams.
* How to test: Run `python -m streamlit run app.py`, open the Management Export tab, download `commerce_readiness_ai_management_export.xlsx`, and confirm the expected sheets are present.
* Next recommended step: Add light formatting or column width improvements after the workbook structure is validated.

### Rule Engine / Product Data Checks v2 - Step 1

* Date: TODO
* Change: Added grouped product data check helpers and new checks for missing category, missing or invalid price, invalid EAN, generic product names, suspicious image URLs, missing manufacturer, missing attributes, and expanded safety categories for warning notes.
* Why it matters: Makes the audit more useful for real e-commerce product data workflows while keeping the app simple and rule-based.
* How to test: Run `python -m streamlit run app.py`, check the Issues and Review Tasks tabs for the new issue and task types, then confirm CSV exports and the Management Export include the new rows.
* Next recommended step: Validate the v2 checks with a realistic merchant CSV before planning variant or marketplace-specific checks.

### Review Workflow v1

* Date: TODO
* Change: Added a review-focused workflow with product review overview metrics, task filters by priority, task type, and review status, issue type and field name in Review Tasks, filtered task CSV export, and manual review status overrides stored in Streamlit session state.
* Why it matters: Helps users move from audit results to practical review work while keeping the MVP local and simple.
* How to test: Run `python -m streamlit run app.py`, open Review Tasks, use the filters, save a manual review status override, and confirm the status appears in Product Readiness Scores and exports.
* Next recommended step: Add persistence or accept/reject tracking only after the session-based workflow feels useful.

### AI Suggestions v1 Structured Workflow

* Date: TODO
* Change: Improved the AI Suggestions tab with selectable suggestion types, compact product context, stronger prompt instructions, structured output sections, prompt preview without an API key, and expanded CSV/Management Export fields for generated suggestions.
* Why it matters: Makes AI support more transparent and human-review friendly without automatically changing product data.
* How to test: Run `python -m streamlit run app.py`, open AI Suggestions, select suggestion types, confirm the API-key fallback and prompt preview work, and generate structured suggestions if an API key is available.
* Next recommended step: Add accept/reject tracking for generated suggestions only after the structured workflow is validated.

### Demo Dataset & Portfolio Polish v1

* Date: TODO
* Change: Expanded the sample dataset to 25 realistic demo products across apparel, electronics, home and kitchen, sports, office, toys, beauty, and pet supplies. Improved the README for portfolio use, added a portfolio case study draft, added a demo script, and refreshed the demo test checklist.
* Changed files: `data/sample_products.csv`, `README.md`, `docs/portfolio_case_study.md`, `docs/demo_script.md`, `docs/demo_test_checklist.md`, `docs/commerce_readiness_ai_project_log.md`, `.gitignore`.
* Why it matters: Makes the project easier to understand for GitHub visitors, recruiters, and interview walkthroughs while keeping the app focused on the existing MVP workflow.
* How to test: Run `python -m streamlit run app.py`, confirm the sample data loads, walk through `docs/demo_script.md`, and use `docs/demo_test_checklist.md` for a manual smoke test.
* Next recommended step: Capture screenshots for the README or portfolio case study after one full local demo pass.
* Intentionally not added: No new rule engine, marketplace presets, database, login, deployment, integrations, bulk AI generation, automatic write-back, legal compliance guarantees, or major UI redesign.

### Streamlit Compatibility & DataFrame Type Cleanup v1

* Date: TODO
* Change: Replaced deprecated `use_container_width` dataframe parameters with `width="stretch"` and added a small display-safety helper for Streamlit dataframe rendering.
* Why it matters: Removes noisy compatibility and Arrow serialization warnings so the local MVP feels cleaner and more professional during demos.
* How to test: Run `python -m streamlit run app.py`, open the main tabs, and confirm the previous `use_container_width` and mixed `value` column warnings no longer appear.
* Next recommended step: Do one browser-based walkthrough before recording screenshots.

### Final GitHub Readiness v1

* Date: TODO
* Change: Finalized README clarity, strengthened the demo test checklist, added `docs/screenshots_to_capture.md`, clarified the project log as the current source of truth, and extended `.gitignore` for local generated exports.
* Changed files: `README.md`, `.gitignore`, `docs/demo_test_checklist.md`, `docs/screenshots_to_capture.md`, `docs/portfolio_case_study.md`, `docs/commerce_readiness_ai_project_log.md`.
* Why it matters: Makes the repository easier to review on GitHub and more reliable for portfolio or interview walkthroughs.
* How to test: Run `python -m py_compile app.py`, confirm `data/sample_products.csv` loads with pandas, start the app locally, and walk through `docs/demo_test_checklist.md`.
* Next recommended step: Portfolio Case Study v1 Finalization.
* Intentionally not added: No new product features, database, login, roles, marketplace integrations, marketplace presets, architecture rewrite, bulk AI generation, automatic write-back, or legal compliance guarantees.

### Requirements Documentation v1

* Date: TODO
* Change: Added `docs/product_requirements.md` with target users, business goals, functional requirements, non-functional requirements, business rules, out-of-scope items, acceptance criteria, risks, and next recommended requirement block.
* Why it matters: Makes the project stronger from a requirements-engineering perspective and easier to evaluate as a serious portfolio project.
* How to test: Review `docs/product_requirements.md` and confirm it matches the current app behavior and MVP scope.
* Next recommended step: Use the requirements document as context when finalizing the portfolio case study.

### Testing Notes v1

* Date: TODO
* Change: Added `docs/testing_notes.md` with technical checks, manual smoke tests, functional acceptance checks, documentation checks, and known manual checks.
* Why it matters: Makes verification repeatable without adding unnecessary testing infrastructure.
* How to test: Follow `docs/testing_notes.md` before a demo or GitHub update.
* Next recommended step: Add lightweight automated tests only if they remain simple and low-risk.

### Portfolio Case Study v1

* Date: TODO
* Change: Finalized `docs/portfolio_case_study.md` as a professional portfolio case study with problem statement, target users, requirements approach, MVP scope, key features, product decisions, workflow, technical approach, quality documentation, results, screenshots to add, and next steps.
* Why it matters: Makes the project easier to explain in applications, interviews, and portfolio reviews.
* How to test: Read the case study and confirm it accurately reflects the current MVP and documented requirements.
* Next recommended step: Capture screenshots and optionally add selected images to the README or portfolio page.

### Master Product & Architecture Blueprint v1

* Date: TODO
* Change: Added `docs/master_product_architecture_blueprint.md` with the forward-looking Product Data Copilot vision, target users, core workflow, long-term capabilities, AI safety rules, AI suggestion data model, target architecture, refactor roadmap, pytest strategy, tooling strategy, UX strategy, explicit non-goals, risks, and definitions of portfolio-ready and almost sellable.
* Why it matters: Creates a clear professional direction for evolving the current Streamlit MVP into a more modular Product Data Copilot without overengineering or prematurely rebuilding the UI.
* How to test: Review the blueprint and confirm it does not require immediate code changes or new product features.
* Next recommended step: Add lightweight pytest tests before extracting logic from `app.py`.

### Codebase Audit & Refactor Inventory v1

* Date: TODO
* Change: Added `docs/codebase_refactor_inventory.md` documenting what currently lives in `app.py`, how the logic maps to future modules, refactor risks, safe extraction order, and first test candidates.
* Why it matters: Provides a safer bridge from the working Streamlit MVP to the future modular Product Data Copilot architecture.
* How to test: Review the inventory and confirm no code was moved or refactored.
* Next recommended step: Add lightweight pytest tests for pure validators and scoring helpers.

### Lightweight Tests v1 - Strategy

* Date: TODO
* Change: Added `docs/testing_strategy.md` documenting why direct pytest imports from the current monolithic `app.py` are unsafe, which pure functions should be extracted first, and which pytest tests should follow.
* Why it matters: Avoids brittle tests that accidentally execute Streamlit UI code and sets up a safer test-first refactor path.
* How to test: Review `docs/testing_strategy.md` and confirm no code or app behavior was changed.
* Next recommended step: Extract pure validators into an import-safe module, then add the first pytest tests.

### Extract Validators v1

* Date: TODO
* Change: Added the first import-safe package module under `src/product_data_copilot/`, extracted small pure validator helpers into `rules/validators.py`, added pytest coverage in `tests/test_validators.py`, and added `pytest` to requirements.
* Why it matters: Creates the first real automated test safety net before larger refactoring work begins.
* How to test: Run `python -m pytest` and `python -m py_compile app.py`.
* Next recommended step: Extract scoring helpers into an import-safe module with focused tests.

### Extract Scoring Helpers v1

* Date: TODO
* Change: Added `src/product_data_copilot/scoring/scoring_helpers.py` with small pure scoring helpers and pytest coverage in `tests/test_scoring_helpers.py`.
* Why it matters: Expands the import-safe test safety net before moving larger scoring logic out of the Streamlit monolith.
* How to test: Run `python -m pytest` and `python -m py_compile app.py`.
* Next recommended step: Extract review mapping helpers into an import-safe module with focused tests.

### Codex Workflow Setup v1

* Date: TODO
* Change: Updated `AGENTS.md` for the Product Data Copilot direction and added `docs/codex_workflow.md`, `docs/codex_task_backlog.md`, and `docs/codex_report_template.md`.
* Why it matters: Gives future Codex runs persistent instructions, a repeatable workflow, a task backlog, and a consistent report format.
* How to test: Review the new workflow documents and confirm forbidden files were not modified.
* Next recommended step: Continue with the next approved backlog block only after the user requests it.

### Repo State Check v1

* Date: TODO
* Change: Verified the current commit history, existing helper modules, and pytest coverage, then corrected `docs/codex_task_backlog.md` so `Extract Review Helpers v1` is the next block.
* Why it matters: Keeps the Codex task backlog aligned with the actual repository state after `Extract Scoring Helpers v1` was already committed.
* How to test: Run `git log --oneline -5`, `python -m py_compile app.py`, and `python -m pytest`.
* Next recommended step: Start `Extract Review Helpers v1` only after explicit user approval.

### Extract Review Helpers v1

* Date: TODO
* Change: Added `src/product_data_copilot/review/review_helpers.py` with small pure review helpers and pytest coverage in `tests/test_review_helpers.py`.
* Why it matters: Expands the import-safe test safety net for review task priority, task type, and review status logic before larger app slimdown work.
* How to test: Run `python -m pytest` and `python -m py_compile app.py`.
* Next recommended step: Extract export preparation helpers into an import-safe module with focused tests.

### Extract Export Helpers v1

* Date: TODO
* Change: Added `src/product_data_copilot/export/export_helpers.py` with small pure export preparation helpers and pytest coverage in `tests/test_export_helpers.py`.
* Why it matters: Adds a tested foundation for export filenames, sheet validation, DataFrame checks, and column ordering before moving larger export logic out of the Streamlit app.
* How to test: Run `python -m pytest` and `python -m py_compile app.py`.
* Next recommended step: Extract AI prompt helpers into an import-safe module with focused tests.

### Extract AI Prompt Helpers v1

* Date: TODO
* Change: Added `src/product_data_copilot/ai/prompt_helpers.py` with pure AI prompt safety, context, schema, confidence, and action-status helpers plus pytest coverage in `tests/test_prompt_helpers.py`.
* Why it matters: Builds a tested foundation for safer human-in-the-loop AI prompt preparation without calling OpenAI or changing current AI behavior.
* How to test: Run `python -m pytest`, `python -m py_compile app.py`, and confirm changed files contain no secrets.
* Next recommended step: Plan `App Slimdown v1` before wiring extracted helpers into `app.py`.

### App Slimdown v1 Planning

* Date: TODO
* Change: Added `docs/app_slimdown_plan.md` with current `app.py` responsibilities, target UI module direction, non-move areas, risk areas, rollback strategy, implementation phases, and required checks.
* Why it matters: Reduces refactor risk before touching the monolithic Streamlit app.
* How to test: Review `docs/app_slimdown_plan.md`, run `python -m py_compile app.py`, run `python -m pytest`, and confirm forbidden code/data paths were not modified.
* Next recommended step: Start `App Slimdown v1 - Phase 1` only after explicit approval.

## 8. Product Decisions

Important product decisions so far:

* Streamlit first instead of full SaaS
* CSV first instead of API integration
* Rule-based checks before AI suggestions
* Human review before automatic data changes
* Simple scoring before complex scoring

## 9. Known Limitations

Current known limitations:

* No automatic AI suggestion approval or write-back
* No mass AI generation for all products
* No database yet
* No login
* No marketplace-specific rule presets yet
* No real legal compliance check
* Manual review overrides are session-only
* Portfolio screenshots still need to be captured

## 10. Next Recommended Steps

1. Extract review mapping helpers into an import-safe module
2. Add lightweight pytest tests for review task priority and task type mapping
3. Capture screenshots using `docs/screenshots_to_capture.md`
4. Do one full demo walkthrough using `docs/demo_test_checklist.md`
5. Add selected screenshots to the README or portfolio page

## 11. Copy Context for Future Codex Prompts

Commerce Readiness AI is a beginner-friendly Streamlit MVP for e-commerce product data quality checks. The app loads `data/sample_products.csv` by default and also supports CSV and Excel upload. The current sample dataset has around 25 realistic demo products across multiple e-commerce categories with intentional data quality issues. The app displays product data, detects rule-based data quality issues, shows dashboard metrics, calculates multiple readiness scores, assigns product review statuses, creates a review task list, filters issues by severity, supports review task filters and manual review status overrides, exports readiness scores, issues, and review tasks as CSV files, creates a management-ready Excel workbook, and optionally generates structured AI suggestions for one selected product. Product Data Checks v2 adds checks for category, price, EAN validity, generic titles, image URLs, manufacturer, attributes, and expanded safety categories. The AI Suggestions tab selects the product with the lowest readiness score by default and supports selectable suggestion types. The current layout uses tabs for Dashboard, Product Data, Scores, Issues, Review Tasks, Management Export, and AI Suggestions, plus sidebar controls for file upload and severity filtering. Final GitHub Readiness v1 is complete, with README, demo checklist, demo script, portfolio draft, screenshot planning, and project log prepared for review.

The current data columns are `sku`, `product_name`, `category`, `description`, `brand`, `manufacturer`, `attributes`, `ean`, `language`, `price`, `image_url`, `warning_notes`, `translation_de`, and `translation_en`.

Current checks include missing and short product names, generic product names, missing and short descriptions, missing brand, missing manufacturer, missing category, missing or invalid EAN, missing or invalid price, missing attributes, missing or suspicious image URL, missing German translation, missing English translation, and missing warning notes for safety-relevant categories.

Scoring now includes `data_quality_score`, `marketplace_readiness_score`, `translation_readiness_score`, `compliance_readiness_score`, `ai_content_readiness_score`, and `overall_readiness_score`. Overall score weighting is 35% Data Quality, 25% Marketplace Readiness, 15% Translation Readiness, 15% Compliance Readiness, and 10% AI Content Readiness. Status is Ready for scores 85+, Needs Review for scores 60-84, and Critical for scores below 60.

AI suggestions use `OPENAI_API_KEY` from the local environment or `.env` file. The API key must never be stored in code, README content, or the project log. AI suggestions are draft recommendations, human-in-the-loop only, and are not automatically applied to product data.
