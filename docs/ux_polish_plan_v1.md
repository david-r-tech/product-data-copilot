# UX Polish Plan v1

This plan defines a small, safe UX polish pass for Product Data Copilot.

The goal is clarity, trust, and portfolio presentation. This is not a redesign and does not add new product features.

## 1. Current UX Strengths

- The app already follows a clear tab structure: Dashboard, Product Data, Scores, Issues, Review Tasks, Management Export, and AI Suggestions.
- The product name is visible and consistent: Product Data Copilot.
- Upload and sample-data fallback are simple to understand.
- Dashboard metrics give a quick catalog health overview.
- Issues, scores, review tasks, and exports are separated into understandable work areas.
- Smart Suggestions v2 is clearly marked experimental.
- AI suggestions are framed as human-reviewed draft recommendations.
- Improved export messaging already emphasizes that source product data is not changed automatically.
- Demo fixture support makes the Smart Suggestions v2 workflow testable without an API key.
- Manual QA docs now make export verification repeatable.

## 2. Current UX Friction Points

- The AI Suggestions tab has become long and contains V1 suggestions, V2 generation, fixture loading, human review, export preview, download, and raw response sections.
- Some safety messages are repeated in slightly different wording, which can feel noisy.
- Users may not immediately understand the recommended demo flow: load fixture, review rows, approve/reject, preview export, download workbook.
- Empty states sometimes explain what is missing but not always the next action.
- The difference between AI Suggestions v1 and Smart Suggestions v2 could be made clearer for non-technical reviewers.
- The improved export area could more explicitly say which workbook sheets will be generated.
- The manual approval workflow is session-only, but this detail should stay visible without overwhelming the user.
- Download buttons could benefit from more consistent surrounding text that explains what is inside each export.

## 3. Suggested Small Copy Improvements

These changes should be limited to visible text and captions.

- Replace long or technical captions with short action-oriented wording.
- Add a short "Recommended demo flow" caption in the Smart Suggestions v2 section:
  - Load demo records
  - Review one suggestion
  - Approve or reject
  - Preview export groups
  - Download workbook
- Clarify V1 vs V2:
  - V1: free-form content assistance for one product
  - V2: structured field-level suggestions for review and export
- Use consistent wording for safety:
  - "Draft only"
  - "Human review required"
  - "No source data is changed"
  - "Session-only decision"
- Rename or clarify the demo fixture expander caption so it is obviously test/demo data.
- Keep raw response and prompt preview inside collapsed expanders.

## 4. Suggested Section / Order Improvements

Keep the current tabs and overall navigation.

Recommended AI Suggestions tab order:

1. Product selection and current product context
2. AI Suggestions v1
3. Smart Suggestions v2 overview and safety note
4. Smart Suggestions v2 prompt preview
5. Demo fixture / V2 generation controls
6. Structured V2 suggestions table
7. Human review for one selected suggestion
8. Improved Product Data Export Preview
9. Improved Excel Export download
10. Raw response / technical details

Small improvement ideas:

- Keep advanced/debug content collapsed by default.
- Keep the improved export preview close to the human review section because it depends on review decisions.
- Avoid moving large blocks into new tabs until the current UX polish has been manually tested.
- Do not change dashboard, issue, score, or review task structure unless a later QA pass identifies a concrete problem.

## 5. Suggested Empty-State Improvements

Empty states should answer three questions:

1. What is missing?
2. Why does it matter?
3. What should the user do next?

Recommended empty states:

- No uploaded file:
  - "Using sample data. Upload CSV/XLSX in the sidebar to analyze your own product data."
- No issues:
  - "No issues found for the current checks. Review scores and exports before publishing."
- No Smart Suggestions v2 records:
  - "No structured suggestions yet. Load demo records or generate V2 suggestions to test the review workflow."
- Missing API key:
  - "Generation is disabled because OPENAI_API_KEY is missing. Demo records and prompt preview are still available."
- No approved export candidates:
  - "No approved candidates yet. Approve a non-blocked suggestion to populate the Approved Improvements sheet."
- Empty workbook group:
  - "This sheet is intentionally empty because no rows currently match this status."

## 6. Suggested Safety / Trust Messages

Safety and trust messaging should be visible but not repetitive.

Recommended persistent safety ideas:

- Near Smart Suggestions v2:
  - "AI suggestions are draft recommendations. A human must approve each usable row."
- Near Human Review:
  - "Review decisions are stored only in this session."
- Near Improved Export:
  - "Approved suggestions are export candidates only. Source product data is not changed."
- Near blocked rows:
  - "Blocked rows cannot be approved because required source or safety information is missing."
- Near downloads:
  - "Exports are local files generated from the current session."

Avoid:

- Legal compliance claims
- Marketplace publication claims
- Any wording that sounds like automatic correction or automatic publishing

## 7. Suggested Smart Suggestions v2 Clarity Improvements

Smart Suggestions v2 should feel like a controlled workflow, not a technical experiment only.

Recommended improvements:

- Add a short "What this section does" note:
  - "Creates structured field-level draft suggestions for human review."
- Add a short "What it does not do" note:
  - "It does not approve, publish, or update product data automatically."
- Explain the demo fixture in one line:
  - "Use demo records to test approval and export without an API key."
- Clarify the table:
  - `Current Value` = source/reference value
  - `Suggested Value` = draft recommendation
  - `Human Review Status` = session-only user decision
  - `Suggestion State` = parser/safety state
- Keep raw AI response collapsed and framed as troubleshooting content.

## 8. Suggested Improved Export Clarity Improvements

The improved export workflow should be easy to understand for product data managers.

Recommended improvements:

- Show a short list of workbook sheets before or near the download button.
- Explain that the workbook contains review groups, not rewritten product data.
- Make no-approved state explicit:
  - "The workbook can still be downloaded for review context, but Approved Improvements is empty."
- Keep naming consistent:
  - "Improved Product Data Export"
  - `product_data_copilot_improved_export.xlsx`
- Add a sentence that connects the preview and workbook:
  - "The workbook uses the same groups shown in this preview."

## 9. What Should Not Change Yet

Do not include these in UX Polish v1:

- No large UI redesign
- No new feature area
- No navigation rewrite
- No database or persistence
- No approval workflow rebuild
- No new export type
- No source product write-back
- No automatic AI mass generation
- No marketplace integration or preset flow
- No switch away from Streamlit

## 10. Recommended Implementation Phases

### Phase 1: Copy and Help Text Polish

Scope:

- Improve captions, info boxes, empty states, and safety notes.
- Keep layout and logic unchanged.
- Focus especially on Smart Suggestions v2 and Improved Product Data Export.

Allowed files for a future implementation block:

- `app.py`
- status docs

Checks:

- `python -m py_compile app.py`
- `python -m pytest`
- manual app smoke test

### Phase 2: Section Grouping / Order Polish

Scope:

- Keep current tabs.
- Move only small content blocks if it improves flow.
- Keep prompt/raw response/debug content inside expanders.
- Do not alter V1, V2 generation, approval, or export behavior.

Checks:

- `python -m py_compile app.py`
- `python -m pytest`
- manual walkthrough of AI Suggestions tab

### Phase 3: Manual UI QA

Scope:

- Walk through sample data, fixture loading, approval, export preview, workbook download, and existing exports.
- Verify no confusing safety wording remains.
- Capture notes for final portfolio polish.

Output:

- Short QA doc or checklist update.

### Phase 4: README / Portfolio Screenshot Update Later

Scope:

- Update README screenshots or portfolio docs only after UX copy has stabilized.
- Do not capture screenshots before the UI text and flow feel final.

## 11. Acceptance Criteria For UX Polish v1

UX Polish v1 should pass if:

- Existing functionality remains unchanged.
- Smart Suggestions v2 is easier to explain in a demo.
- Improved Export wording clearly protects source data.
- Empty states tell the user what to do next.
- Safety messages are visible but not overwhelming.
- No new architecture, persistence, or feature scope is introduced.

UX Polish v1 should fail if:

- The UI implies automatic product updates.
- The UI hides human-review requirements.
- The polish changes data processing, exports, AI behavior, or review decisions.
- The app becomes harder to demo.
