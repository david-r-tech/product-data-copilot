# Current Context - Product Data Copilot

## Snapshot

- Product name: Product Data Copilot
- Current repo head before German demo removal: `3272459 feat: finalize German demo presentation checkpoint`
- Runtime baseline: `348213d Harden smart suggestion normalization`
- Test count: `122` passing pytest tests
- App start command: `python -m streamlit run app.py`
- Current roadmap position: UX Polish Phase 3 - Actions, Status & Empty States completed.
- Next recommended step: Language Switch Planning v1

## Current App Capabilities

- CSV/XLSX upload with sample-data fallback
- Product data preview
- Rule-based product data checks
- Multiple readiness scores
- Issues table with severity filtering
- Review tasks with filters and session-only manual status override
- CSV exports and Excel Management Export
- AI Suggestions v1 for one selected product with missing-key fallback
- Experimental Smart Suggestions v2 prompt preview and empty/safe structured suggestions table
- Separate Smart Suggestions v2 generation button with parser-normalized review-required rows
- Smart Suggestions v2 business-friendly result labels, empty states, status help, and summary metrics
- Smart Suggestions v2 session-only approval UI for one-suggestion review with blocked rows non-approvable
- Smart Suggestions v2 demo fixture loader for deterministic local approval UI testing without an API key
- Product logo integrated into the Streamlit app header from `assets/product_data_copilot_logo.png` with embedded display and text fallback
- UX Polish Phase 1 - Core Product adds a compact workflow orientation, clearer upload guidance, dashboard/readiness interpretation, business-friendly review status wording, clearer AI section grouping, and export-purpose copy without changing product logic.
- Core UX Manual QA v1 provides a browser checklist for validating the polished core workflow after the German demo removal.
- Data Table Readability v1 improves visible table scanning with display-only column ordering, business-friendly labels, hidden indexes, simple column sizing, and controlled table heights while keeping internal/export DataFrames unchanged.
- UX Polish Phase 3 improves action hierarchy, button wording, empty states, AI workflow feedback, review status context, and export completion messaging without changing product logic.
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
- GitHub Repo Rename Manual Checklist v1 documents the owner-only steps for renaming the GitHub repository to `product-data-copilot`, updating local remotes, and checking external links later
- Final Portfolio Release Checklist v1 documents final code readiness, manual QA, AI safety, export safety, portfolio readiness, CV readiness, known limitations, and owner tasks before sharing
- Final Docs Link Polish v1 improves navigation between README, case study, screenshot checklist, final release checklist, and repo rename checklist without changing app behavior
- German Furniture Demo was a temporary presentation workflow and has been removed from the active product after completion.

## Key Modules

- `app.py`: Streamlit runtime and main app flow
- `src/product_data_copilot/rules/validators.py`: validation helpers
- `src/product_data_copilot/scoring/scoring_helpers.py`: scoring helpers
- `src/product_data_copilot/review/review_helpers.py`: review mapping helpers
- `src/product_data_copilot/export/export_helpers.py`: export constants/helpers
- `src/product_data_copilot/ai/prompt_helpers.py`: current AI prompt safety helpers
- `src/product_data_copilot/ai/suggestion_schema.py`: Smart Suggestions v2 schema helpers
- `src/product_data_copilot/ai/suggestion_contract.py`: Smart Suggestions v2 contract text
- `src/product_data_copilot/ai/suggestion_parser.py`: Smart Suggestions v2 parser/normalization helpers
- `src/product_data_copilot/ai/suggestion_prompt_adapter.py`: Smart Suggestions v2 prompt adapter
- `src/product_data_copilot/ui/streamlit_layout.py`: small Streamlit presentation helpers
- `tests/`: pytest coverage for extracted helpers and core product behavior

## Current Non-Goals

- No database, login, user accounts, SaaS backend, billing, or deployment
- No marketplace integrations or presets
- No automatic AI mass generation
- No automatic write-back or auto-approval
- No legal compliance guarantees

## Prompt Guidance

Future Codex prompts should reference this file and include only:

- Goal block
- Allowed files
- Forbidden files
- Required checks
- Commit message
- Any specific acceptance criteria
