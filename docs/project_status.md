# Product Data Copilot - Project Status

## Current Snapshot

- Product name: Product Data Copilot
- Current repo head before Improved Excel Download Wiring v1: `12b3839 Add improved Excel export helpers`
- Runtime baseline: `348213d Harden smart suggestion normalization`
- Current test count: `122` passing pytest tests
- Local start command: `python -m streamlit run app.py`
- Current state: local Streamlit MVP with a growing import-safe helper module foundation
- Current planning focus: Improved Excel Download Wiring v1 completed; improved export manual QA is the next recommended block.
- Workflow note: Future Codex prompts should reference `docs/current_context.md` instead of repeating the full project history.

## Implemented Capabilities

- CSV and XLSX upload with sample-data fallback
- Product data preview
- Rule-based product data checks
- Multiple readiness scores
- Dashboard metrics
- Issues table with severity filtering
- Review tasks with filters and manual review status override
- CSV exports for scores, issues, and review tasks
- Excel Management Export
- AI Suggestions for one selected product
- Missing API-key fallback for AI Suggestions
- Human-review wording for AI Suggestions
- Experimental Smart Suggestions v2 prompt preview and structured suggestions table
- Separate Smart Suggestions v2 generation button with parser-normalized review-required rows
- Smart Suggestions v2 business-friendly result labels, empty states, status help, and summary metrics
- Smart Suggestions v2 demo fixture loader for deterministic local review testing without an API key
- Smart Suggestions v2 fixture QA documentation with manual smoke-test checklist
- Visible app and README branding aligned around Product Data Copilot
- Improved Product Data Export plan for safe approved-suggestion export without write-back
- Improved export helpers for splitting Smart Suggestions v2 records into approved, pending, rejected, blocked, and unknown export DataFrames
- Improved Product Data Export Preview in the Smart Suggestions v2 area without downloads or write-back
- Improved Excel Export v1 plan for a safe workbook download with approved/pending/rejected/blocked/unknown sheets and original source snapshot
- Improved Excel export helpers for workbook sheet mapping, export summary data, suggestion groups, and original source snapshots without file writing or write-back
- Improved Excel download wiring for a safe in-memory workbook generated from Smart Suggestions v2 review state without source write-back
- Documentation, demo checklist, demo script, and portfolio case-study draft

## Completed Architecture / Refactor Milestones

- `app.py` has a minimal `run_app()` entrypoint.
- Small Streamlit presentation helpers live under `src/product_data_copilot/ui/`.
- Import-safe helpers exist for validators, scoring, review mappings, export constants, and AI prompt safety text.
- Helper Integration v1 is complete across Validators, Scoring, Review Helpers, Export Helpers, and AI Prompt Helpers.
- Pytest coverage exists for extracted helper modules.
- Smart Suggestions v2 planning is documented in `docs/smart_suggestions_v2_plan.md`.
- Smart Suggestions v2 schema, contract, and parser helpers exist as pure import-safe modules with tests.
- Smart Suggestions v2 prompt contract planning is documented in `docs/smart_suggestions_v2_phase3_prompt_contract_plan.md`.
- Smart Suggestions v2 prompt adapter helpers exist as pure import-safe modules with tests.
- Smart Suggestions v2 normalization hardening covers approved-like statuses, restricted factual fields, missing source fields, missing reasons, unsupported source shapes, and ignored extra keys.
- Smart Suggestions v2 runtime integration planning is documented in `docs/smart_suggestions_v2_runtime_integration_plan.md`.
- Smart Suggestions v2 experimental UI wiring shows a prompt preview and schema-stable table without changing V1 behavior.
- Smart Suggestions v2 controlled runtime generation planning is documented in `docs/smart_suggestions_v2_generation_plan.md`.
- Smart Suggestions v2 controlled runtime generation is wired separately from V1 and stores V2 output in separate session state.
- Smart Suggestions v2 runtime QA is documented in `docs/smart_suggestions_v2_runtime_qa.md`.
- Smart Suggestions v2 result UX polish keeps V2 easier to understand without adding approval, export, or write-back scope.
- Smart Suggestions v2 approval workflow planning is documented in `docs/smart_suggestions_v2_approval_workflow_plan.md`.
- Smart Suggestions v2 Approval UI v1 supports one-suggestion-at-a-time session-only approve/reject/pending decisions with blocked rows non-approvable.
- Smart Suggestions v2 Approval UI QA is documented in `docs/smart_suggestions_v2_approval_ui_qa.md`.
- Smart Suggestions v2 test fixture planning is documented in `docs/smart_suggestions_v2_test_fixture_plan.md`.
- Smart Suggestions v2 Test Fixture v1 adds deterministic fixture records and parser coverage for pending, high-risk, blocked, missing-source, and AI-supplied approved cases.
- Smart Suggestions v2 Fixture QA is documented in `docs/smart_suggestions_v2_fixture_qa.md`.
- Product Data Copilot branding polish updates the visible app title and README identity while preserving the original project history.
- Improved Product Data Export Planning is documented in `docs/improved_product_data_export_plan.md`.
- Improved Export Helpers v1 adds pure helper functions and tests for preparing Smart Suggestions v2 export data without Streamlit wiring or write-back.
- Improved Export Preview v1 wires the helper output into a preview-only Streamlit section without downloads, source mutation, or write-back.
- Improved Excel Export v1 planning is documented in `docs/improved_excel_export_v1_plan.md`.
- Improved Excel Export Helpers v1 adds pure helper functions and tests for preparing workbook sheet data before Streamlit download wiring.
- Improved Excel Download Wiring v1 adds the Streamlit download button using helper-built workbook sheets and in-memory Excel generation.

## Intentionally Not Implemented Yet

- Database, login, user accounts, or multi-user roles
- SaaS backend, billing, deployment, or production hosting
- Shopware, Shopify, Plentymarkets, or other marketplace integrations
- Marketplace-specific rule presets
- Automatic AI mass generation
- Automatic acceptance or write-back of AI suggestions
- Smart Suggestions v2 export integration
- Improved Product Data Export implementation
- Improved Export Manual QA
- Legal compliance guarantees

## Recommended Next Roadmap

1. Improved Export Manual QA v1
2. Tests Expansion v1
3. UX Polish v1
4. Public GitHub Readiness / portfolio presentation pass
