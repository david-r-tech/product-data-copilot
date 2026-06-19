# Codex Task Backlog - Product Data Copilot

This backlog is a lightweight execution guide for the next safe refactor and quality blocks.

Work on one block at a time. Do not start the next block unless the user explicitly requests it.

| Order | Block | Status | Goal |
| --- | --- | --- | --- |
| 1 | Extract Scoring Helpers v1 | Done | Created small import-safe scoring helpers and pytest coverage without changing app behavior. |
| 2 | Extract Review Helpers v1 | NEXT | Move pure review mapping/status helper logic into an import-safe module with tests. |
| 3 | Extract Export Helpers v1 | Planned | Move pure export preparation helpers into an import-safe module with tests. |
| 4 | Extract AI Prompt Helpers v1 | Planned | Move prompt-building and AI response parsing helpers into an import-safe module with tests. |
| 5 | App Slimdown v1 | Planned | Make `app.py` thinner by importing tested helpers while preserving behavior. |
| 6 | Tests Expansion v1 | Planned | Expand pytest coverage for extracted helper modules and key business rules. |
| 7 | UX Polish v1 | Planned | Improve usability after the core logic is safer and more modular. |

## Backlog Rules

- Keep each block small enough to review.
- Preserve current app behavior unless the task explicitly allows behavior changes.
- Add or update tests when pure helper logic is extracted.
- Run checks before committing.
- Update the project log after meaningful changes.
