# Product Data Copilot

AI-assisted product data quality and export workflow for E-commerce teams.

Product Data Copilot is a local Streamlit MVP for auditing product data before marketplace or shop publication. It helps product data managers, marketplace managers, E-commerce operations teams, and category teams find missing or weak product data, prioritize review work, generate human-reviewed AI draft suggestions, and export review-ready workbooks.

This project is a portfolio-grade local prototype. It is not a production SaaS product.

<!-- Screenshot placeholder: add final app screenshot here -->

## What It Does

Product Data Copilot turns a product file into a structured review workflow:

- Product data can be loaded from CSV/XLSX or from the built-in sample dataset.
- Missing or problematic product data can be detected with rule-based checks.
- Products receive explainable readiness scores.
- Issues are converted into practical review tasks.
- AI can suggest product data improvements based on available source information.
- Human review is required before suggestions are used.
- Approved suggestions can be prepared for Excel export.
- Original uploaded data is not overwritten automatically.

## Key Features

- CSV/XLSX upload
- Built-in sample data for demos
- Product data preview
- Product data checks for missing, weak, or suspicious fields
- Multiple readiness scores
- Issues table with severity filtering
- Review workflow with task filters and session-only manual status override
- AI Suggestions v1 for one selected product
- Smart Suggestions v2 with structured field-level suggestions
- Human Approval UI for approve/reject/pending/blocked review states
- German furniture demo export for no-cost description, bulletpoint, and translation filling
- Improved Excel export for approved/pending/rejected/blocked suggestion groups
- Excel Management Export for business review
- Pytest-backed helper modules under `src/product_data_copilot/`

## Demo Workflow

1. Start the app.
2. Load the built-in sample data or upload a CSV/XLSX file.
3. Review product checks, dashboard metrics, and readiness scores.
4. Open Issues to inspect detected product data problems.
5. Open Review Tasks to filter operational work and apply session-only review status overrides.
6. Open AI Suggestions and use Smart Suggestions v2.
7. Generate or load demo Smart Suggestions v2 records.
8. Approve, reject, or leave suggestions pending during the current session.
9. Preview the improved product data export groups.
10. Download the improved Excel workbook or the management workbook.

For a short German presentation without API costs, open the `DE Demo` tab, upload `data/moebel_demo_upload.xlsx`, click `Demo-Liste erstellen`, and download `moebel_demo_export.xlsx`. The demo fills empty description, bulletpoint, and English translation fields without calling OpenAI.

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

Start the Streamlit app:

```bash
python -m streamlit run app.py
```

Then open the local URL shown in the terminal.

### Start on Windows

Windows users can also double-click:

```text
start_app.bat
```

If modules are missing, run this once in the project folder:

```bash
pip install -r requirements.txt
```

## Tests

Run the test suite:

```bash
python -m pytest
```

Current known test state:

```text
122 passed
```

## Architecture Overview

The app is intentionally local-first and Streamlit-based, but core helper logic has been extracted into import-safe modules.

```text
app.py
src/product_data_copilot/
  rules/
  scoring/
  review/
  export/
  ai/
  ui/
tests/
docs/
data/
```

Key areas:

- `app.py` - Streamlit runtime and main app flow
- `src/product_data_copilot/rules/` - validation helpers
- `src/product_data_copilot/scoring/` - readiness scoring helpers
- `src/product_data_copilot/review/` - review status and task mapping helpers
- `src/product_data_copilot/export/` - export preparation helpers
- `src/product_data_copilot/ai/` - prompt, schema, parser, and Smart Suggestions v2 helpers
- `src/product_data_copilot/ui/` - small Streamlit presentation helpers
- `tests/` - pytest coverage for pure helper logic
- `docs/` - planning, QA, project status, and portfolio documentation

## AI Safety / Human Review

AI suggestions are draft recommendations only.

Safety rules:

- No invented facts policy: suggestions should be based on available source fields.
- Structured suggestions include source, reason, confidence, and risk context.
- User approval is required.
- AI cannot approve itself.
- Blocked suggestions cannot be approved.
- Approved means export candidate, not automatic source mutation.
- Missing API keys are handled safely.

To enable OpenAI-backed suggestions locally:

1. Copy `.env.example` to `.env`.
2. Set `OPENAI_API_KEY` in `.env`.
3. Restart the app.

Never commit `.env` or real API keys.

## Export Safety

The improved Excel export is a review handoff artifact.

- Original uploaded data remains unchanged.
- Approved suggestions are separated from pending, rejected, blocked, and unknown suggestions.
- The workbook includes an original source snapshot.
- No source file is overwritten.
- No automatic write-back is performed.
- Review decisions are session-only in the current MVP.

The improved export workbook is generated locally in memory as:

```text
product_data_copilot_improved_export.xlsx
```

The Management Export workbook is also available for audit summaries:

```text
commerce_readiness_ai_management_export.xlsx
```

Generated export files are local outputs and should not be committed to the repository.

## Sample Data

The app loads `data/sample_products.csv` when no file is uploaded.

The demo dataset contains 25 fictional products across categories such as Apparel, Electronics, Home & Kitchen, Sports & Outdoors, Office, Toys, Beauty / Personal Care, and Pet Supplies. It intentionally includes realistic product data issues so checks, scores, review tasks, AI suggestions, and exports can be demonstrated immediately.

## Case Study and Documentation

- [Portfolio Case Study](docs/portfolio_case_study.md)
- [Portfolio Screenshot Checklist](docs/portfolio_screenshot_checklist_v1.md)
- [Final Portfolio Release Checklist](docs/final_portfolio_release_checklist_v1.md)
- [GitHub Repo Rename Manual Checklist](docs/github_repo_rename_manual_checklist_v1.md)
- [Demo Test Checklist](docs/demo_test_checklist.md)
- [Demo Script](docs/demo_script.md)
- [Project Log](docs/commerce_readiness_ai_project_log.md)
- [Current Context](docs/current_context.md)

## Final Portfolio Docs

Use these documents for the final portfolio handoff:

- [Portfolio Case Study](docs/portfolio_case_study.md) - product story, workflow, architecture, AI safety, export safety, limitations, and roadmap.
- [Portfolio Screenshot Checklist](docs/portfolio_screenshot_checklist_v1.md) - manual screenshot plan for GitHub and portfolio presentation.
- [Final Portfolio Release Checklist](docs/final_portfolio_release_checklist_v1.md) - final go/no-go checklist before sharing the project.
- [GitHub Repo Rename Manual Checklist](docs/github_repo_rename_manual_checklist_v1.md) - owner-only steps for the optional future repository rename.

## Current Status

Product Data Copilot is a local MVP and portfolio prototype. It is designed to demonstrate a practical product-data audit workflow with AI safety thinking, human review, tested helper modules, and safe exports.

It is not intended to publish products automatically or replace legal/compliance review.

## Current Limitations

- Not SaaS
- No deployment or hosted backend
- No database
- No login or multi-user roles
- No marketplace integrations
- No marketplace-specific rule presets
- Session-only approval state
- AI suggestions require human review
- German furniture demo export is deterministic demo output, not live AI generation
- No automatic product data write-back
- No legal compliance guarantees

## Roadmap / Next Steps

- Capture final screenshots
- Run final manual QA
- Plan GitHub repository naming cleanup
- Prepare portfolio release v0.1
- Expand pytest coverage around key business rules
- Improve workbook formatting and column widths

## License

No license file has been added yet. Treat the repository as a private portfolio project unless a license is added later.
