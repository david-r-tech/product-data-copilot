# Current Context - Product Data Copilot

## Snapshot

- Product name: Product Data Copilot
- Current repo head before Phase 10 QA: `6175716 Add controlled smart suggestion generation`
- Runtime baseline: `348213d Harden smart suggestion normalization`
- Test count: `98` passing pytest tests
- App start command: `python -m streamlit run app.py`
- Current roadmap position: Smart Suggestions v2 runtime QA is documented; result UX polish is the next recommended visible-value block.
- Next block: `Smart Suggestions v2 Result UX Polish`

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
- `tests/`: pytest coverage for extracted helpers

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
