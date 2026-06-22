# Product Data Copilot - Project Status

## Current Snapshot

- Product name: Product Data Copilot
- Current repo head before this planning block: `bc53f34 Optimize Codex workflow docs`
- Runtime baseline: `348213d Harden smart suggestion normalization`
- Current test count: `98` passing pytest tests
- Local start command: `python -m streamlit run app.py`
- Current state: local Streamlit MVP with a growing import-safe helper module foundation
- Current planning focus: Smart Suggestions v2 approval UI is implemented session-only; approval UI QA is the next recommended block.
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

## Intentionally Not Implemented Yet

- Database, login, user accounts, or multi-user roles
- SaaS backend, billing, deployment, or production hosting
- Shopware, Shopify, Plentymarkets, or other marketplace integrations
- Marketplace-specific rule presets
- Automatic AI mass generation
- Automatic acceptance or write-back of AI suggestions
- Smart Suggestions v2 approval workflow and export integration
- Field-level AI suggestion approval workflow in the Streamlit app
- Legal compliance guarantees

## Recommended Next Roadmap

1. Smart Suggestions v2 Approval UI QA
2. Improved Product Data Export Planning
3. Tests Expansion v1
4. UX Polish v1
5. Public GitHub Readiness / portfolio presentation pass
