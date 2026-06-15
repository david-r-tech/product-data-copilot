# Commerce Readiness AI - Portfolio Case Study

## Project Overview

Commerce Readiness AI is a local Streamlit MVP for auditing e-commerce product data before products are published to shops, marketplaces, or catalog workflows.

The project turns a CSV/XLSX product file into a structured product-data review workflow with dashboard metrics, rule-based issue detection, explainable readiness scores, review tasks, optional AI draft suggestions, and exportable management reports.

The goal was not to build a full SaaS product. The goal was to create a focused, business-oriented MVP that demonstrates product thinking, requirements engineering, data quality logic, human-in-the-loop AI support, and practical reporting.

## Problem Statement

E-commerce teams often receive product data in spreadsheets, PIM exports, supplier files, or marketplace templates. These files can contain missing product names, weak descriptions, invalid identifiers, missing translations, incomplete media links, unclear warning notes, or inconsistent commercial data.

Without a structured audit workflow, teams have to inspect product rows manually. This makes it difficult to answer simple operational questions:

- Which products are ready?
- Which products need urgent data completion?
- Which issues block marketplace review?
- Which products need translation or compliance review?
- Which tasks should the team handle first?
- What summary can be shared with managers or stakeholders?

Commerce Readiness AI addresses this by making product-data issues visible, prioritized, and exportable.

## Target Users

- Product Data Managers
- Marketplace Managers
- E-commerce Operations Teams
- Category Managers
- Content and Translation Teams
- Small merchant teams preparing marketplace listings

## Product Goals

- Make product data quality issues visible quickly
- Prioritize review work by severity and business impact
- Provide explainable readiness scores per product
- Convert audit findings into operational review tasks
- Support AI-assisted content improvement without automatic write-back
- Provide CSV and Excel exports for review and management workflows
- Keep the MVP understandable, local, and easy to run

## Requirements Approach

The project was shaped around practical requirements instead of a broad feature wishlist. The first priority was to make product data problems visible. The second priority was to make those problems actionable through scoring, review tasks, filters, and exports.

The current requirements are documented in `docs/product_requirements.md`, including:

- Functional requirements
- Non-functional requirements
- Business rules
- Acceptance criteria
- Out-of-scope items
- Risks and limitations

This gives the project a clear requirements-engineering baseline and makes it easier to explain why the MVP is scoped the way it is.

## MVP Scope

The MVP includes:

- Local Streamlit app
- Built-in sample product dataset
- CSV and XLSX upload
- Product data preview
- Rule-based product data checks
- Dashboard metrics
- Multiple readiness scores
- Product review status
- Review task workflow
- Manual review status override in Streamlit session state
- CSV exports
- Excel Management Export
- Optional AI Suggestions for one selected product
- Documentation for requirements, demo testing, screenshots, and portfolio use

The MVP intentionally does not include production deployment, user accounts, database persistence, marketplace integrations, or automatic publishing.

## Key Features

- Sample demo dataset with realistic product categories and intentional quality issues
- CSV and Excel upload for user-provided product data
- Product Data tab for source-data inspection
- Rule-based issue detection with severity, field name, message, and recommended action
- Dashboard metrics for product count, issue count, affected products, and average scores
- Multiple readiness scores: data quality, marketplace readiness, translation readiness, compliance readiness, AI content readiness, and overall readiness
- Review Tasks tab with task types, priorities, filters, and manual status override
- CSV exports for operational follow-up
- Excel Management Export with summary, scores, issues, tasks, AI suggestions, and source products
- Optional AI Suggestions tab with API-key fallback and human-review warning

## Product Decisions and Trade-Offs

- **Streamlit first:** Streamlit was chosen to build a useful local MVP quickly instead of spending time on frontend/backend architecture.
- **CSV/XLSX first:** Spreadsheet upload was prioritized because product-data teams often work with CSV exports, marketplace templates, and supplier spreadsheets.
- **Rules before AI:** Rule-based checks make the audit transparent and explainable before adding AI suggestions.
- **Human-in-the-loop AI:** AI Suggestions are limited to one selected product and are not automatically written back to source data.
- **Session state before database:** Manual review overrides use Streamlit session state to keep the MVP simple and avoid premature persistence work.
- **Excel export as business artifact:** The Management Export turns the audit into a file that business stakeholders can open and review outside the app.

## User Workflow

1. Start the local Streamlit app.
2. Load the built-in sample dataset or upload a CSV/XLSX product file.
3. Review dashboard metrics to understand catalog health.
4. Inspect product data in the Product Data tab.
5. Review detected issues and filter by severity.
6. Compare readiness scores across products.
7. Use Review Tasks to prioritize operational work.
8. Apply a manual review status override during the current session.
9. Open AI Suggestions to show the missing-key fallback or generate one product suggestion if an API key is configured.
10. Download CSV exports or the Excel Management Export for follow-up.

## Technical Approach

The app is implemented in Python with Streamlit and Pandas.

Product checks are grouped in helper functions inside `app.py` to keep the code approachable while avoiding a large rule-engine framework too early. This keeps the MVP easy to understand and modify.

Detected issues use a stable structure:

- `sku`
- `issue_type`
- `field_name`
- `severity`
- `message`
- `recommended_action`

Readiness scores are calculated from simple, explainable checks and combined into a weighted overall score. Review tasks are generated from detected issues, which keeps the workflow consistent across the UI and exports.

The Excel Management Export is generated in memory with `BytesIO`, Pandas, and OpenPyXL. AI Suggestions use an environment-based OpenAI API key when available and fall back safely when no key is configured.

## Quality and Documentation

The project includes supporting documentation to make the MVP understandable and testable:

- `README.md` for project overview, setup, features, scope, and roadmap
- `docs/product_requirements.md` for requirements, acceptance criteria, risks, and scope
- `docs/testing_notes.md` for technical and manual verification steps
- `docs/demo_test_checklist.md` for repeatable demo validation
- `docs/demo_script.md` for walkthrough preparation
- `docs/screenshots_to_capture.md` for portfolio screenshot planning
- `docs/commerce_readiness_ai_project_log.md` as the central project log

## Results / Current MVP Status

The current MVP demonstrates a complete local product-data audit workflow:

- Load product data
- Detect product-data issues
- Explain why products are or are not ready
- Score readiness across multiple dimensions
- Create operational review tasks
- Support manual review decisions in the session
- Generate optional AI draft suggestions
- Export operational and management-ready files

The project is ready for GitHub/portfolio review and for final screenshots.

## Screenshots to Add

Detailed screenshot planning is tracked in `docs/screenshots_to_capture.md`.

Recommended screenshots:

- App overview / header
- Sample data loaded
- Dashboard metrics
- Readiness Scores tab
- Issues tab
- Review Tasks tab
- Manual Review Status Override
- AI Suggestions tab
- Management Export tab
- Optional opened Excel export

## What This Project Demonstrates

This project demonstrates:

- Understanding of a real e-commerce operations problem
- Requirements engineering and scope control
- MVP product thinking
- Rule-based data quality validation
- Explainable scoring logic
- Human-in-the-loop AI design
- Streamlit and Pandas implementation skills
- Business-friendly exports
- Professional project documentation

## Next Steps

- Capture final screenshots and add selected images to the README or portfolio page
- Improve Excel export formatting and column widths
- Add accept/reject tracking for AI suggestions
- Test the rule catalog with realistic merchant exports
- Add optional persistence for review statuses if the workflow proves useful
- Consider marketplace-specific rule presets later
