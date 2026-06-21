# Smart Suggestions v2 - Planning

## 1. Goal

Smart Suggestions v2 should evolve the current AI Suggestions workflow from broad product-level draft text into safer, field-level suggestions.

The goal is to make AI support more useful for product data teams while keeping the product human-reviewed, auditable, and conservative.

Every suggestion should clearly answer:

- Which field is affected?
- What is the current value?
- What is the proposed value?
- Which source fields support the proposal?
- Why was the suggestion made?
- How confident is the suggestion?
- What risk level does it have?
- Does it require human approval?
- What is its current review status?

## 2. Non-Goals

Smart Suggestions v2 planning does not implement:

- changes to `app.py`
- prompt changes in runtime code
- OpenAI provider changes
- automatic AI generation for all products
- automatic write-back into product data
- automatic approval of AI suggestions
- database persistence
- login, users, or roles
- marketplace integrations
- legal compliance guarantees
- UI redesign
- export behavior changes

## 3. Current AI Suggestions v1 Behavior

Current behavior in `app.py`:

- The AI Suggestions tab selects one product at a time.
- The default selected product is the one with the lowest `overall_readiness_score`.
- Users choose suggestion types such as improved title, description, bullet points, missing attributes, translation, and compliance/safety review note.
- The prompt uses product context, current issues, current scores, anti-hallucination wording, and human-review wording.
- The OpenAI call runs only after the user clicks `Generate AI Suggestions`.
- If `OPENAI_API_KEY` is missing, the app shows an explanatory message and a prompt preview instead of crashing.
- The AI response is expected as JSON with product-level keys:
  - `improved_product_title`
  - `improved_product_description`
  - `bullet_points`
  - `suggested_missing_attributes`
  - `translation`
  - `compliance_safety_review_note`
  - `human_review_notes`
- Invalid JSON falls back to a manual review note and raw response display.
- Suggestions are stored only in `st.session_state`.
- The current AI Suggestions CSV export contains the current one-product suggestion payload.

Important limitation:

AI Suggestions v1 is useful for demos, but it is not yet a field-level approval workflow. It does not track each suggestion as a separate auditable product-data change.

## 4. Target Smart Suggestions v2 Model

Smart Suggestions v2 should model every AI recommendation as one structured suggestion row.

Target examples:

- Suggest a better `product_name` based on existing brand, category, and attributes.
- Suggest a clearer `description` based only on available source fields.
- Suggest missing `attributes` as review tasks if the source data is insufficient.
- Suggest a translation draft only from existing source text and clearly mark it for human review.
- Create a compliance review task instead of inventing warning notes or legal claims.

The future workflow should remain:

1. Select one product.
2. Generate draft field-level suggestions.
3. Review each suggestion.
4. Approve, edit, reject, or mark as needing more source data.
5. Export approved suggestions separately from original data.
6. Never overwrite product data automatically.

## 5. Proposed Suggestion Data Schema

Recommended canonical schema:

| Field | Purpose |
| --- | --- |
| `suggestion_id` | Stable local ID for one suggestion row. |
| `sku` | Product SKU. |
| `field_name` | Target field, such as `product_name`, `description`, `attributes`, or `translation_de`. |
| `current_value` | Current value from the product data. |
| `proposed_value` | Draft suggested value. Empty when no safe factual suggestion can be made. |
| `source_fields` | List or delimited string of source fields used to create the suggestion. |
| `reason` | Short explanation of why the suggestion was created. |
| `confidence` | `low`, `medium`, or `high`. |
| `risk_level` | `low`, `medium`, or `high`. |
| `requires_human_approval` | Boolean, always `True` for AI-generated suggestions. |
| `action_status` | `draft`, `needs_review`, `approved`, or `rejected`. |
| `created_from_issue_type` | Optional issue type that triggered the suggestion. |
| `created_from_field_name` | Optional issue field that triggered the suggestion. |
| `review_note` | Optional note for the human reviewer. |

User-facing wording may call `action_status` simply `status`, but the internal field should stay explicit.

Minimum v2 required fields:

- `sku`
- `field_name`
- `current_value`
- `proposed_value`
- `source_fields`
- `reason`
- `confidence`
- `risk_level`
- `requires_human_approval`
- `action_status`

## 6. Safety Rules / Hallucination Prevention

Smart Suggestions v2 must be conservative by design.

Strict rules:

- Do not invent product facts.
- Do not create unverifiable certifications, dimensions, EANs, materials, compliance claims, prices, or legal/safety statements.
- Do not generate a replacement EAN, GTIN, price, certification, or warning claim.
- Do not claim that a product is legally compliant, safe, certified, or approved unless that exact fact exists in source data.
- Do not turn missing data into factual values.
- Use only the provided product fields, current issues, and current scores.
- Always list the source fields used.
- Always provide a reason.
- Always provide confidence and risk level.
- Always require human approval.
- If source data is missing, contradictory, or too weak, create a review task style suggestion instead of a factual proposed value.

Translation-specific rule:

- A translation draft may be suggested only from existing source text such as `product_name`, `description`, or another translation field.
- The translation must remain a draft and must not add new claims.

Compliance-specific rule:

- For safety-relevant products, AI may suggest that a human should check warning notes.
- AI must not generate legal assurances or compliance guarantees.

## 7. Human-in-the-Loop Approval Model

Every generated suggestion should start in `draft` or `needs_review`.

Allowed action statuses:

- `draft`: Generated but not reviewed.
- `needs_review`: Requires explicit human review before use.
- `approved`: Human accepted the suggestion for export.
- `rejected`: Human rejected the suggestion.

Future optional statuses:

- `edited`: Human changed the proposed value before approval.
- `blocked_insufficient_source`: No safe suggestion could be created because source data was missing.

Approval rules:

- AI suggestions never update the source product table automatically.
- Only approved suggestions may be included in a future improved-data export.
- Rejected and draft suggestions may still be included in audit/report exports.
- Compliance and safety-related suggestions should remain `needs_review` until a human checks them.

## 8. Connection to Review Tasks

Smart Suggestions v2 should connect to review tasks without replacing them.

Recommended relationship:

- Product issues remain the source of what needs attention.
- Review tasks remain the operational checklist.
- AI suggestions are optional draft recommendations attached to specific fields or issues.

Examples:

- Missing description -> Review task: `Content Improvement`; AI may suggest a draft description only if enough source fields exist.
- Missing attributes -> Review task: `Attribute Enrichment`; AI should suggest which attributes to collect, not invent values.
- Missing warning notes -> Review task: `Compliance Review`; AI should recommend human safety review, not create compliance claims.
- Invalid EAN -> Review task: `Data Completion`; AI should not propose a replacement EAN.
- Invalid price -> Review task: `Commercial Review`; AI should not invent a price.

## 9. Confidence and Risk-Level Model

Confidence values:

- `high`: Suggestion is based on several clear source fields and does not add new facts.
- `medium`: Suggestion is based on useful source data but needs careful review.
- `low`: Source data is thin, incomplete, or ambiguous.

Risk levels:

- `low`: Formatting, wording, or clarity improvement with no new factual claims.
- `medium`: Content rewrite, translation draft, or attribute recommendation that could affect marketplace quality.
- `high`: Safety, compliance, pricing, EAN/GTIN, certification, legal, regulated, or claim-sensitive content.

Default rules:

- Safety/compliance-related suggestions should default to `high` risk.
- Price, EAN, certification, and legal fields should normally produce review tasks, not proposed factual values.
- Missing or contradictory source fields should reduce confidence.
- Every `high` risk suggestion must require human approval and should not be exportable as improved data unless explicitly approved later.

## 10. Export Implications

Current exports should not change during planning.

Future export direction:

- Management Export should include an `AI Suggestions` sheet with all generated suggestions and statuses.
- A future improved-data export should include only approved suggestions.
- Original product data should remain available in exports.
- Approved suggestions should be traceable back to `source_fields`, `reason`, confidence, and risk level.
- Draft, rejected, and needs-review suggestions should be audit/report data, not applied product data.

Minimum future export sheets:

- `AI Suggestions Audit`
- `Approved Suggestions`
- optional `Improved Product Data Preview`

## 11. UI Implications

Smart Suggestions v2 should fit into the existing AI Suggestions tab first.

Recommended future UI behavior:

- Keep one-product generation first.
- Show suggestions as a table with one row per field-level suggestion.
- Show source fields, confidence, risk level, reason, and action status.
- Allow status changes in session state first.
- Make approval explicit.
- Keep original product data visible beside suggestions.
- Avoid mass generation until the field-level model is stable.

Do not redesign the whole app during Smart Suggestions v2.

## 12. Tests Needed

Pure helper tests should come before runtime integration.

Recommended test areas:

- schema field list contains required fields
- confidence validation and normalization
- risk-level validation and normalization
- action-status validation and normalization
- suggestion row normalization
- missing source data creates a review-style suggestion instead of a factual proposed value
- unsafe target fields such as EAN or price are blocked from factual AI proposals
- approved-only filter for future improved exports
- parser behavior for malformed or partial AI responses
- no OpenAI API call during helper tests

## 13. Exact Implementation Phases

### Phase 1: Schema Helpers

Purpose:

Create pure, import-safe schema and validation helpers for field-level suggestions.

Status: Completed in `Smart Suggestions v2 - Phase 1: Schema Helpers`.

Result:

- Added pure schema helpers in `src/product_data_copilot/ai/suggestion_schema.py`.
- Added future contract helpers in `src/product_data_copilot/ai/suggestion_contract.py`.
- Added focused pytest coverage in `tests/test_suggestion_schema.py` and `tests/test_suggestion_contract.py`.
- Kept `app.py`, current prompt runtime behavior, exports, UI, and OpenAI behavior unchanged.
- Smart Suggestions v2 is still not wired into the running Streamlit app.

Allowed future files:

- `src/product_data_copilot/ai/suggestion_schema.py`
- `tests/test_suggestion_schema.py`
- `docs/commerce_readiness_ai_project_log.md`
- `docs/codex_task_backlog.md`

Do not change:

- `app.py`
- prompt runtime behavior
- OpenAI calls
- exports
- UI

Required checks:

- `python -m pytest`
- forbidden-file diff check for `app.py`, `requirements.txt`, and sample data

### Phase 2: Contract & Parser Helpers

Purpose:

Add safe parser and response-normalization helpers for future field-level AI responses. Keep contract helpers aligned with the schema, but do not change runtime prompts yet.

Allowed future files:

- `src/product_data_copilot/ai/suggestion_schema.py`
- `tests/test_suggestion_schema.py`
- `src/product_data_copilot/ai/suggestion_contract.py`
- optional `src/product_data_copilot/ai/response_parser.py`
- `tests/test_suggestion_contract.py`
- optional `tests/test_response_parser.py`

Do not change:

- `app.py`
- current OpenAI call behavior
- current prompt used by the app
- UI or exports

### Phase 3: Prompt Contract Update, No Provider Change

Purpose:

Update the prompt contract to request field-level suggestion rows while preserving the current OpenAI provider and missing-key fallback.

Allowed future files:

- `app.py`
- `src/product_data_copilot/ai/prompt_helpers.py`
- `tests/test_prompt_helpers.py`
- optional prompt snapshot tests

Stop if:

- prompt changes would require broad UI or export changes in the same phase
- AI response keys become ambiguous

### Phase 4: Safe AI Response Parsing

Purpose:

Parse and normalize AI responses into the field-level schema. Preserve raw response fallback for malformed JSON.

Allowed future files:

- `src/product_data_copilot/ai/suggestion_schema.py`
- optional `src/product_data_copilot/ai/response_parser.py`
- `tests/test_suggestion_schema.py`
- optional `tests/test_response_parser.py`
- `app.py` only for minimal wiring

### Phase 5: Display Structured Suggestions in Existing AI Tab

Purpose:

Show field-level suggestions in the current AI Suggestions tab without redesigning the app.

Allowed future files:

- `app.py`
- optional UI helper tests if presentation helpers are extracted

Behavior limits:

- one selected product only
- no mass generation
- session-state only
- no automatic product-data overwrite

### Phase 6: Export Approved Suggestions Only

Purpose:

Add export logic that separates all suggestions from approved suggestions and prevents draft suggestions from being treated as improved data.

Allowed future files:

- `app.py`
- `src/product_data_copilot/export/export_helpers.py`
- tests for approved-only filtering

Behavior limits:

- original source data must remain unchanged
- approved suggestions export should be clearly labeled
- management export may include audit rows, but improved-data export should use approved suggestions only

## 14. Rollback Strategy

Each future phase should be one small commit.

If behavior changes unexpectedly:

1. Stop immediately.
2. Do not continue into the next phase.
3. Run `git status`.
4. Revert only the latest phase commit.
5. Rerun `python -m pytest`.
6. Manually run `python -m streamlit run app.py` before continuing.

For prompt or parser changes, keep the old v1 behavior available until v2 parsing is proven by tests and manual review.

## 15. Risks and Limitations

Main risks:

- AI might produce fields that are not in the schema.
- AI might include invented facts despite instructions.
- Human reviewers might misunderstand draft suggestions as approved values.
- Export logic might accidentally mix draft suggestions with approved data.
- Compliance-related wording could look stronger than intended.
- The UI could become too complex if all statuses and controls are added at once.

Risk controls:

- Start with pure schema helpers.
- Add tests before app wiring.
- Keep one-product generation first.
- Require explicit approval for every suggestion.
- Use conservative defaults for risk and confidence.
- Block factual proposals for high-risk fields such as EAN, price, certifications, and legal claims.
- Keep original product data visible and unchanged.

## 16. Definition of Done for Smart Suggestions v2 Planning

Planning is complete when:

- Smart Suggestions v2 is clearly marked as planned, not implemented.
- Field-level suggestion schema is defined.
- AI safety rules are explicit and strict.
- Human approval is required.
- Review task connection is clear.
- Export and UI implications are documented.
- Future implementation phases are small and safe.
- The next backlog block is `Smart Suggestions v2 - Phase 1: Schema Helpers`.
