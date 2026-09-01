# Product Data Copilot - Project Status

## Current Snapshot

- Product name: Product Data Copilot
- Current repo head before German demo removal: `3272459 feat: finalize German demo presentation checkpoint`
- Runtime baseline: `348213d Harden smart suggestion normalization`
- Current test count: `122` passing pytest tests
- Local start command: `python -m streamlit run app.py`
- Current state: local Streamlit MVP with a growing import-safe helper module foundation
- Current planning focus: Core UX Manual QA v1 documented; Data Table Readability v1 is the next recommended step.
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
- Product logo integrated into the Streamlit app header from `assets/product_data_copilot_logo.png` with embedded display and text fallback
- UX Polish Phase 1 - Core Product adds clearer workflow orientation, upload guidance, dashboard/readiness interpretation, business-friendly review status wording, AI section grouping, and export-purpose copy without behavior changes.
- Core UX Manual QA v1 documents how to manually verify the polished core workflow in the browser.
- Smart Suggestions v2 fixture QA documentation with manual smoke-test checklist
- Visible app and README branding aligned around Product Data Copilot
- Improved Product Data Export plan for safe approved-suggestion export without write-back
- Improved export helpers for splitting Smart Suggestions v2 records into approved, pending, rejected, blocked, and unknown export DataFrames
- Improved Product Data Export Preview in the Smart Suggestions v2 area without downloads or write-back
- Improved Excel Export v1 plan for a safe workbook download with approved/pending/rejected/blocked/unknown sheets and original source snapshot
- Improved Excel export helpers for workbook sheet mapping, export summary data, suggestion groups, and original source snapshots without file writing or write-back
- Improved Excel download wiring for a safe in-memory workbook generated from Smart Suggestions v2 review state without source write-back
- Improved export manual QA checklist for verifying workbook sheets, approved export candidates, empty states, and unchanged source snapshots
- UX Polish v1 plan for small copy, help text, empty-state, safety-message, Smart Suggestions v2, and improved export clarity improvements
- UX Copy Polish v1 improved AI safety wording, Smart Suggestions v2 guidance, empty states, and improved export explanations without behavior changes
- UX Manual QA v1 checklist for validating browser clarity, AI safety wording, review workflow, export safety, and portfolio presentation
- Portfolio Case Study Planning v1 defines the target audience, story arc, structure, screenshot needs, portfolio-worthy points, and honest claim boundaries for the final case study
- Portfolio Case Study Draft v1 documents the product story, user problem, workflows, architecture, AI safety model, export safety, testing approach, limitations, roadmap, and screenshot placeholders
- Portfolio Screenshot Checklist v1 defines the final manual screenshots, preparation steps, filenames, captions, and pass/fail notes for GitHub and portfolio presentation
- README Final Polish Planning v1 defines the final README structure, screenshot placeholder strategy, case study links, test/run instructions, AI/export safety wording, limitations, and acceptance criteria
- README Final Polish v1 updates the GitHub-facing README with a concise product pitch, screenshot placeholder, run/test commands, architecture overview, AI/export safety, case study links, limitations, and roadmap
- Final Naming Cleanup Planning v1 defines how to move safely from the old working name and repository name toward Product Data Copilot without automatic repo/folder renaming
- Safe Naming Cleanup v1 removes safe current-facing old product-name references from the app header and README while keeping historical references, package paths, generated filenames, and repository URLs unchanged
- GitHub Repo Rename Manual Checklist v1 documents the owner-only repository rename steps, local remote update commands, external link checks, risks, and acceptance criteria
- Final Portfolio Release Checklist v1 documents final code readiness, manual QA, AI safety, export safety, GitHub/portfolio readiness, CV readiness, known limitations, and manual owner tasks
- Final Docs Link Polish v1 adds final GitHub-friendly navigation links between README, case study, screenshot checklist, final release checklist, and repo rename checklist
- German Furniture Demo was a temporary presentation workflow and has been removed from the active product after completion.
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
- Improved Export Manual QA v1 is documented in `docs/improved_export_manual_qa.md`.
- UX Polish Planning v1 is documented in `docs/ux_polish_plan_v1.md`.
- UX Copy Polish v1 updated in-app wording for clearer AI safety, Smart Suggestions v2 review flow, and improved export expectations.
- UX Manual QA v1 is documented in `docs/ux_manual_qa_v1.md`.
- Portfolio Case Study Planning v1 is documented in `docs/portfolio_case_study_plan_v1.md`.
- Portfolio Case Study Draft v1 is documented in `docs/portfolio_case_study.md`.
- Portfolio Screenshot Checklist v1 is documented in `docs/portfolio_screenshot_checklist_v1.md`.
- README Final Polish Planning v1 is documented in `docs/readme_final_polish_plan_v1.md`.
- README Final Polish v1 updates the public `README.md`.
- Final Naming Cleanup Planning v1 is documented in `docs/final_naming_cleanup_plan_v1.md`.
- Safe Naming Cleanup v1 updates current-facing app/README naming without repository, package, or filename renames.
- GitHub Repo Rename Manual Checklist v1 is documented in `docs/github_repo_rename_manual_checklist_v1.md`.
- Final Portfolio Release Checklist v1 is documented in `docs/final_portfolio_release_checklist_v1.md`.
- Final Docs Link Polish v1 connects the final portfolio documents for easier reviewer navigation.
- German Furniture Demo removal keeps the active product focused on the normal Product Data Copilot workflow.

## Intentionally Not Implemented Yet

- Database, login, user accounts, or multi-user roles
- SaaS backend, billing, deployment, or production hosting
- Shopware, Shopify, Plentymarkets, or other marketplace integrations
- Marketplace-specific rule presets
- Automatic AI mass generation
- Automatic acceptance or write-back of AI suggestions
- Permanent Smart Suggestions v2 approval persistence
- Marketplace-ready export/write-back integration
- Actual screenshot image files for the portfolio case study
- Manual GitHub repository rename to `product-data-copilot`
- Legal compliance guarantees

## Recommended Next Roadmap

1. Manual owner tasks for QA, screenshots, and optional GitHub repo rename
2. Tests Expansion v1
3. Data Table Readability v1
4. Public GitHub Readiness / portfolio presentation pass
