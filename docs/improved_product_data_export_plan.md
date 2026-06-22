# Improved Product Data Export Plan

## 1. Goal

Improved Product Data Export should let Product Data Copilot create a safe business handoff file that shows which product fields could be improved after human review.

The export must protect the original uploaded product data. It should never modify the source file, never auto-apply AI suggestions, and never pretend that draft or blocked suggestions are approved.

## 2. Exportable Data Later

Future improved export data should include:

- original source product rows
- current product readiness scores
- current product review status
- approved Smart Suggestions v2 records
- rejected Smart Suggestions v2 records
- blocked Smart Suggestions v2 records
- pending suggestions that still need review
- a field-level change summary for approved suggestions
- an audit trail showing that changes are proposed/exported, not written back

The first implementation should focus on Smart Suggestions v2 records because they are already field-level, parser-normalized, and human-review oriented.

## 3. Approved Smart Suggestions v2 Representation

Approved Smart Suggestions v2 records should be represented as field-level improvement rows.

Recommended columns:

- `sku`
- `product_name`
- `target_field`
- `original_value`
- `approved_value`
- `source_fields`
- `reason`
- `confidence`
- `risk_level`
- `approval_status`
- `suggestion_status`
- `review_decision_source`
- `export_status`

Important rules:

- `approval_status = approved` may only come from a user decision.
- AI-supplied `approved` values must remain downgraded to `needs_review`.
- blocked suggestions must never appear as approved changes.
- high-risk suggestions may be visible, but should require explicit human approval before inclusion as approved changes.

## 4. Protecting Original Uploaded Data

The original uploaded product data should remain read-only inside the workflow.

Protection rules:

- never overwrite uploaded CSV/XLSX files
- never mutate the source product DataFrame for export
- create derived export DataFrames only
- keep source values and proposed/approved values in separate columns
- clearly label export sheets as source, proposed, approved, rejected, or blocked
- keep session-only decisions separate from generated suggestion records

The export should act as a review artifact, not as a write-back mechanism.

## 5. Future Excel Workbook Sheets

Recommended future workbook name:

`product_data_copilot_improved_product_export.xlsx`

Recommended sheets:

### Export Summary

Purpose: management overview.

Suggested columns:

- `metric`
- `value`

Suggested metrics:

- total source products
- products with approved improvements
- approved improvement count
- pending suggestion count
- rejected suggestion count
- blocked suggestion count
- high-risk approved improvement count
- export generated from session state: Yes/No

### Source Products

Purpose: unchanged original product data.

Content:

- current uploaded product DataFrame
- no approved values merged into source columns

### Approved Improvements

Purpose: field-level approved changes.

Suggested columns:

- `sku`
- `product_name`
- `target_field`
- `original_value`
- `approved_value`
- `source_fields`
- `reason`
- `confidence`
- `risk_level`
- `approval_status`
- `suggestion_status`

### Proposed Improvements

Purpose: pending draft suggestions that still need review.

Suggested columns:

- `sku`
- `product_name`
- `target_field`
- `current_value`
- `proposed_value`
- `source_fields`
- `reason`
- `confidence`
- `risk_level`
- `approval_status`
- `suggestion_status`

### Rejected Suggestions

Purpose: preserve review context without applying changes.

Suggested columns:

- `sku`
- `product_name`
- `target_field`
- `current_value`
- `proposed_value`
- `reason`
- `rejection_status`

### Blocked Suggestions

Purpose: show unsafe or incomplete AI output.

Suggested columns:

- `sku`
- `product_name`
- `target_field`
- `current_value`
- `proposed_value`
- `source_fields`
- `reason`
- `risk_level`
- `suggestion_status`
- `block_reason`

### Audit Notes

Purpose: make export safety explicit.

Suggested rows:

- AI suggestions are draft recommendations.
- Approved suggestions were approved by the user in the current session.
- Source product data was not overwritten.
- No legal or compliance guarantee is provided.

## 6. Data State Definitions

### Source Product Data

The uploaded or sample product data as loaded into the app.

It is the baseline for comparison and must remain unchanged.

### Proposed Improvements

Parser-normalized Smart Suggestions v2 records with `needs_review`, `pending`, or review-required status.

They may be useful but are not approved and should not be used as final data.

### Approved Improvements

Smart Suggestions v2 records that a human explicitly approved in the current Streamlit session.

They are exportable as approved field-level changes, but should still not overwrite the source file automatically.

### Rejected / Blocked Suggestions

Rejected suggestions are user-reviewed but not accepted.

Blocked suggestions are unsafe, incomplete, unsupported, or insufficiently sourced and must not be approvable or exportable as approved improvements.

## 7. Session-Only State For Now

For the next implementation phase, these remain session-only:

- Smart Suggestions v2 generated records
- Smart Suggestions v2 fixture records
- Smart Suggestions v2 review decisions
- approved/rejected/pending decision state

No database or persistent review store should be introduced in this export phase.

## 8. What Must Not Happen

Do not implement:

- automatic mass changes
- write-back to source CSV/XLSX files
- invented AI facts
- AI self-approval
- export of blocked suggestions as approved changes
- database persistence
- SaaS/backend architecture
- marketplace integrations
- legal or compliance guarantees

## 9. Recommended Implementation Phases

### Phase 1: Export Plan Only

This document.

Outcome:

- agreed export goal
- sheet structure
- safety boundaries
- implementation phases

### Phase 2: Pure Helper Design / Tests

Create import-safe export helper functions under the existing export helper area.

Possible helpers:

- split V2 suggestions by human review status
- build approved improvements DataFrame
- build proposed improvements DataFrame
- build rejected suggestions DataFrame
- build blocked suggestions DataFrame
- build improved export summary DataFrame
- validate that blocked rows are never approved

Tests should run without Streamlit.

### Phase 3: Safe Export Preview

Add a preview-only section in the app.

Rules:

- show what would be exported
- use current session state
- no file write-back
- no source DataFrame mutation
- no change to existing management export

### Phase 4: Excel Export Implementation

Add the actual workbook download.

Rules:

- use in-memory `BytesIO`
- include every planned sheet even when empty
- keep existing exports unchanged
- clearly label source vs approved vs proposed vs blocked records
- no database
- no write-back

## 10. Acceptance Criteria For Future Implementation

- Source product data remains unchanged.
- Approved improvements are user-approved only.
- Blocked suggestions cannot appear in approved improvements.
- Empty sheets are still exported with stable columns.
- Existing CSV exports and Management Export remain unchanged unless explicitly extended.
- App works without `OPENAI_API_KEY`.
- The export is understandable for a product data manager or marketplace operations user.

## 11. Risks

- Confusing approved suggestions with written-back product data.
- Treating session-only approval as durable approval.
- Exporting blocked or unsafe suggestions in the wrong sheet.
- Making the export too complex before the V2 review workflow is stable.
- Overlapping with Management Export without clear naming.

Mitigation:

- keep the first implementation preview-focused
- add pure tests before UI/export wiring
- keep sheet names explicit
- keep source and approved values separate
- document that this is a local review artifact
