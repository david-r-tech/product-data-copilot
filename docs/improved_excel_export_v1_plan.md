# Improved Excel Export v1 Plan

## 1. Product Goal

Improved Excel Export v1 should create a clear workbook download for Smart Suggestions v2 review results.

The workbook should help product data managers and e-commerce operations teams review approved, pending, rejected, blocked, and unknown suggestion groups outside the app.

The export is a handoff artifact only. It must not write back to uploaded files, mutate product data, or apply AI suggestions automatically.

## 2. Workbook Name

Recommended filename:

`product_data_copilot_improved_export.xlsx`

The name should be distinct from the existing Management Export so users understand this workbook is focused on improved product data candidates.

## 3. Minimum Workbook Sheets

Improved Excel Export v1 should create these sheets:

1. `Export Summary`
2. `Approved Improvements`
3. `Pending Suggestions`
4. `Rejected Suggestions`
5. `Blocked Suggestions`
6. `Unknown Suggestions`
7. `Original Source Snapshot`

All sheets should exist even when empty. Empty sheets should still have stable columns.

## 4. Sheet Columns

### Export Summary

Purpose: give a quick overview of the current session export state.

Recommended columns:

- `metric`
- `value`

Recommended rows:

- `total_smart_suggestions_v2_records`
- `approved_improvement_count`
- `pending_suggestion_count`
- `rejected_suggestion_count`
- `blocked_suggestion_count`
- `unknown_suggestion_count`
- `source_product_count`
- `export_scope`
- `source_data_changed`
- `write_back_enabled`
- `generated_from_session_state`

Recommended fixed values:

- `export_scope`: `Smart Suggestions v2 review results`
- `source_data_changed`: `No`
- `write_back_enabled`: `No`
- `generated_from_session_state`: `Yes`

### Approved Improvements

Purpose: show field-level improvement candidates approved by the user.

Recommended columns should follow existing helper output:

- `sku`
- `product_name`
- `field`
- `current_value`
- `suggested_value`
- `original_value`
- `approved_value`
- `source`
- `reason`
- `confidence`
- `risk_level`
- `approval_status`
- `suggestion_status`
- `export_status`

Important: `approved_value` is an export candidate only. It is not applied to `Original Source Snapshot`.

### Pending Suggestions

Purpose: show suggestions that still need review.

Use the same stable helper columns as Approved Improvements.

These rows should be clearly treated as proposed/draft only.

### Rejected Suggestions

Purpose: preserve review context for suggestions that the user rejected.

Use the same stable helper columns as Approved Improvements.

Rejected rows should not be treated as improvement candidates.

### Blocked Suggestions

Purpose: show unsafe, incomplete, unsupported, or insufficiently sourced suggestions.

Use the same stable helper columns as Approved Improvements.

Blocked rows must never be included as approved improvements.

### Unknown Suggestions

Purpose: capture unexpected or incomplete statuses without losing audit visibility.

Use the same stable helper columns as Approved Improvements.

Unknown rows should stay separate from approved, pending, rejected, and blocked records.

### Original Source Snapshot

Purpose: provide the unchanged input product data for reference.

Columns should come from the currently loaded product DataFrame.

Rules:

- do not merge approved values into this sheet
- do not overwrite source fields
- do not create new product values here
- keep it as a snapshot of current app input data

## 5. Approved Suggestions As Export Candidates Only

Approved suggestions should be represented as field-level export candidates.

Rules:

- approval must come from user review state, not AI output
- `export_status = approved` identifies the candidate row
- `original_value` and `approved_value` must remain separate
- approved rows do not mutate source product rows
- approved rows are not automatically written back to CSV/XLSX

This keeps human review visible while avoiding automatic product data changes.

## 6. Source Data Protection

The Excel export should use derived DataFrames only.

Implementation rules:

- never modify the products DataFrame in place
- make a copy for `Original Source Snapshot`
- use `split_smart_suggestions_for_export(...)` for suggestion groups
- never write uploaded files
- never persist decisions outside the generated workbook
- never update sample data

## 7. Use Existing Export Helpers

The implementation should reuse:

- `split_smart_suggestions_for_export(...)`
- `smart_suggestions_to_export_dataframe(...)`
- `IMPROVED_EXPORT_STATUS_GROUPS`
- `IMPROVED_PRODUCT_EXPORT_COLUMNS`
- `safe_sheet_name(...)`

Do not duplicate export-splitting logic in `app.py`.

If new helper code is needed, it should live in `src/product_data_copilot/export/export_helpers.py` and be covered by pytest before Streamlit wiring.

## 8. Streamlit Fit

The download should fit into the existing Smart Suggestions v2 / Improved Product Data Export Preview area.

Recommended UI behavior:

- keep the existing preview section
- add the download button below the preview in a later implementation block
- label it clearly as an improved export
- explain that the workbook is generated from current session review state
- keep the existing Management Export unchanged

Recommended button label for later:

`Download Improved Product Data Excel Export`

Recommended file name:

`product_data_copilot_improved_export.xlsx`

## 9. Empty-State Behavior

When there are no Smart Suggestions v2 records:

- show a clear message in the preview
- disable or hide the future download button
- explain that the user should generate or load Smart Suggestions v2 records first

When there are suggestions but no approved rows:

- still allow a workbook only if the implementation chooses to export pending/rejected/blocked context
- clearly show `Approved Improvements` as empty
- keep pending/rejected/blocked sheets populated when relevant
- do not imply source product data was improved

Recommended v1 behavior:

- allow workbook generation when any Smart Suggestions v2 records exist
- include all sheets
- keep approved sheet empty if no rows are approved

## 10. Safety Boundaries

Do not implement:

- write-back to source files
- automatic product data mutation
- automatic application of AI suggestions
- AI self-approval
- database storage
- persistence beyond generated file download
- marketplace integration
- legal or compliance guarantees

The export is a local review artifact, not a publishing workflow.

## 11. Recommended Implementation Sequence

### Step 1: Helper-Level Workbook Builder Design / Tests

Add pure helper functions for:

- creating an export summary DataFrame
- building the workbook sheet mapping
- confirming expected sheet names
- confirming empty groups keep stable columns
- validating that blocked rows cannot appear in approved improvements

Tests should not launch Streamlit.

### Step 2: Streamlit Download Button Wiring

Add a download button in the current preview area.

Rules:

- use in-memory `BytesIO`
- use the helper-produced sheet mapping
- use `openpyxl`, already available through current dependencies
- do not change existing Management Export
- do not write files to disk

### Step 3: Manual QA Checklist

Manual QA should verify:

- app starts
- demo fixture rows can be loaded
- approving one row moves it to Approved Improvements
- rejected rows appear in Rejected Suggestions
- blocked rows appear in Blocked Suggestions
- source snapshot stays unchanged
- workbook opens in Excel or compatible spreadsheet software
- no existing exports changed

### Step 4: Documentation Update

Update:

- project log
- current context
- project status
- demo checklist, if the button becomes user-visible

## 12. Acceptance Criteria For Future Implementation

- workbook downloads as `.xlsx`
- all required sheets exist
- source snapshot is unchanged
- approved rows are user-approved only
- pending/rejected/blocked/unknown rows stay separate
- empty sheets retain stable columns
- no existing Management Export behavior changes
- app works without `OPENAI_API_KEY`
- no files are written except the user-triggered download stream
