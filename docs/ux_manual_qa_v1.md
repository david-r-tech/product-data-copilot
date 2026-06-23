# UX Manual QA v1 Checklist

This checklist verifies the current Product Data Copilot UI after `UX Copy Polish v1`.

The goal is to confirm that the app communicates product value, AI safety, review workflow, and export safety clearly in a real browser walkthrough.

## 1. Start the App

- [ ] Run:

```bash
python -m streamlit run app.py
```

- [ ] Confirm the app opens without red runtime errors.
- [ ] Confirm the app remains usable without `OPENAI_API_KEY`.
- [ ] Confirm the main tabs are visible:
  - Dashboard
  - Product Data
  - Scores
  - Issues
  - Review Tasks
  - Management Export
  - AI Suggestions

Expected result:

- App starts successfully.
- No login, database, backend, or setup beyond local dependencies is required.

## 2. Initial Landing Impression

- [ ] Confirm the primary visible product name is Product Data Copilot.
- [ ] Confirm the value proposition is understandable: product data quality checks for e-commerce readiness.
- [ ] Confirm `Commerce Readiness AI` appears only as historical context, not as the primary brand.
- [ ] Confirm the app does not feel like a raw script or unfinished prototype on first view.

Expected result:

- Product identity is clear.
- The user can understand what the app does within a few seconds.

## 3. Sample Data Workflow

- [ ] Start with no uploaded file.
- [ ] Confirm sample data loads automatically.
- [ ] Confirm the current data source notice is understandable.
- [ ] Confirm upload/sample behavior is clear from the sidebar or data input area.
- [ ] Confirm no confusing empty state appears while sample data is loaded.

Expected result:

- Sample workflow feels intentional.
- Users understand they can either use sample data or upload CSV/XLSX.

## 4. Product Checks and Results

- [ ] Open the Dashboard tab.
- [ ] Confirm total products, issues, affected products, and average scores are understandable.
- [ ] Open the Scores tab.
- [ ] Confirm score names are understandable enough for a product/data audience.
- [ ] Open the Issues tab.
- [ ] Confirm issue table language is clear.
- [ ] Confirm severity wording is understandable: Critical, Warning, Info.
- [ ] Confirm issue filters do not create confusing empty states.

Expected result:

- Product readiness results are understandable without reading code.
- Severity and status language feels professional and practical.

## 5. Review Tasks / Review Workflow

- [ ] Open the Review Tasks tab.
- [ ] Confirm review task language is understandable.
- [ ] Confirm task priority labels are clear.
- [ ] Confirm review status wording is clear.
- [ ] Test the manual review status override.
- [ ] Confirm manual override wording does not imply source data is changed.
- [ ] Confirm filtered review task export still makes sense as a workflow artifact.

Expected result:

- The review workflow feels like a task-management aid.
- No automatic data change is implied.

## 6. AI Suggestions v1

- [ ] Open the AI Suggestions tab.
- [ ] Confirm the selected product is understandable.
- [ ] Confirm the app explains that AI suggestions are draft recommendations.
- [ ] Confirm the missing API key fallback is understandable when `OPENAI_API_KEY` is not set.
- [ ] Confirm prompt preview remains available without an API key.
- [ ] Confirm no wording implies factual invention or automatic application.
- [ ] If an API key is available, generate one suggestion and confirm the result still appears as draft content.

Expected result:

- AI Suggestions v1 feels safe and human-reviewed.
- Missing API key state does not feel broken.

## 7. Smart Suggestions v2

- [ ] Confirm `Smart Suggestions v2 (experimental)` is visible and clearly separate from AI Suggestions v1.
- [ ] Confirm the section explains structured field-level draft suggestions.
- [ ] Confirm the text says V2 does not approve, publish, or update product data automatically.
- [ ] Confirm the recommended demo flow is understandable.
- [ ] Open the prompt preview and confirm it remains collapsed by default.
- [ ] Open the demo fixture expander and confirm fixture data is clearly labeled as demo/test data.
- [ ] Load demo Smart Suggestions v2 records without an API key.
- [ ] Confirm confidence, source fields, reason, risk, human review status, and suggestion state are visible or understandable.

Expected result:

- Smart Suggestions v2 feels like a controlled review workflow.
- Demo fixture use is understandable and not confused with real AI output.

## 8. Human Approval UI

- [ ] Confirm the Human Review section appears after V2 records exist.
- [ ] Select one suggestion.
- [ ] Confirm selected suggestion details are understandable:
  - SKU
  - Product
  - Field
  - Current Value
  - Suggested Value
  - Reason
  - Source Fields
  - Confidence
  - Risk
  - Current Review Status
- [ ] Approve one non-blocked suggestion.
- [ ] Reject one non-blocked suggestion.
- [ ] Mark one suggestion as pending.
- [ ] Select a blocked suggestion.
- [ ] Confirm blocked suggestions cannot be approved.
- [ ] Confirm session-only limitation is clear.
- [ ] Confirm approved means export candidate only.

Expected result:

- Human approval is understandable.
- AI never appears to approve itself.
- Approval does not imply product data write-back.

## 9. Improved Product Data Export

- [ ] Scroll to Improved Product Data Export Preview.
- [ ] Confirm the preview copy is clear.
- [ ] Confirm it says no product data is changed and no source file is overwritten.
- [ ] Confirm approved, pending, rejected, blocked, and unknown groups are understandable.
- [ ] Confirm no-approved state is understandable.
- [ ] Confirm download copy explains that the workbook uses the preview groups.
- [ ] Download `product_data_copilot_improved_export.xlsx`.
- [ ] Confirm no source write-back is implied.
- [ ] Confirm approved suggestions remain export candidates only.

Expected result:

- Improved export feels like a safe handoff artifact.
- It does not look like an automatic product update workflow.

## 10. Empty States

Check these empty states:

- [ ] No uploaded data: sample-data fallback is understandable.
- [ ] No suggestions: user knows to load demo records or generate V2 suggestions.
- [ ] No approved suggestions: user understands Approved Improvements will be empty until approval.
- [ ] Missing API key: user understands generation is disabled but demo records and prompt preview remain available.
- [ ] No matching issue/review filters: user understands the filter result is empty, not broken.

Expected result:

- Empty states tell the user what is missing and what to do next.

## 11. Portfolio Presentation

- [ ] App feels coherent across tabs.
- [ ] App feels safe and trustworthy.
- [ ] App does not look like a rough demo.
- [ ] Product, review, AI, and export concepts are understandable for a non-code reviewer.
- [ ] Safety boundaries are visible without overwhelming the user.
- [ ] No unsupported product claims are visible.

Expected result:

- The app is presentable in a portfolio walkthrough.
- The product story is understandable without reading implementation details.

## 12. Pass / Fail Criteria

PASS only if:

- The current UI communicates product value clearly.
- AI safety is clear.
- Review workflow is understandable.
- Export safety is clear.
- Smart Suggestions v2 is clearly draft-only and human-reviewed.
- Approved suggestions are clearly export candidates only.
- Original/source product data is not presented as overwritten.
- Old `Commerce Readiness AI` branding is not prominent.
- Major empty states are understandable.

FAIL if:

- The UI suggests AI suggestions are automatically applied.
- The UI suggests source product data is overwritten.
- The UI suggests AI can approve its own suggestions.
- Old branding is still prominent.
- Major empty states are confusing.
- Review decisions appear persistent when they are session-only.
- Improved export appears to be a write-back workflow.

## 13. Manual QA Notes

Use this section during a real browser QA run:

- Tester:
- Date:
- App commit:
- Browser:
- API key present: Yes / No
- Demo fixture tested: Yes / No
- Improved export downloaded: Yes / No
- Result: PASS / FAIL
- Notes:
