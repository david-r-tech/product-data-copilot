# Product Data Copilot - Portfolio Screenshot Checklist v1

Screenshots are captured manually by the project owner after running the app locally. This block only documents what to capture.

Use this checklist after the app has passed the manual UX and export QA checks. The screenshots should support the portfolio case study and GitHub presentation without overstating the current MVP.

Recommended local start command:

```bash
python -m streamlit run app.py
```

## Capture Guidelines

- Use the built-in sample data unless a specific screenshot requires uploaded data.
- Keep browser zoom consistent across screenshots.
- Avoid showing API keys, local secrets, or private file paths.
- Prefer screenshots that show product value, safety wording, and workflow clarity.
- Capture only stable states that can be reproduced from the sample data or demo fixture.
- Do not crop away important captions, warnings, or safety copy.

## 1. Landing / Upload Area

### Screenshot 1.1 - App Landing and Upload Entry

- Purpose: Show the first impression and make the product identity clear.
- What to show: Product Data Copilot title/header, value proposition, sidebar or upload/sample data controls.
- How to prepare the app state: Start the app with no uploaded file so sample-data fallback is active.
- Suggested filename: `01_product_data_copilot_landing_upload.png`
- Portfolio caption: Product Data Copilot starts as a local Streamlit workflow for auditing e-commerce product data from sample data, CSV, or Excel files.
- Pass/fail notes: PASS if product name, purpose, and upload/sample workflow are visible. FAIL if old branding is prominent or the upload path is unclear.

## 2. Sample Data Loaded

### Screenshot 2.1 - Product Data Preview

- Purpose: Show that the app works immediately with realistic sample data.
- What to show: Product Data tab with product table and understandable columns.
- How to prepare the app state: Use sample data, open the Product Data tab, and scroll only enough to show key columns such as `sku`, `product_name`, `category`, `brand`, `price`, and `attributes`.
- Suggested filename: `02_sample_data_product_table.png`
- Portfolio caption: The sample dataset includes realistic product rows and intentional quality issues so the audit workflow can be demonstrated without external files.
- Pass/fail notes: PASS if product rows and columns are readable. FAIL if the table looks empty, confusing, or disconnected from the demo story.

## 3. Product Readiness Scores

### Screenshot 3.1 - Readiness Scores Overview

- Purpose: Show explainable scoring instead of one opaque health score.
- What to show: Scores tab with score columns and review status.
- How to prepare the app state: Use sample data and open the Scores tab.
- Suggested filename: `03_readiness_scores_overview.png`
- Portfolio caption: Multiple readiness scores help users compare data quality, marketplace readiness, translations, compliance, AI content readiness, and overall status.
- Pass/fail notes: PASS if score columns and review status are visible. FAIL if the screenshot hides the overall score or review status.

## 4. Data Quality Issues

### Screenshot 4.1 - Issues Table and Severity

- Purpose: Show rule-based issue detection and prioritization.
- What to show: Issues tab with issues table, severity/status columns, issue type, field name, message, and recommended action.
- How to prepare the app state: Use sample data, open the Issues tab, and keep severity filters broad enough to show multiple issue types.
- Suggested filename: `04_data_quality_issues_table.png`
- Portfolio caption: Rule-based checks turn messy product rows into clear issues with severity, affected fields, and recommended actions.
- Pass/fail notes: PASS if issue severity and recommended actions are visible. FAIL if the screenshot only shows empty filters or hides issue context.

## 5. Review Tasks / Workflow

### Screenshot 5.1 - Review Tasks Table

- Purpose: Show how audit findings become operational tasks.
- What to show: Review Tasks tab with task table, priority, task type, issue type, recommended action, and review status.
- How to prepare the app state: Use sample data and open the Review Tasks tab with filters set to show at least High and Medium priority rows.
- Suggested filename: `05_review_tasks_table.png`
- Portfolio caption: Review tasks translate product data issues into prioritized work for operations, content, translation, and compliance review.
- Pass/fail notes: PASS if tasks, priorities, and review statuses are readable. FAIL if filters hide all rows.

### Screenshot 5.2 - Manual Review Status Override

- Purpose: Show the session-based review workflow.
- What to show: Manual review status override area, SKU selector, status selector, and explanatory session-only wording if visible.
- How to prepare the app state: Open Review Tasks and select a product SKU for status override.
- Suggested filename: `06_manual_review_status_override.png`
- Portfolio caption: Manual review status overrides allow a reviewer to mark product review progress during the current Streamlit session.
- Pass/fail notes: PASS if it is clear this is a review aid, not a source data write-back. FAIL if the screenshot implies persistent database storage.

## 6. AI Suggestions v1

### Screenshot 6.1 - AI Suggestions v1 Safe Fallback

- Purpose: Show that the AI area is safe even without an API key.
- What to show: AI Suggestions tab with draft/human-review message and missing API-key fallback or prompt preview.
- How to prepare the app state: Run without `OPENAI_API_KEY`, open AI Suggestions, and keep the selected product visible.
- Suggested filename: `07_ai_suggestions_v1_missing_key.png`
- Portfolio caption: AI Suggestions v1 supports one selected product and remains safe when no API key is configured.
- Pass/fail notes: PASS if draft/human-review wording and missing-key fallback are visible. FAIL if the app looks broken without an API key.

## 7. Smart Suggestions v2

### Screenshot 7.1 - Smart Suggestions v2 Experimental Section

- Purpose: Show the structured field-level suggestion model.
- What to show: Smart Suggestions v2 experimental section, prompt preview expander or demo fixture controls, and structured suggestions table.
- How to prepare the app state: Open AI Suggestions and use the V2 experimental section. If needed, load demo Smart Suggestions v2 records.
- Suggested filename: `08_smart_suggestions_v2_structured_table.png`
- Portfolio caption: Smart Suggestions v2 uses structured field-level rows with source, reason, confidence, risk, and review-required status.
- Pass/fail notes: PASS if source/reason/confidence or equivalent display labels are visible. FAIL if V2 appears to replace V1 or looks auto-approved.

### Screenshot 7.2 - Demo Fixture Flow

- Purpose: Show deterministic local testing without needing an API key.
- What to show: Demo fixture loader and loaded V2 demo rows.
- How to prepare the app state: Open the demo fixture expander and click `Load demo Smart Suggestions v2 records`.
- Suggested filename: `09_smart_suggestions_v2_demo_fixture.png`
- Portfolio caption: The deterministic demo fixture lets the Smart Suggestions v2 workflow be tested without a real API key.
- Pass/fail notes: PASS if demo/test labeling is visible. FAIL if fixture output could be mistaken for real AI output.

## 8. Human Approval UI

### Screenshot 8.1 - Human Review Detail Panel

- Purpose: Show one-suggestion-at-a-time human review.
- What to show: Selected suggestion details including SKU, product, field, current value, suggested value, reason, source fields, confidence, risk, and current review status.
- How to prepare the app state: Load demo V2 records, select one non-blocked suggestion in the Human Review section.
- Suggested filename: `10_human_approval_detail_panel.png`
- Portfolio caption: Human review keeps AI suggestions controlled by showing the evidence and risk context before approval or rejection.
- Pass/fail notes: PASS if the selected suggestion details are understandable. FAIL if source/reason/risk are hidden.

### Screenshot 8.2 - Approval States

- Purpose: Show pending, approved, rejected, and blocked states.
- What to show: Review decision metrics or table rows after one suggestion is approved, one rejected, one left pending, and one blocked row visible.
- How to prepare the app state: Load demo V2 records, approve one non-blocked row, reject one non-blocked row, leave one pending, and select or show a blocked row.
- Suggested filename: `11_human_approval_states.png`
- Portfolio caption: Approval decisions are session-only, blocked rows remain non-approvable, and approved suggestions become export candidates only.
- Pass/fail notes: PASS if approved/rejected/pending/blocked states are clear. FAIL if blocked suggestions look approvable or approved suggestions look automatically applied.

## 9. Improved Product Data Export Preview

### Screenshot 9.1 - Export Preview Groups

- Purpose: Show safe export preparation before downloading the workbook.
- What to show: Improved Product Data Export Preview with approved, pending, rejected, blocked, and unknown groups if available.
- How to prepare the app state: Load demo V2 records and apply at least one approve/reject decision before scrolling to the export preview.
- Suggested filename: `12_improved_export_preview_groups.png`
- Portfolio caption: The improved export preview separates approved, pending, rejected, blocked, and unknown suggestions before any workbook is downloaded.
- Pass/fail notes: PASS if safety copy and status groups are visible. FAIL if preview implies source data has already changed.

### Screenshot 9.2 - Improved Export Download Copy

- Purpose: Show that the workbook is a handoff artifact, not a write-back mechanism.
- What to show: Download button area and safety copy explaining no automatic product data changes.
- How to prepare the app state: Use V2 records so the improved export download area is meaningful.
- Suggested filename: `13_improved_export_download_copy.png`
- Portfolio caption: The improved Excel export is prepared in memory and treats approved suggestions as export candidates only.
- Pass/fail notes: PASS if "no source write-back" or equivalent safety copy is visible. FAIL if the UI suggests automatic source updates.

## 10. Improved Excel Export Workbook

### Screenshot 10.1 - Workbook Sheet Tabs

- Purpose: Show the final Excel handoff artifact.
- What to show: Opened `product_data_copilot_improved_export.xlsx` with required sheet tabs visible.
- How to prepare the app state: Download the improved export after loading demo records and applying review decisions, then open the workbook locally.
- Suggested filename: `14_improved_excel_workbook_sheets.png`
- Portfolio caption: The improved workbook separates export summary, approved improvements, pending suggestions, rejected suggestions, blocked suggestions, unknown suggestions, and the original source snapshot.
- Pass/fail notes: PASS if required sheet tabs are visible. FAIL if any planned sheet is missing.

Required workbook sheets:

- Export Summary
- Approved Improvements
- Pending Suggestions
- Rejected Suggestions
- Blocked Suggestions
- Unknown Suggestions
- Original Source Snapshot

### Screenshot 10.2 - Original Source Snapshot

- Purpose: Show source data protection.
- What to show: Original Source Snapshot sheet with original product rows and no merged approved values.
- How to prepare the app state: Open the improved Excel workbook and select the Original Source Snapshot sheet.
- Suggested filename: `15_original_source_snapshot.png`
- Portfolio caption: The source snapshot documents that the export keeps original product data separate from approved improvement candidates.
- Pass/fail notes: PASS if original fields are unchanged. FAIL if approved values appear merged into source columns.

## 11. Optional GitHub / Portfolio Screenshots

### Screenshot 11.1 - README Top Section

- Purpose: Show the GitHub landing explanation.
- What to show: README title, short product description, problem/value statement, and local MVP positioning.
- How to prepare the app state: Open the GitHub repository or local README preview.
- Suggested filename: `16_github_readme_top_section.png`
- Portfolio caption: The README explains the product, target workflow, and local MVP boundary for external reviewers.
- Pass/fail notes: PASS if the top section is understandable without scrolling far. FAIL if old branding or exaggerated production claims dominate.

### Screenshot 11.2 - Tests Passing Terminal

- Purpose: Show quality discipline.
- What to show: Terminal output from `python -m pytest` with passing test count.
- How to prepare the app state: Run `python -m pytest` locally after the repo is clean.
- Suggested filename: `17_pytest_passing_terminal.png`
- Portfolio caption: Automated tests cover extracted helper logic for validation, scoring, review, export, and AI suggestion safety behavior.
- Pass/fail notes: PASS if tests pass cleanly. FAIL if failures or secrets are visible.

### Screenshot 11.3 - Repository Structure

- Purpose: Show that the project is more than one loose script.
- What to show: File tree with `app.py`, `src/product_data_copilot/`, `tests/`, `data/`, and `docs/`.
- How to prepare the app state: Use VS Code Explorer or GitHub file browser.
- Suggested filename: `18_repo_structure.png`
- Portfolio caption: The project keeps the Streamlit app local-first while extracting testable helper modules and maintaining documentation.
- Pass/fail notes: PASS if core folders are visible. FAIL if private files, `.env`, or generated exports are visible.

### Screenshot 11.4 - Case Study Document

- Purpose: Show portfolio documentation depth.
- What to show: `docs/portfolio_case_study.md` rendered or opened with title and early sections visible.
- How to prepare the app state: Open the case study in GitHub, VS Code preview, or another Markdown renderer.
- Suggested filename: `19_portfolio_case_study_document.png`
- Portfolio caption: The case study explains the product problem, workflow, architecture, AI safety model, export safety, testing, limitations, and roadmap.
- Pass/fail notes: PASS if the document looks professional and honest. FAIL if it reads as production SaaS marketing.

## Final Screenshot Set Recommendation

For a concise portfolio page, use 6 to 8 screenshots:

1. Landing / upload area
2. Dashboard or readiness scores
3. Issues table
4. Review tasks
5. Smart Suggestions v2 structured table
6. Human approval states
7. Improved export preview
8. Excel workbook sheets

For a full GitHub case study, include the optional README, tests, repository structure, and case study screenshots as supporting evidence.

## Final Pass / Fail Criteria

PASS only if:

- Product name and value proposition are clear.
- Screenshots show product workflow, not random UI fragments.
- AI safety and human review are visible.
- Approved suggestions are clearly export candidates only.
- Export safety and source data protection are visible.
- No secrets, API keys, private file paths, or generated confidential files appear.
- The project looks like a polished local MVP, not a production SaaS claim.

FAIL if:

- Screenshots imply automatic AI approval.
- Screenshots imply source product data is overwritten.
- Old branding is prominent.
- Sensitive local/private data is visible.
- The selected screenshots hide the core product value.
