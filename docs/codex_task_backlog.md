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
| 17 | Helper Integration v1 - Finalization | NEXT | Review completed helper integration, document final state, and decide the next safe quality block. |
| 18 | Tests Expansion v1 | Planned | Expand pytest coverage for extracted helper modules and key business rules. |
| 19 | UX Polish v1 | Planned | Improve usability after the core logic is safer and more modular. |

## Backlog Rules

- Keep each block small enough to review.
- Preserve current app behavior unless the task explicitly allows behavior changes.
- Add or update tests when pure helper logic is extracted.
- Run checks before committing.
- Update the project log after meaningful changes.
