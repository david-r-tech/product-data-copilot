# Current context — Product Data Copilot

**Updated:** 27 September 2026. Product Data Copilot is a local Streamlit MVP for product-data quality, readiness, review tasks, optional single-product AI suggestions, and safe management/improvement exports. The target for this pass is a credible GitHub reference for a Requirements Engineer application, with honest product boundaries.

Read [README.md](../README.md) for setup and user-facing behavior, [requirements_traceability.md](requirements_traceability.md) for decisions and acceptance evidence, and [commerce_readiness_ai_project_log.md](commerce_readiness_ai_project_log.md) for history. Historical plans and demo scripts under `docs/` are not the current runtime specification.

## Current capabilities

- Fictional sample data or bounded CSV/XLSX upload; preserves text identifiers and rejects bad/ambiguous files.
- Deterministic checks, five component readiness scores, severity-aware status, review tasks, and session-only manual status.
- Optional AI suggestions for one selected product. V1 output is an unreviewed draft. V2 output is source-checked, human-reviewed, and exportable as candidates only. No demo-fixture control remains in the application.
- CSV and management/improvement Excel downloads with source snapshot and spreadsheet-safe cell serialization. No source write-back.
- Pure helper modules in `src/product_data_copilot/` and 188 passing pytest tests as last verified on 27 September 2026, including offline calls through the installed OpenAI SDK.

## Scope boundary and remaining checks

This is local and single-session. No accounts, database, deployment, marketplace integration, automatic bulk AI, auto-approval, or compliance guarantee. Manual Excel visual verification remains. A live-AI quality review is explicitly optional and is not part of today's acceptance; no real key or provider request was used. The owner now intends public GitHub visibility for job applications after reviewing the private release candidate; change the repository setting and verify anonymous access only then. External portfolio/CV publication links have not yet been supplied.

For future tasks, read this file and the specific source files involved. Preserve app behavior outside the requested block, keep changes reviewable, update the project log after meaningful changes, and run the relevant automated checks. Do not store secrets. Commit and push only when requested and after checks pass.
