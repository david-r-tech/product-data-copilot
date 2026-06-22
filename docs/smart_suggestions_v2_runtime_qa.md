# Smart Suggestions v2 - Runtime QA

## 1. Scope

This QA note reviews the current Smart Suggestions v2 runtime integration after Phase 9.

No code changes are part of this QA block.

## 2. Current V2 Runtime Behavior

Smart Suggestions v2 is visible inside the existing `AI Suggestions` tab as a separate experimental section.

Current behavior:

- V1 AI Suggestions remains above the V2 section.
- V2 shows a structured prompt preview.
- V2 has a separate `Generate Smart Suggestions v2` button.
- V2 uses a separate OpenAI call path from V1.
- V2 parses raw AI output through `parse_and_normalize_suggestions(...)`.
- V2 displays normalized field-level rows in a schema-stable table.
- V2 raw response appears only in `Raw Smart Suggestions v2 response`.
- V2 does not export, approve, or apply suggestions.

## 3. Manual Smoke Test Result

Reported manual smoke test result: Passed.

Confirmed:

- The Streamlit app starts successfully.
- V1 AI Suggestions still appears.
- Smart Suggestions v2 experimental section appears.
- V2 prompt preview appears.
- V2 structured suggestions table appears.
- Without `OPENAI_API_KEY`, V2 generation is safely disabled.
- No red runtime error was visible.
- Exports appeared unchanged.

## 4. V1 Preservation Check

V1 remains preserved because:

- The existing V1 button remains `Generate AI Suggestions`.
- The existing V1 prompt builder remains separate.
- The existing V1 session-state keys remain separate:
  - `ai_suggestions`
  - `ai_suggestions_sku`
- The existing V1 CSV download remains unchanged.
- The V2 section is added below V1 instead of replacing it.

## 5. V2 Session State Separation Check

V2 uses separate session-state keys:

- `smart_suggestions_v2_prompt`
- `smart_suggestions_v2_raw_response`
- `smart_suggestions_v2_records`
- `smart_suggestions_v2_error`
- `smart_suggestions_v2_is_valid_json`
- `smart_suggestions_v2_sku`

The display checks both selected SKU and prompt match before showing stored V2 records. This reduces the risk of showing V2 rows for the wrong selected product.

## 6. Parser and Safety Behavior Check

Current safety behavior:

- Raw V2 output is parsed with `parse_and_normalize_suggestions(...)`.
- Parser errors are shown as review-needed output.
- Invalid JSON is not treated as usable product data.
- Blocked rows remain visible as blocked.
- Display logic prevents approved-looking rows from being displayed as approved.
- Product data is not changed.
- Review tasks, scores, issues, and exports are not changed.

This is consistent with the V2 safety goal: AI output can support review, but it does not become accepted product data.

## 7. Known Limitations

- V2 result display is still table-first and technical.
- There is no row-level approval, rejection, or edit workflow yet.
- There is no V2 CSV or Excel export integration yet.
- There is no improved product data preview yet.
- V2 prompt/response quality has not been reviewed with several real API responses yet.
- Parser warnings and blocked rows may need clearer user-facing explanations.
- V2 still lives inside the larger `app.py` AI tab code path.

## 8. Risks Before Making V2 More Prominent

Main risks:

- Users may not immediately understand the difference between V1 product-level suggestions and V2 field-level suggestions.
- A raw table can feel too technical for portfolio/demo users.
- Blocked or review-required statuses need clearer visual explanation.
- Future approval/export features could accidentally imply product-data write-back if not planned carefully.
- Actual OpenAI responses may expose prompt/schema friction that tests do not cover.

Risk controls:

- Keep V2 labeled experimental until the result UX is clearer.
- Improve result presentation before adding approval workflow.
- Keep approval/export planning separate from runtime generation.
- Preserve raw response visibility for debugging, but keep it inside an expander.

## 9. Recommended Next Product Block

Recommended next block:

`Smart Suggestions v2 Result UX Polish`

Why this is the best next step:

- It creates visible product value without adding approval/export scope.
- It makes V2 easier to understand for demos and reviewers.
- It can improve status explanations, empty states, blocked-row messaging, and table readability.
- It keeps product data unchanged.
- It avoids jumping too early into approval workflow or improved-data export.

## 10. Suggested Scope for Next Block

Smart Suggestions v2 Result UX Polish should:

- Improve V2 result section copy.
- Add concise explanations for `approval_status` and `suggestion_status`.
- Make empty, blocked, and parser-error states easier to understand.
- Keep V1 unchanged.
- Keep exports unchanged.
- Avoid approval buttons.
- Avoid product data write-back.
- Avoid new dependencies.

Suggested allowed files:

- `app.py`
- documentation status files

Suggested checks:

- `python -m py_compile app.py`
- `python -m pytest`
- forbidden-file diff checks
