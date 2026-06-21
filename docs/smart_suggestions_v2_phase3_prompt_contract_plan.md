# Smart Suggestions v2 - Phase 3 Prompt Contract Plan

## 1. Purpose

This phase plans the future prompt contract for Smart Suggestions v2.

It does not change the running Streamlit app, the current AI Suggestions v1 prompt, OpenAI calls, exports, UI, or review workflow.

The goal is to define how a future prompt should request structured field-level suggestions that can be parsed by the existing Smart Suggestions v2 schema and parser helpers.

## 2. Current AI Suggestions v1 Summary

Current behavior in `app.py`:

- AI Suggestions runs for one selected product.
- The default selected product is the product with the lowest `overall_readiness_score`.
- The user selects broad suggestion types.
- The current prompt asks for product-level sections:
  - improved product title
  - improved product description
  - bullet points
  - suggested missing attributes
  - translation
  - compliance/safety review note
  - human review notes
- The prompt includes product context, current issues, current scores, anti-hallucination wording, and human-review wording.
- OpenAI is called only after the user clicks `Generate AI Suggestions`.
- Missing `OPENAI_API_KEY` shows a fallback message and prompt preview.
- Invalid JSON falls back to raw response display and a manual review note.
- Suggestions are stored only in `st.session_state`.

Current limitation:

AI Suggestions v1 is useful for a demo, but its output is not yet a row-based, auditable field-level suggestion model.

## 3. Target Smart Suggestions v2 Prompt Contract

Future Smart Suggestions v2 prompts should request exactly one JSON object with a `smart_suggestions` array.

Each item in `smart_suggestions` must be one field-level suggestion.

The prompt should explicitly require:

- no invented facts
- source fields for every suggestion
- reason for every suggestion
- confidence value
- risk level
- human approval requirement
- review-required status by default
- no automatic approval
- no unsupported factual values for risky fields

The future prompt should use the reusable contract helper:

`smart_suggestion_prompt_contract_block()`

That helper is not wired into `app.py` yet.

## 4. Exact Required Output Shape

Future output shape:

```json
{
  "smart_suggestions": [
    {
      "sku": "SKU-001",
      "product_name": "Example product",
      "target_field": "description",
      "current_value": "Existing value",
      "proposed_value": "Draft value based only on source fields",
      "source_fields": ["product_name", "attributes"],
      "reason": "Short explanation",
      "confidence": "medium",
      "risk_level": "low",
      "requires_human_approval": true,
      "approval_status": "needs_review",
      "suggestion_status": "review_required"
    }
  ]
}
```

Required keys:

- `sku`
- `product_name`
- `target_field`
- `current_value`
- `proposed_value`
- `source_fields`
- `reason`
- `confidence`
- `risk_level`
- `requires_human_approval`
- `approval_status`
- `suggestion_status`

Allowed values:

- `confidence`: `low`, `medium`, `high`
- `risk_level`: `low`, `medium`, `high`
- `approval_status`: `needs_review`, `approved`, `rejected`
- `suggestion_status`: `draft`, `review_required`, `blocked_insufficient_source`

Important:

The AI must not set `approval_status` to `approved`. If it does, parser helpers already downgrade that value to `needs_review`.

## 5. Safety Language That Must Be Preserved

Future prompts must preserve these rules:

- Do not invent product facts.
- Use only existing source fields from the provided product data.
- Do not create unverifiable EANs, GTINs, prices, dimensions, certifications, materials, translations, or compliance claims.
- Do not claim legal compliance.
- Do not claim that a product is safe.
- If source data is missing, weak, unknown, or contradictory, leave `proposed_value` empty and mark the suggestion as review required.
- Every suggestion must include `source_fields`, `reason`, `confidence`, `risk_level`, `approval_status`, and `suggestion_status`.
- Human approval is required before use or export.
- Do not auto-apply suggestions to product data.

## 6. Forbidden AI Behaviors

The future prompt must forbid:

- inventing product facts
- generating replacement EANs or GTINs
- inventing prices
- inventing dimensions or technical specifications
- inventing materials
- inventing certifications
- inventing safety warnings as factual claims
- claiming legal compliance
- claiming that a product is safe
- adding unsupported translations that introduce new facts
- setting `approval_status` to `approved`
- suggesting automatic write-back into product data

## 7. Allowed Suggestion Examples

Allowed example: title clarity

- `target_field`: `product_name`
- source fields: `product_name`, `brand`, `category`, `attributes`
- proposed value: a clearer title using only existing values
- confidence: `medium` or `high`
- risk level: `low`
- approval status: `needs_review`

Allowed example: description rewrite

- `target_field`: `description`
- source fields: `product_name`, `category`, `brand`, `attributes`
- proposed value: a clearer description using only source information
- confidence: `medium`
- risk level: `low` or `medium`
- approval status: `needs_review`

Allowed example: translation draft

- `target_field`: `translation_de` or `translation_en`
- source fields: existing title or description fields
- proposed value: a draft translation that does not add claims
- confidence: `medium` or `low`
- risk level: `medium`
- approval status: `needs_review`

## 8. Blocked / Review-Required Suggestion Examples

Blocked example: missing EAN

- `target_field`: `ean`
- proposed value: empty
- reason: EAN is missing and cannot be invented
- risk level: `high`
- suggestion status: `blocked_insufficient_source`

Blocked example: missing price

- `target_field`: `price`
- proposed value: empty
- reason: Price must come from a business source and cannot be invented
- risk level: `high`
- suggestion status: `blocked_insufficient_source`

Review-required example: missing warning notes

- `target_field`: `warning_notes`
- proposed value: empty or a reviewer note, not a factual safety claim
- reason: Safety-related content needs human compliance review
- risk level: `high`
- suggestion status: `review_required`

Review-required example: weak source attributes

- `target_field`: `attributes`
- proposed value: empty or a list of attributes to collect, not invented values
- reason: Source data is insufficient to create factual attributes
- confidence: `low`
- suggestion status: `blocked_insufficient_source` or `review_required`

## 9. Parser Handling Expectations

Future prompt integration should rely on the parser helpers instead of trusting raw model output.

Expected parser behavior:

- Invalid JSON returns no suggestions and a parser error record.
- Empty or null responses return an empty safe result.
- Unknown confidence values normalize to `low`.
- Unknown risk values normalize to `high`.
- Unknown approval statuses normalize to `needs_review`.
- Unknown suggestion statuses normalize to `review_required`.
- AI-supplied `approval_status = approved` is downgraded to `needs_review`.
- Missing source fields or missing reason make records invalid/use-blocked.
- Supported root keys should include `smart_suggestions`, but future prompt integration should request only `smart_suggestions`.

## 10. Future App Integration Phases

### Phase 4: Runtime Prompt Adapter

Create a prompt adapter helper that can build the Smart Suggestions v2 prompt contract from existing product context, issues, and scores.

Allowed future direction:

- add helper tests first
- keep OpenAI provider unchanged
- keep missing-key fallback unchanged
- keep one-product generation
- do not change UI yet

### Phase 5: Runtime Parser Wiring

Wire generated AI text through the parser helpers.

Limits:

- preserve raw response fallback
- keep current v1 display until v2 display is ready, or clearly gate v2 output
- do not auto-apply suggestions

### Phase 6: Structured Suggestion Display

Display field-level suggestions in the existing AI Suggestions tab.

Limits:

- no broad redesign
- one product only
- session-state only
- explicit human review status

### Phase 7: Approved Suggestions Export

Export approved suggestions separately from original product data.

Limits:

- do not overwrite source product data
- draft and rejected suggestions remain audit records
- approved-only export must be clearly labeled

## 11. Test Strategy

Before runtime integration:

- test prompt contract helper output is deterministic
- test required keys are present
- test safety wording includes anti-hallucination language
- test forbidden categories are listed
- test review-required conditions are listed
- test human review wording is present
- test parser rejects or blocks unsafe model output

During runtime integration:

- add prompt snapshot tests before changing `app.py`
- verify missing-key fallback still works
- verify no OpenAI call occurs during import or tests
- verify malformed model output does not crash
- verify no parsed suggestion becomes approved automatically

Manual smoke tests later:

- start app with `python -m streamlit run app.py`
- open AI Suggestions tab without API key
- confirm fallback still appears
- with API key, generate for one product only
- verify structured suggestions remain draft/review-required

## 12. Rollback Strategy

Keep each future prompt/runtime phase as one small commit.

If behavior changes unexpectedly:

1. Stop immediately.
2. Do not continue to UI/export work.
3. Revert only the latest prompt/runtime commit.
4. Rerun `python -m pytest`.
5. Rerun `python -m py_compile app.py`.
6. Manually smoke-test AI Suggestions.

The current v1 prompt should remain easy to restore until v2 behavior is proven.

## 13. Explicit Not In Scope

This phase does not include:

- editing `app.py`
- wiring Smart Suggestions v2 into the running app
- changing the current AI Suggestions v1 prompt
- changing OpenAI model/provider behavior
- changing API-key fallback behavior
- changing UI
- changing exports
- changing review workflow
- adding dependencies
- generating real AI suggestions
- adding mass generation
- automatic approval or write-back
- database/login/SaaS/integrations

## 14. Definition of Done

This phase is complete when:

- a prompt contract plan exists
- contract helper output is stricter and test-covered
- required output shape is documented
- safety language is explicit
- parser expectations are documented
- future integration phases are clear
- runtime behavior remains unchanged
