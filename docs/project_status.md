# Product Data Copilot - Project Status

## Current Snapshot

- Product name: Product Data Copilot
- Last documented baseline before this package: `4a8b2d1 Add smart suggestion foundation helpers`
- Current test count: `78` passing pytest tests
- Local start command: `python -m streamlit run app.py`
- Current state: local Streamlit MVP with a growing import-safe helper module foundation
- Current planning focus: Smart Suggestions v2 has pure schema, contract, and parser foundations; it is not wired into runtime yet.

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
- Documentation, demo checklist, demo script, and portfolio case-study draft

## Completed Architecture / Refactor Milestones

- `app.py` has a minimal `run_app()` entrypoint.
- Small Streamlit presentation helpers live under `src/product_data_copilot/ui/`.
- Import-safe helpers exist for validators, scoring, review mappings, export constants, and AI prompt safety text.
- Helper Integration v1 is complete across Validators, Scoring, Review Helpers, Export Helpers, and AI Prompt Helpers.
- Pytest coverage exists for extracted helper modules.
- Smart Suggestions v2 planning is documented in `docs/smart_suggestions_v2_plan.md`.
- Smart Suggestions v2 schema, contract, and parser helpers exist as pure import-safe modules with tests.

## Intentionally Not Implemented Yet

- Database, login, user accounts, or multi-user roles
- SaaS backend, billing, deployment, or production hosting
- Shopware, Shopify, Plentymarkets, or other marketplace integrations
- Marketplace-specific rule presets
- Automatic AI mass generation
- Automatic acceptance or write-back of AI suggestions
- Smart Suggestions v2 runtime behavior
- Field-level AI suggestion approval workflow in the Streamlit app
- Legal compliance guarantees

## Recommended Next Roadmap

1. Smart Suggestions v2 - Phase 3: Prompt Contract Planning
2. Tests Expansion v1
3. UX Polish v1
4. Public GitHub Readiness / portfolio presentation pass
