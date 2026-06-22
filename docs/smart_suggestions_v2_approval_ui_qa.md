# Smart Suggestions v2 - Approval UI QA

## 1. Scope

This QA note reviews the Smart Suggestions v2 Approval UI after `Smart Suggestions v2 Approval UI v1`.

No runtime behavior changes are part of this QA block.

## 2. Current Approval UI Behavior

The current approval UI appears inside the existing Smart Suggestions v2 experimental section only when V2 records are available.

Current behavior:

- Shows V2 suggestions in a structured table.
- Adds `Human Review Status` as a session-only display state.
- Shows decision metrics for approved, rejected, pending, and blocked rows.
- Lets the user select one V2 suggestion at a time.
- Shows selected suggestion details.
- Lets the user approve, reject, or mark a non-blocked suggestion as pending.
- Keeps blocked suggestions visible but non-approvable.
- Stores review decisions separately in `st.session_state["smart_suggestions_v2_review_decisions"]`.

## 3. Manual Smoke Test Result Without API Key

Reported manual smoke test result: Passed without `OPENAI_API_KEY`.

Confirmed:

- The app starts successfully.
- V1 AI Suggestions still appears.
- Smart Suggestions v2 experimental section appears.
- V2 prompt preview appears.
- V2 structured suggestions table appears.
- Missing API key is handled safely.
- No red runtime error was visible.
- No V2 records were generated.

Because no V2 records were generated, the approval section could not be fully tested manually yet.

## 4. Full Approval Interaction Still Needs Records

The following behaviors still need manual verification with real V2 records or a future deterministic test fixture:

- approval section appears when records exist
- approve action changes a row to approved
- reject action changes a row to rejected
- mark pending clears a prior decision
- blocked rows cannot be approved
- review decisions do not leak between selected products
- session-only decisions disappear after app restart

## 5. Session-State-Only Approval Behavior

Approval decisions are stored separately from generated V2 records.

Current session key:

`smart_suggestions_v2_review_decisions`

This is aligned with the product safety goal:

- generated AI suggestions remain separate from human decisions
- approval is local to the current Streamlit session
- no product data is modified
- no database persistence is introduced
- no export behavior changes yet

## 6. Blocked-Row Behavior

Blocked rows are detected through `human_review_status = blocked`, which is derived from parser/safety output.

Expected behavior:

- blocked rows remain visible
- blocked rows show an explanatory warning
- blocked rows cannot be approved
- blocked rows are not written back or exported

This protects against unsafe or incomplete AI output being treated as usable product data.

## 7. V1 Preservation Check

V1 remains preserved because:

- V1 UI still appears above the V2 section.
- V1 prompt behavior was not changed.
- V1 session-state keys remain separate.
- V1 CSV export remains unchanged.
- V2 approval decisions use a separate session-state key.

## 8. Export / Write-Back Safety Check

No export or write-back behavior was added.

Current state:

- approved V2 suggestions do not update product data
- approved V2 suggestions are not exported
- rejected suggestions remain local review decisions
- blocked suggestions remain non-approvable
- Management Export is unchanged
- existing V1 AI Suggestions CSV export is unchanged

## 9. Known Limitations

- Approval UI cannot be fully tested without V2 records.
- There is no deterministic local fixture for V2 records yet.
- There is no approved-only export yet.
- There is no edit-before-approval workflow yet.
- There is no review note input yet.
- Decisions are session-only and disappear after restart.
- The approval UI still lives inside the larger `app.py` AI Suggestions tab code path.

## 10. Recommended Next Block

Recommended next block:

`Smart Suggestions v2 Test Fixture Planning`

Why this is the best next step:

- It enables deterministic testing and demo behavior without requiring an API key.
- It makes approval UI QA possible before export planning.
- It avoids jumping too early into approved-suggestion export or write-back.
- It keeps the current Streamlit/local-first scope.
- It supports portfolio quality because reviewers can see and test the human-in-the-loop workflow reliably.

## 11. Suggested Scope for Test Fixture Planning

The planning block should decide:

- whether to use a static local JSON fixture
- where the fixture should live
- whether fixture loading is dev/demo-only
- how to avoid confusing fixture data with real AI output
- how to test approved/rejected/blocked UI paths safely
- whether fixture use should be gated behind an expander or button

Do not implement fixture loading in the planning block.

## 12. Do Not Do Next

Do not jump directly into:

- approved-suggestion export
- improved product data export
- product data write-back
- database persistence
- login or roles
- SaaS/backend/productization

Those steps should come after deterministic approval UI testing is possible.
