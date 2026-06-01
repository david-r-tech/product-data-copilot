# Commerce Readiness AI - Demo Test Checklist

## 1. Start the app

- Start with `start_app.bat` on Windows
- Alternative command: `python -m streamlit run app.py`
- Open `http://localhost:8501` if the browser does not open automatically

## 2. Validate sample data load

- Confirm the app shows "Using: Sample data"
- Confirm the sample dataset loads with around 25 products
- Confirm categories include Apparel, Electronics, Home & Kitchen, Sports & Outdoors, Office, Toys, Beauty / Personal Care, and Pet Supplies
- Confirm dashboard metrics are visible

## 3. Follow the end-to-end demo path

- Open Dashboard and explain catalog health
- Open Product Data and show the sample products
- Open Issues and filter by severity
- Open Scores and explain multiple readiness scores
- Open Review Tasks and filter operational work
- Apply one manual review status override
- Open Management Export and download the Excel workbook
- Open AI Suggestions and show the missing-key fallback or generate one suggestion if an API key is configured

## 4. Check main tabs

- Dashboard
- Product Data
- Scores
- Issues
- Review Tasks
- Management Export
- AI Suggestions

## 5. Check dashboard

- Total products visible
- Total issues visible
- Products affected visible
- Average overall score visible

## 6. Check Product Data tab

- Product table is visible
- New demo columns are present, including `manufacturer` and `attributes`
- Sample data includes realistic clean products and intentionally imperfect products

## 7. Check Scores tab

- Multiple readiness score columns visible:
  - `data_quality_score`
  - `marketplace_readiness_score`
  - `translation_readiness_score`
  - `compliance_readiness_score`
  - `ai_content_readiness_score`
  - `overall_readiness_score`
  - `review_status`
- CSV download works

## 8. Check Issues tab

- Issues table visible
- Severity filter works
- New issue types visible, such as Missing category, Missing price, Invalid price, Invalid ean, Generic product_name, Image URL suspicious, Missing manufacturer, or Missing attributes
- CSV download works

## 9. Check Review Tasks tab

- Review task table visible
- Product Review Overview visible
- Products by review status visible
- Tasks by priority visible
- Top task types visible
- Filters for Priority, Task type, and Review status work
- Manual Review Status Override can be saved for one product
- Manual override appears in the Product Readiness Scores table after save
- Priority, issue type, and field name columns are visible
- Task types such as Commercial Review, Attribute Enrichment, Media Improvement, and Data Completion are visible
- CSV download exports the currently filtered task table

## 10. Check Management Export tab

- Management Export tab opens
- Management Summary Preview is visible
- Excel download works
- Downloaded workbook contains Management Summary, Product Scores, Issues, Review Tasks, AI Suggestions, and Source Products sheets
- Downloaded workbook includes current issues and review tasks
- Downloaded workbook includes effective review_status values
- App does not require an API key to create the Excel export

## 11. Check AI Suggestions without API key

- AI Suggestions tab opens
- Product with lowest readiness score is selected by default
- Compact selected product context is visible
- Suggestion type selection is visible
- Missing-key message appears:
  "AI generation requires an API key. AI suggestions are disabled because OPENAI_API_KEY is missing."
- Prompt preview is available
- Human-in-the-loop draft warning is visible
- App does not crash

## 12. Optional: Check AI Suggestions with API key

- Create local `.env` from `.env.example`
- Set `OPENAI_API_KEY` locally
- Restart app
- Select one or more suggestion types
- Generate suggestions for one selected product
- Confirm structured AI suggestion sections appear
- Confirm AI suggestions CSV export works
- Confirm AI suggestions are not automatically applied to product data
- Confirm Management Excel Export still works after generating suggestions

## 13. Screenshot checklist

- Dashboard screenshot
- Product Data screenshot
- Scores screenshot
- Issues screenshot with severity filter
- Review Tasks screenshot with filters
- Manual Review Status Override screenshot
- Management Export screenshot
- AI Suggestions missing-key or generated-suggestion screenshot
