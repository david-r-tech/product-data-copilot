# Core UX Manual QA v1

## Purpose

This checklist verifies the normal Product Data Copilot workflow after UX Polish Phase 1. It focuses on clarity, trust, and safe product workflow communication.

The removed German Furniture Demo is not part of this QA pass.

## Scope

Check only the active core product workflow:

`Upload -> Check -> Review -> Improve -> Approve -> Export`

Do not test removed demo flows, create new features, change product data logic, or adjust app behavior during this QA pass.

## Pre-Checks

- `git status` is clean before manual QA.
- `python -m py_compile app.py` passes.
- `python -m pytest` passes.
- App starts with:

```bash
python -m streamlit run app.py
```

## Manual Browser QA

### 1. Startup And First Impression

**Pass if:**

- Product Data Copilot logo or fallback title is visible.
- The short product caption is understandable.
- The workflow line is visible: `Upload -> Check -> Review -> Improve -> Approve -> Export`.
- No old `DE Demo` tab is visible.
- No red Streamlit error appears on startup.

**Fail if:**

- The app still presents the removed German Furniture Demo as active.
- The first screen does not make the product purpose understandable.

### 2. Upload And Sample Data

**Pass if:**

- Sidebar upload accepts CSV/XLSX.
- Sidebar text explains upload and sample-data fallback.
- With no upload, sample data loads automatically.
- Data source notice clearly says the app is using sample data.
- Product Data tab shows rows and columns without confusing empty states.

**Fail if:**

- Upload guidance implies source data will be overwritten.
- Sample data fails to load.

### 3. Dashboard

**Pass if:**

- Dashboard metrics render.
- Total products, total issues, and affected products are visible.
- Critical/warning/info issue counts are visible.
- Average readiness scores are visible.
- The new business interpretation message is understandable.

**Fail if:**

- Dashboard suggests product data is automatically fixed.
- Score wording is misleading or contradicts the table values.

### 4. Product Data

**Pass if:**

- Product Data tab shows the loaded source table.
- Copy makes clear that this is source data.
- Copy makes clear AI/export flows do not automatically change this table.

**Fail if:**

- The UI implies uploaded data is mutated automatically.

### 5. Scores

**Pass if:**

- Product Readiness Scores tab renders.
- Readiness score copy is understandable for a business user.
- Download Product Readiness Scores still appears.
- Score values and review statuses remain visible.

**Fail if:**

- Score display breaks.
- Existing score download is missing.

### 6. Issues

**Pass if:**

- Data Quality Issues tab renders.
- Severity filter still affects visible issues.
- Copy explains that issues are grouped by severity.
- Download Data Quality Issues still appears.

**Fail if:**

- Filtering breaks.
- Empty states are confusing.

### 7. Review Tasks

**Pass if:**

- Review Tasks tab renders.
- Product Review Overview is understandable.
- `Set Product Review Status` feels business-facing, not overly technical.
- Status changes remain session-only.
- Priority, task type, and review status filters still work.
- Download Review Tasks exports the filtered view.

**Fail if:**

- Review wording implies permanent database storage.
- Session-only behavior no longer works.
- Task generation or priorities appear changed.

### 8. Management Export

**Pass if:**

- Management Export tab renders.
- Copy explains that Management Export is an audit/reporting workbook.
- Management Summary Preview renders.
- Excel Management Export download still appears.
- Export includes reporting context, not source write-back behavior.

**Fail if:**

- Export copy implies automatic publishing or product mutation.
- Download button is missing or broken.

### 9. AI Suggestions V1

**Pass if:**

- AI Suggestions tab renders.
- Classic AI Suggestions v1 section is distinguishable.
- Missing `OPENAI_API_KEY` fallback is understandable.
- Prompt preview remains available when generation is disabled.
- AI suggestions are clearly described as drafts.
- Raw AI response, when present, stays inside an expander.

**Fail if:**

- V1 behavior changes.
- UI suggests AI output is automatically accepted.

### 10. Smart Suggestions V2

**Pass if:**

- Smart Suggestions v2 experimental section is visible but not more prominent than the core workflow.
- Prompt preview remains inside an expander.
- Demo fixture loader still works without an API key.
- Structured table shows source, reason, confidence, risk, and review status fields.
- Empty state tells the user what to do next.

**Fail if:**

- V2 output is presented as automatically trusted.
- Missing/blocked suggestions appear approvable.

### 11. Human Approval UI

**Pass if:**

- Human Review for Smart Suggestions v2 appears when records exist.
- One suggestion can be selected.
- Approve, reject, and pending actions are understandable.
- Blocked rows cannot be approved.
- Copy makes clear approval is session-only.
- Approved means export candidate only.

**Fail if:**

- AI can approve itself.
- Approval state is shown as permanent persistence.
- Product data is changed automatically.

### 12. Improved Product Data Export

**Pass if:**

- Improved Product Data Export Preview renders when suggestions exist.
- Approved, pending, rejected, blocked, and unknown groups are understandable.
- Copy makes clear the preview is safe.
- Download Improved Product Data Export creates a separate workbook.
- Original Source Snapshot is included in the workbook.
- Approved suggestions are export candidates only.

**Fail if:**

- Export overwrites source data.
- Export copy implies write-back.
- Download breaks when there are no approved suggestions.

## Acceptance Criteria

PASS only if:

- The core workflow is understandable without explaining the removed German demo.
- The user can identify where to upload, check, review, improve, approve, and export.
- AI safety and export safety are visible.
- Existing app behavior still works.
- No automatic write-back or auto-approval is implied.

FAIL if:

- The removed German Furniture Demo is still visible as active product functionality.
- The UI implies automatic product data changes.
- The UI implies AI suggestions are trusted without human review.
- Any core tab shows a red runtime error.

## Recommended QA Notes To Capture

- Browser and viewport size used.
- Whether sample data or uploaded file was used.
- Any confusing wording that remains.
- Any table that feels too wide or dense.
- Whether screenshots are ready for portfolio capture.

## Next Step After QA

If this checklist passes, the next safe product block is `Data Table Readability v1`.
