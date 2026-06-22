# Smart Suggestions v2 - Approval Workflow Plan

## 1. Goal

Plan a safe human approval workflow for Smart Suggestions v2 without implementing approval UI yet.

The workflow should help a user review one V2 suggestion at a time while preserving the current safety boundaries:

- AI can generate draft suggestions.
- AI can never approve itself.
- Only the user can approve.
- Approved suggestions do not update product data automatically yet.
- Export and write-back come later in separate phases.

## 2. Current Starting Point

Smart Suggestions v2 currently provides:

- an experimental section inside the existing AI Suggestions tab
- a V2 prompt preview
- a separate V2 generation button
- parser-normalized field-level rows
- business-friendly display labels and summary metrics
- review-required / blocked status display
- no approval UI
- no export or write-back behavior

## 3. User Review Flow

The first approval workflow should stay small and local to the existing V2 section.

Recommended user flow:

1. Select one product in the AI Suggestions tab.
2. Generate Smart Suggestions v2 for that product.
3. Review the structured V2 table.
4. Select one suggestion row from a dropdown.
5. Inspect its current value, suggested value, source fields, reason, confidence, risk, and state.
6. Choose one action:
   - Approve
   - Reject
   - Keep pending
7. See the updated approval state reflected in the V2 display.

Do not add bulk approve, bulk reject, edit fields, export, or write-back in the first implementation.

## 4. Approval States

Use these product-review states for the UI layer:

- `pending`: The suggestion still needs user review.
- `approved`: The user approved the suggestion for future export/use.
- `rejected`: The user rejected the suggestion.
- `blocked`: The suggestion is not approvable because it is unsafe, incomplete, unsupported, or lacks source information.

Mapping from current V2 parser output:

- `approval_status = needs_review` -> UI state `pending`
- `approval_status = rejected` -> UI state `rejected`
- `suggestion_status = blocked_insufficient_source` -> UI state `blocked`
- `approval_status = approved` should only happen from user action, not AI output

## 5. Safety Rules

Hard rules:

- AI can never approve itself.
- Parser-normalized AI output must never be displayed as user-approved by default.
- Blocked suggestions cannot be approved.
- High-risk suggestions can remain approvable only after explicit user action, but the UI should clearly show the risk.
- Approved suggestions still do not update product data automatically.
- Approved suggestions are session-state review decisions only until a separate export/write-back phase exists.

## 6. Separate Approval State Storage

Approval decisions should be stored separately from generated suggestion rows.

Recommended session-state key:

`smart_suggestions_v2_approval_overrides`

Recommended shape:

```python
{
    suggestion_key: {
        "sku": "...",
        "target_field": "...",
        "approval_state": "approved",
        "review_note": "",
    }
}
```

Suggested stable `suggestion_key`:

`sku | target_field | current_value | proposed_value`

Why separate storage matters:

- Keeps generated AI output immutable.
- Makes it clear that approval is a human decision.
- Supports future export logic without changing source product data.
- Allows rollback by clearing session state.

## 7. Rejected Suggestions

Rejected suggestions should:

- remain visible in the review session
- show `rejected` in the approval state
- not be included in future approved-only exports
- not update product data
- optionally allow a short review note later

Rejected suggestions should not be deleted in v1 because auditability matters.

## 8. Blocked Suggestions

Blocked suggestions should:

- remain visible for transparency
- show `blocked`
- not be approvable
- keep the reason visible
- not be exported as approved product data later

Blocked states should come from parser/safety behavior, not from user approval.

## 9. Approved Suggestions

Approved suggestions should:

- mean "approved by the current user in this local session"
- not overwrite the product table
- not modify uploaded data
- not modify sample data
- not change scores, issues, or review tasks
- be reserved for a later export workflow

Suggested UI copy:

`Approved means accepted for a future export step. It does not update product data automatically.`

## 10. Small UI Concept

Place a small section below the V2 structured table:

`Review one Smart Suggestion`

Suggested UI elements:

- Dropdown: Select suggestion row
- Read-only details:
  - Field
  - Current Value
  - Suggested Value
  - Source Fields
  - Reason
  - Confidence
  - Risk
  - Current Suggestion State
- Buttons or selectbox:
  - Keep pending
  - Approve suggestion
  - Reject suggestion
- Optional text input for review note can wait until later if scope feels large.

Blocked row behavior:

- Show blocked details.
- Disable approve behavior by showing an explanatory info/warning message.
- Allow only "Keep pending" or "Reject" if implementation stays simple; safest v1 can simply make blocked rows non-actionable.

## 11. Exact Next Implementation Scope

Next block:

`Smart Suggestions v2 Approval UI v1`

Allowed files:

- `app.py`
- `docs/codex_task_backlog.md`
- `docs/commerce_readiness_ai_project_log.md`
- `docs/project_status.md`
- `docs/current_context.md`

Do not modify:

- `src/`
- `tests/`
- `requirements.txt`
- `data/sample_products.csv`

Implementation boundaries:

- Add session-state-only approval overrides.
- Add one-suggestion-at-a-time review UI below the V2 table.
- Apply the override only to displayed V2 approval state.
- Keep blocked rows non-approvable.
- Do not export approval decisions yet.
- Do not update source product data.
- Do not change V1.

Acceptance criteria:

- V1 remains unchanged.
- V2 generation remains unchanged.
- User can review one V2 suggestion at a time.
- User can mark a non-blocked suggestion as pending, approved, or rejected.
- Blocked suggestions cannot be approved.
- Approval decisions are session-only.
- No exports change.
- No product data changes.

## 12. Manual Smoke Test Checklist

After implementation:

1. Run `python -m streamlit run app.py`.
2. Open the AI Suggestions tab.
3. Confirm V1 still appears unchanged.
4. Generate or load V2 suggestions.
5. Confirm the V2 table still appears.
6. Select one V2 suggestion.
7. Approve a non-blocked suggestion.
8. Reject a non-blocked suggestion.
9. Confirm a blocked suggestion cannot be approved.
10. Change selected product and confirm approval state does not leak incorrectly.
11. Confirm exports are unchanged.
12. Restart the app and confirm session-only approvals are not persisted.

## 13. Rollback Strategy

Keep implementation as one focused commit.

Rollback steps:

1. Revert the approval UI commit.
2. Run `python -m py_compile app.py`.
3. Run `python -m pytest`.
4. Start Streamlit manually.
5. Confirm the V2 generation/table still works as before.

If approval state display becomes confusing, stop and return to the table-only V2 workflow.

## 14. Explicit Later Phases

Do not implement now:

- approved-only CSV export
- Excel Management Export integration for V2 approvals
- improved product data preview
- product data write-back
- database persistence
- multi-user approvals
- login or roles
- deployment/backend work

Recommended later sequence:

1. Approval UI v1
2. Runtime QA for Approval UI
3. Improved Product Data Export Planning
4. Approved Suggestions Export v1
