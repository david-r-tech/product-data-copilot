# Commerce Readiness AI - Portfolio Case Study Draft

## Project Overview

Commerce Readiness AI is a local Streamlit MVP for auditing e-commerce product data before products are published to shops, marketplaces, or catalog workflows.

The project focuses on turning messy product files into a clear review workflow with dashboard metrics, issue detection, readiness scores, review tasks, optional AI draft suggestions, and exportable management reports.

## Problem Statement

Product data teams often receive product information in spreadsheets with missing fields, weak descriptions, invalid identifiers, missing translations, incomplete media links, and unclear compliance notes.

These issues slow down marketplace onboarding, create manual review work, and make it difficult for managers to understand which products are ready and which need attention.

The MVP answers a practical question: "What should we fix first before these products are ready for commerce?"

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
- Convert issues into operational review tasks
- Support human-reviewed AI draft suggestions without automatic write-back
- Export results in formats that can be shared with business stakeholders

## MVP Scope

The MVP supports local CSV/XLSX upload, rule-based product data checks, readiness scores, review workflow, AI draft suggestions for one product, and management exports.

It is not a production system. It does not include login, database persistence, marketplace integrations, deployment, or automated publishing.

## Key Features

- Sample demo dataset with realistic product categories and intentional data quality issues
- CSV and Excel upload
- Product data preview
- Rule-based issue detection
- Dashboard metrics for products, issues, and scores
- Multiple readiness scores
- Review task generation
- Review task filtering
- Manual review status override in session state
- CSV exports for operational tables
- Excel Management Export with summary and detailed sheets
- Optional AI Suggestions tab with missing-key fallback and human-review warning

## Product Decisions and Trade-Offs

- Streamlit was chosen for speed and clarity instead of building a full SaaS interface.
- CSV/XLSX upload was prioritized before API integrations because spreadsheets are common in product data operations.
- Rule-based checks were implemented before AI so users can understand exactly why issues are detected.
- AI suggestions are limited to one selected product to keep the workflow human-in-the-loop.
- Manual review overrides are stored only in Streamlit session state to avoid premature database complexity.
- The Excel Management Export was prioritized because it creates a practical artifact for managers and operations teams.

## User Workflow

1. Start the local Streamlit app.
2. Load the sample dataset or upload a product CSV/XLSX file.
3. Review dashboard metrics to understand catalog health.
4. Inspect detected issues by severity.
5. Compare product readiness scores.
6. Use Review Tasks to prioritize operational work.
7. Apply a manual review status override during the review session.
8. Generate AI draft suggestions for one selected product if an API key is configured.
9. Download CSV files or the Excel Management Export for follow-up.

## Technical Approach

The app is implemented in Python with Streamlit and Pandas.

Product checks are grouped in small helper functions inside `app.py` to keep the code beginner-friendly while avoiding a large rule-engine framework too early.

Detected issues use a stable structure:

- `sku`
- `issue_type`
- `field_name`
- `severity`
- `message`
- `recommended_action`

Readiness scores are calculated from simple ratio-based checks and combined into a weighted overall score. Review tasks are generated from detected issues, which keeps the workflow consistent across the UI and exports.

The Excel Management Export is generated in memory with `BytesIO`, Pandas, and OpenPyXL.

## Screenshots to Add Later

- Dashboard overview
- Product data preview
- Issues tab with severity filter
- Product readiness scores
- Review Tasks tab with filters and manual override
- Management Export tab
- AI Suggestions tab with missing-key fallback or generated suggestion

## Results / Current MVP Status

The current MVP demonstrates a complete local product-data audit workflow:

- Load product data
- Detect issues
- Score product readiness
- Create review tasks
- Support manual review decisions
- Generate optional AI draft suggestions
- Export operational and management-ready files

The project is ready for portfolio screenshots, demo recording, and testing with more realistic merchant data.

## Next Steps

- Improve Excel formatting and column widths
- Add accept/reject tracking for AI suggestions
- Test the rule catalog with realistic merchant exports
- Add optional persistence for review statuses
- Add marketplace-specific rule presets later
- Prepare final portfolio screenshots and demo video
