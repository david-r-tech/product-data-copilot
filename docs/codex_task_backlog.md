# Codex Task Backlog - Product Data Copilot

This backlog is a lightweight execution guide for the next safe refactor and quality blocks.

Work on one block at a time. Do not start the next block unless the user explicitly requests it.

| Order | Block | Status | Goal |
| --- | --- | --- | --- |
| 1 | Extract Scoring Helpers v1 | Done | Created small import-safe scoring helpers and pytest coverage without changing app behavior. |
| 2 | Extract Review Helpers v1 | Done | Moved pure review mapping/status helper logic into an import-safe module with tests. |
| 3 | Extract Export Helpers v1 | Done | Moved pure export preparation helpers into an import-safe module with tests. |
| 4 | Extract AI Prompt Helpers v1 | Done | Moved pure prompt-building support helpers into an import-safe module with tests. |
| 5 | App Slimdown v1 | Planning Done | Created a safe phased plan for making `app.py` thinner while preserving behavior. |
| 6 | App Slimdown v1 - Phase 1 | Done | Created the Streamlit entrypoint wrapper while keeping behavior unchanged. |
| 7 | App Slimdown v1 - Phase 2 | Done | Extracted minimal Streamlit layout/setup intro helpers with focused tests. |
| 8 | App Slimdown v1 - Phase 3 | Done | Extracted small data input/source notice UI helpers with focused tests. |
| 9 | App Slimdown v1 - Phase 4 | Done | Extracted small status/summary UI helpers with focused tests. |
| 10 | App Slimdown v1 - Phase 5 | Done | Finalized App Slimdown v1 as a safe stop point and documented what remains in `app.py`. |
| 11 | Helper Integration v1 - Planning | Done | Planned how already extracted helpers can be wired into `app.py` safely without behavior changes. |
| 12 | Helper Integration v1 - Phase 1: Validators | Done | Wired tested validator helpers into `app.py` with behavior-preserving checks. |
| 13 | Helper Integration v1 - Phase 2: Scoring | Done | Wired tested scoring helpers into `app.py` after validator integration stayed stable. |
| 14 | Helper Integration v1 - Phase 3: Review Helpers | Done | Wired tested review helpers into `app.py` after scoring integration stayed stable. |
| 15 | Helper Integration v1 - Phase 4: Export Helpers | Done | Wired tested export constants into `app.py` while preserving export behavior. |
| 16 | Helper Integration v1 - Phase 5: AI Prompt Helpers | Done | Wired narrow AI prompt safety helpers into `app.py` while preserving current AI behavior. |
| 17 | Helper Integration v1 - Finalization | Done | Reviewed completed helper integration, documented final state, and prepared the next safe planning block. |
| 18 | Smart Suggestions v2 - Planning | Done | Planned a safer structured AI suggestion model without implementation or app behavior changes. |
| 19 | Smart Suggestions v2 - Phase 1: Schema Helpers | Done | Created pure field-level suggestion schema and contract helpers with tests without changing app behavior. |
| 20 | Smart Suggestions v2 - Phase 2: Contract & Parser Helpers | Done | Added safe response parser/normalization helpers for future field-level AI responses without runtime wiring. |
| 21 | Smart Suggestions v2 - Phase 3: Prompt Contract Planning | Done | Planned how to update the AI prompt contract for field-level suggestions before runtime integration. |
| 22 | Smart Suggestions v2 - Phase 4: Runtime Prompt Adapter | Done | Added a tested prompt adapter for field-level suggestions while preserving current runtime behavior. |
| 23 | Smart Suggestions v2 - Phase 5: Structured Response Normalization Review | Done | Reviewed and hardened schema/parser behavior against the prompt adapter contract before runtime wiring. |
| 24 | Smart Suggestions v2 - Phase 6: Runtime Integration Planning | Done | Planned the safest path for wiring Smart Suggestions v2 into the existing AI Suggestions tab without changing runtime behavior yet. |
| 25 | Smart Suggestions v2 - Phase 7: Experimental UI Wiring | Done | Added a clearly separated experimental V2 prompt preview and schema-stable structured suggestions table inside the existing AI Suggestions tab. |
| 26 | Smart Suggestions v2 - Phase 8: Controlled Runtime Generation Planning | Done | Planned the separate V2 runtime generation flow, API-key fallback, parser handling, session-state keys, error display, and rollback strategy. |
| 27 | Smart Suggestions v2 - Phase 9: Controlled Runtime Generation | Done | Added a separate V2 generate button, separate session state, parser normalization, safe error display, and raw-response review expander without changing V1 or exports. |
| 28 | Smart Suggestions v2 - Phase 10: Runtime QA and Next-Step Planning | Done | Documented V2 runtime QA, manual smoke-test result, V1 preservation, session-state separation, parser safety, limitations, and next product block. |
| 29 | Smart Suggestions v2 Result UX Polish | Done | Improved V2 copy, empty states, status explanations, summary metrics, and business-friendly table labels without changing generation, approval, export, or write-back behavior. |
| 30 | Smart Suggestions v2 Approval Workflow Planning | Done | Planned a session-state-only human approval workflow with pending, approved, rejected, and blocked states while preserving V1, exports, and product data. |
| 31 | Smart Suggestions v2 Approval UI v1 | Done | Added a session-only one-suggestion-at-a-time review UI for pending/approved/rejected decisions, with blocked rows non-approvable and no export/write-back scope. |
| 32 | Smart Suggestions v2 Approval UI QA | Done | Documented approval UI QA findings, missing-key smoke test result, untested record-dependent paths, session-state safety, blocked-row behavior, V1 preservation, and export/write-back boundaries. |
| 33 | Smart Suggestions v2 Test Fixture Planning | Done | Planned deterministic parser/demo fixture support so approval UI states can be tested without an API key before export planning. |
| 34 | Smart Suggestions v2 Test Fixture v1 | Done | Added a deterministic JSON fixture, parser test coverage, and clearly labeled Streamlit demo fixture loader without export/write-back scope. |
| 35 | Smart Suggestions v2 Fixture QA | Done | Documented fixture coverage, parser test coverage, demo loader behavior, approval UI testability, safety checks, limitations, and manual smoke-test steps. |
| 36 | Product Data Copilot Branding Polish | Done | Aligned visible app and README branding around Product Data Copilot while preserving historical Commerce Readiness AI context. |
| 37 | Improved Product Data Export Planning | Done | Planned safe approved-suggestion export with source protection, proposed/approved/rejected/blocked separation, workbook sheets, and phased implementation. |
| 38 | Improved Export Helpers v1 | NEXT | Design and test pure helper functions for splitting V2 suggestions into safe export DataFrames without Streamlit wiring. |
| 39 | Tests Expansion v1 | Planned | Expand pytest coverage for extracted helper modules and key business rules. |
| 40 | UX Polish v1 | Planned | Improve broader app usability after the core Smart Suggestions v2 flow is clearer. |
| 41 | Public GitHub Readiness / Portfolio Presentation Pass | Planned | Prepare the project presentation after the product and helper architecture are stable. |
| 42 | Codex Workflow Optimization v1 | Done | Added compact workflow/context docs so future prompts can reference high-signal state instead of repeating full project history. |

## Backlog Rules

- Keep each block small enough to review.
- Preserve current app behavior unless the task explicitly allows behavior changes.
- Add or update tests when pure helper logic is extracted.
- Run checks before committing.
- Update the project log after meaningful changes.
