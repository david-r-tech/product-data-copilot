# Commerce Readiness AI - Demo Script

> Historical walkthrough. Use the current [README](../README.md) and [release check](final_portfolio_release_checklist_v1.md) for the application workflow.

## 1. Start the App

Start the app with `start_app.bat` on Windows or run:

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` if the browser does not open automatically.

## 2. Load Sample Data

Start without uploading a file.

Point out that the app uses the built-in sample dataset and shows "Using: Sample data".

Explain that the sample file contains realistic e-commerce products with intentional data quality issues.

## 3. Explain the Dashboard

Open the Dashboard tab.

Show:

- Total products
- Total issues
- Products affected
- Critical, Warning, and Info issues
- Average readiness scores

Explain that this gives a quick management-level view of catalog readiness.

## 4. Open Issues

Open the Issues tab.

Show the severity filter and explain that teams can focus on Critical, Warning, or Info issues.

Point out examples such as missing category, invalid EAN, missing attributes, suspicious image URL, or missing warning notes.

## 5. Open Scores

Open the Scores tab.

Explain the multiple readiness scores:

- Data Quality
- Marketplace Readiness
- Translation Readiness
- Compliance Readiness
- AI Content Readiness
- Overall Readiness

Show how products can be compared quickly by score and review status.

## 6. Open Review Tasks

Open the Review Tasks tab.

Show the Product Review Overview, task priority metrics, products by review status, and top task types.

Use the filters for priority, task type, and review status to narrow the task table.

Explain that issues are translated into practical work items.

## 7. Apply Manual Review Override

In the Manual Review Status Override section:

1. Select one SKU.
2. Choose a status such as `Needs Review`, `Ready for Export`, or `Rejected`.
3. Click the apply button.

Show that the status is stored for the current Streamlit session and appears in the scores/review workflow.

## 8. Open AI Suggestions

Open the AI Suggestions tab.

Explain that the app selects the lowest-readiness product by default to focus AI support where it matters most.

If no API key is configured, show the missing-key fallback message and prompt preview.

If an API key is configured, generate suggestions for one selected product and show:

- Suggested title
- Suggested description
- Bullet points
- Missing attribute suggestions
- Review notes

Emphasize that AI suggestions are drafts and are not applied automatically.

## 9. Download Management Export

Open the Management Export tab.

Download `commerce_readiness_ai_management_export.xlsx`.

Explain that the workbook contains:

- Management Summary
- Product Scores
- Issues
- Review Tasks
- AI Suggestions
- Source Products

Close by explaining that this turns the audit into a practical handoff file for managers and operations teams.
