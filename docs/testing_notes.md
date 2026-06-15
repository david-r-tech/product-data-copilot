# Commerce Readiness AI - Testing Notes

## Purpose

This document summarizes how the current local MVP should be checked before a demo, portfolio review, or GitHub update.

It does not introduce a new test framework. The goal is to keep verification simple, repeatable, and understandable.

## Technical Checks

Run these commands from the project root:

```bash
python -m py_compile app.py
```

Expected result: command finishes without errors.

```bash
python -c "import pandas as pd; df = pd.read_csv('data/sample_products.csv'); print(df.shape)"
```

Expected result:

```text
(25, 14)
```

## Manual Smoke Test

Start the app:

```bash
python -m streamlit run app.py
```

Confirm:

- The app opens locally.
- The app shows "Using: Sample data" when no file is uploaded.
- Dashboard metrics are visible.
- Product Data, Scores, Issues, Review Tasks, Management Export, and AI Suggestions tabs render.
- No API key is required to open the app.

## Functional Acceptance Checks

- CSV upload works.
- XLSX upload works.
- Product data issues are detected.
- Severity filter updates the Issues table.
- Readiness scores are visible.
- Review tasks are generated.
- Review task filters work.
- Manual review status override updates the current session display.
- CSV downloads are available.
- Management Excel Export downloads successfully.
- AI Suggestions tab shows a clear missing-key fallback when `OPENAI_API_KEY` is not configured.
- AI Suggestions are not automatically written back to source product data.

## Documentation Checks

Before sharing the repository, confirm:

- README explains problem, users, setup, features, scope, limits, and demo flow.
- `docs/product_requirements.md` reflects current app behavior.
- `docs/demo_test_checklist.md` can be used for a full demo walkthrough.
- `docs/screenshots_to_capture.md` lists the screenshots still needed.
- `.env` is ignored and `.env.example` contains only placeholder values.

## Known Manual Checks

These checks currently require manual confirmation:

- Downloaded Excel workbook opens correctly.
- UI layout looks readable in the browser.
- Screenshots are captured and added later if desired.
- AI generation works with a valid local API key.
