# Commerce Readiness AI

Commerce Readiness AI is a Streamlit MVP for auditing e-commerce product data before marketplace or shop publication.

It helps product data managers, marketplace managers, e-commerce operations teams, and category teams find missing or weak product data, prioritize review work, calculate readiness scores, generate human-reviewed AI draft suggestions, and export audit results.

The project is currently a local demo tool, not a production SaaS product.

## Problem It Solves

E-commerce teams often manage product data across CSV files, PIM exports, marketplace templates, and manual spreadsheets. Before products can be published, teams need to know:

- Which products are missing required data
- Which listings need better content
- Which products need translation or compliance review
- Which issues should be fixed first
- What can be exported for management or operational follow-up

Commerce Readiness AI turns a product file into a clear audit workflow with scores, issues, review tasks, and exports.

## MVP Features

- CSV and Excel upload
- Sample product dataset for demos
- Product data preview
- Rule-based product data checks
- Dashboard metrics
- Multiple readiness scores
- Product review status
- Review Workflow v1 with task overview, filters, manual status overrides, and filtered task export
- Data Quality Issues table with severity filtering
- CSV exports for scores, issues, and review tasks
- Excel Management Export with summary, scores, issues, tasks, AI suggestions, and source products
- Optional AI Suggestions for one selected product at a time

## Product Data Checks

Product Data Checks v2 currently checks for practical audit issues such as:

- Missing or short product names
- Generic product titles
- Missing or short descriptions
- Missing brand or manufacturer
- Missing category
- Missing, invalid, or suspicious EAN/GTIN values
- Missing or invalid prices
- Missing product attributes
- Missing or suspicious image URLs
- Missing German or English translations
- Missing warning notes for safety-relevant categories

## Readiness Scores

Each product receives these scores:

- `data_quality_score`
- `marketplace_readiness_score`
- `translation_readiness_score`
- `compliance_readiness_score`
- `ai_content_readiness_score`
- `overall_readiness_score`

Overall score weighting:

- 35% Data Quality
- 25% Marketplace Readiness
- 15% Translation Readiness
- 15% Compliance Readiness
- 10% AI Content Readiness

Readiness status:

- 85+ = Ready
- 60-84 = Needs Review
- Below 60 = Critical

## Review Workflow v1

The Review Tasks tab helps turn audit findings into practical work:

- Product Review Overview
- Tasks by priority
- Top task types
- Review task table with issue type and field name
- Filters for priority, task type, and review status
- Manual product review status overrides stored in the local Streamlit session
- CSV download for the currently filtered review task table

Manual overrides are not stored in a database. They are session-only and are included in the current score display and exports while the app session is active.

## AI Suggestions v1

The AI Suggestions tab can generate draft recommendations for one selected product:

- Improved product title
- Product description
- Bullet points
- Missing attribute suggestions
- Translation suggestions
- Compliance or safety review note
- Human review notes

AI suggestions are drafts only. They must be reviewed by a human and are never automatically written back into product data.

By default, the AI Suggestions tab selects the product with the lowest readiness score so review starts with the most critical item.

To enable AI suggestions:

1. Create a local `.env` file in the project root.
2. Use `.env.example` as the template.
3. Set `OPENAI_API_KEY` in your local `.env` file.

If `OPENAI_API_KEY` is missing, the app still works and shows a clear missing-key message.

## Excel Management Export

The Management Export tab creates one Excel workbook:

```text
commerce_readiness_ai_management_export.xlsx
```

Sheets included:

- Management Summary
- Product Scores
- Issues
- Review Tasks
- AI Suggestions
- Source Products

The export does not require an OpenAI API key. If no AI suggestions have been generated, the AI Suggestions sheet is still included but empty.

## Demo Workflow

1. Start the app.
2. Use the built-in sample data or upload a CSV/XLSX file.
3. Review dashboard metrics.
4. Open Issues to inspect detected product data problems.
5. Open Scores to compare readiness by product.
6. Open Review Tasks to filter operational work and apply a manual review status override.
7. Open AI Suggestions to show the missing-key fallback or generate one product suggestion if an API key is configured.
8. Download the Excel Management Export.

## Tech Stack

- Python
- Streamlit
- Pandas
- OpenPyXL
- OpenAI Python SDK
- python-dotenv

## How to Run Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
python -m streamlit run app.py
```

3. Open the local URL shown in your terminal.

## Start on Windows

Windows users can start the app by double-clicking:

```text
start_app.bat
```

If modules are missing when the app starts, run this once in the project folder:

```bash
pip install -r requirements.txt
```

Then double-click `start_app.bat` again.

## Current Status

This is a local MVP and portfolio demo. It is designed to show a practical product-data audit workflow, not to publish products automatically or replace legal/compliance review.

## Intentionally Out of Scope

- Production deployment
- Login, roles, or multi-user workflow
- Database persistence
- Marketplace-specific presets
- Shopware, Shopify, or Plentymarkets integrations
- Variant parent-child logic
- Bulk AI generation
- Automatic acceptance of AI suggestions
- Automatic write-back to source product data
- Legal compliance guarantees

## Roadmap

- Improve Excel export formatting and column widths
- Add accept/reject tracking for AI suggestions
- Expand the rule catalog after testing with realistic merchant data
- Add optional persistence for review decisions
- Add marketplace-specific rule presets later
- Create final screenshots and portfolio write-up

## Project Files

- `app.py` - Streamlit app
- `requirements.txt` - Python dependencies
- `data/sample_products.csv` - demo product data
- `docs/commerce_readiness_ai_project_log.md` - project progress log
- `docs/demo_test_checklist.md` - manual demo and smoke-test checklist
- `docs/demo_script.md` - demo walkthrough script
- `docs/portfolio_case_study.md` - portfolio case study draft
- `.env.example` - local environment variable template
- `start_app.bat` - Windows launcher

## Documentation

A manual demo test checklist is available at `docs/demo_test_checklist.md`.
