# Improved Export Manual QA Checklist

This checklist verifies the improved Excel export for Smart Suggestions v2 review results.

The export must remain a review handoff artifact only. It must not update source product data, write back to uploaded files, persist decisions in a database, or apply AI suggestions automatically.

## 1. Start the App

- [ ] Run:

```bash
python -m streamlit run app.py
```

- [ ] Confirm the app opens without red runtime errors.
- [ ] Confirm the visible product name is Product Data Copilot.
- [ ] Confirm the main tabs still appear.

Expected result:

- App starts successfully.
- No database, login, persistence, or backend step is required.

## 2. Load Sample Data

- [ ] Start with no uploaded file.
- [ ] Confirm the app uses sample data.
- [ ] Confirm product data, dashboard metrics, scores, issues, and review tasks still render.

Expected result:

- Sample data loads normally.
- Existing product audit workflow is unchanged.

## 3. Open Smart Suggestions v2 Area

- [ ] Open the AI Suggestions tab.
- [ ] Confirm AI Suggestions v1 still appears.
- [ ] Confirm Smart Suggestions v2 is clearly labeled experimental.
- [ ] Confirm Smart Suggestions v2 explains that suggestions need human review.
- [ ] Confirm the prompt preview is available.

Expected result:

- V1 is still present.
- V2 appears as a separate experimental section.
- The UI does not imply automatic approval or automatic product data changes.

## 4. Load Demo Smart Suggestions v2 Fixture

- [ ] Open the Demo fixture expander.
- [ ] Click `Load demo Smart Suggestions v2 records`.
- [ ] Confirm demo rows appear in the Smart Suggestions v2 table.
- [ ] Confirm the UI labels the rows as deterministic demo/test data.
- [ ] Confirm this works without `OPENAI_API_KEY`.

Expected result:

- Demo fixture rows load without an API key.
- Rows are not presented as real AI output.
- No export or source product data is changed by loading the fixture.

## 5. Review Suggestion States

- [ ] Approve at least one non-blocked suggestion.
- [ ] Reject at least one non-blocked suggestion.
- [ ] Leave at least one suggestion pending.
- [ ] Confirm at least one blocked suggestion is visible.
- [ ] Try to approve a blocked suggestion if the UI allows selecting it.

Expected result:

- Approved row shows as approved in the session.
- Rejected row shows as rejected in the session.
- Pending row remains pending.
- Blocked row cannot be approved.
- Review decisions are session-only.
- Approved suggestions do not update product data.

## 6. Verify Improved Product Data Export Preview

- [ ] Scroll to `Improved Product Data Export Preview`.
- [ ] Confirm the preview says it is preview/export-candidate oriented.
- [ ] Confirm approved, pending, rejected, blocked, and unknown groups are shown when data exists.
- [ ] Confirm approved suggestions appear only as export candidates.
- [ ] Confirm blocked suggestions stay separate from approved suggestions.
- [ ] Confirm source product data is not changed in the app after approval/rejection.

Expected result:

- Preview groups match the current review decisions.
- Approved rows are separated from pending, rejected, blocked, and unknown rows.
- The UI wording makes it clear no source file is overwritten.

## 7. Download the Improved Excel Export

- [ ] Click `Download Improved Product Data Export`.
- [ ] Save the file:

```text
product_data_copilot_improved_export.xlsx
```

- [ ] Open the workbook in Excel, LibreOffice, or another spreadsheet tool.

Expected result:

- Workbook downloads as `.xlsx`.
- Workbook opens without repair prompts or obvious corruption.

## 8. Verify Workbook Sheets

Confirm these sheets exist:

- [ ] `Export Summary`
- [ ] `Approved Improvements`
- [ ] `Pending Suggestions`
- [ ] `Rejected Suggestions`
- [ ] `Blocked Suggestions`
- [ ] `Unknown Suggestions`
- [ ] `Original Source Snapshot`

Expected result:

- All planned sheets exist.
- Empty sheets are still present when there are no rows for a group.

## 9. Verify Workbook Content

### Export Summary

- [ ] Confirm total Smart Suggestions v2 count matches the demo/generated rows.
- [ ] Confirm approved, pending, rejected, blocked, and unknown counts are understandable.
- [ ] Confirm `source_data_changed` is `No`.
- [ ] Confirm `write_back_enabled` is `No`.

### Approved Improvements

- [ ] Confirm approved suggestions appear as rows.
- [ ] Confirm `approved_value` is populated only for approved rows.
- [ ] Confirm approved rows include source/current value context.

### Pending Suggestions

- [ ] Confirm pending suggestions are present if any were left pending.
- [ ] Confirm pending rows are not treated as approved.

### Rejected Suggestions

- [ ] Confirm rejected suggestions are present if any were rejected.
- [ ] Confirm rejected rows are not treated as approved.

### Blocked Suggestions

- [ ] Confirm blocked suggestions are present if fixture/generated data includes blocked rows.
- [ ] Confirm blocked rows do not appear in `Approved Improvements`.

### Unknown Suggestions

- [ ] Confirm unknown rows stay separate if any exist.

### Original Source Snapshot

- [ ] Confirm original product rows are present.
- [ ] Confirm source product values are unchanged.
- [ ] Confirm approved values are not merged into source columns.

Expected result:

- Workbook is a review artifact.
- Source snapshot remains unchanged.
- Suggestions are separated by status.

## 10. Empty / No-Approved State

Repeat once with V2 records loaded but no approved suggestions:

- [ ] Load demo fixture records.
- [ ] Do not approve any suggestion.
- [ ] Download the workbook.
- [ ] Confirm `Approved Improvements` exists but is empty.
- [ ] Confirm pending/rejected/blocked/unknown context remains available when relevant.
- [ ] Confirm UI copy explains there are no approved export candidates yet.

Expected result:

- No-approved state is understandable.
- Download does not imply product data was improved.
- Workbook remains valid.

## 11. Existing Export Safety

- [ ] Confirm existing CSV exports still appear where expected.
- [ ] Confirm existing Excel Management Export still appears.
- [ ] Confirm no existing export names or behavior changed unexpectedly.

Expected result:

- Improved Excel Export is additive.
- Existing exports remain unchanged.

## 12. Pass / Fail Criteria

PASS only if:

- App starts successfully.
- Demo or generated Smart Suggestions v2 rows can be reviewed.
- Improved Product Data Export Preview groups rows correctly.
- `product_data_copilot_improved_export.xlsx` downloads and opens.
- All planned workbook sheets exist.
- Approved suggestions are separated as export candidates only.
- Original source data remains unchanged.
- UI copy makes source protection and human review clear.
- No database, persistence, write-back, or automatic product data modification exists.

FAIL if:

- Any approved suggestion is silently applied to source product data.
- The UI suggests automatic product data changes.
- Blocked suggestions appear as approved improvements.
- Download breaks empty-state or no-approved scenarios.
- The workbook omits required sheets.
- The source snapshot includes approved values merged into source columns.
- Existing exports break or disappear.

## 13. Manual QA Notes

Use this section during a real QA run:

- Tester:
- Date:
- App commit:
- Browser:
- Workbook opened with:
- Result: PASS / FAIL
- Notes:
