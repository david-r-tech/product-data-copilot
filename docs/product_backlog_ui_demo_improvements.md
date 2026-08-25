# Product Data Copilot - UI and Demo Product Backlog

## Context

This backlog is based on the current Streamlit UI screenshots and the reported demo problem.

Observed user feedback:

- The interface feels too technical and not modern enough.
- Buttons are too small and not visually clear.
- Several tabs are difficult to understand without prior explanation.
- The user does not always know what to do next inside each tool area.
- A language switch between English and German would be useful, but is lower priority.
- The German furniture demo currently fails after upload with a dtype-related error.

This backlog should be handled step by step. It is not a request for a full redesign, a new framework, a database, SaaS, login, or marketplace integration.

## Product Goal

Make Product Data Copilot easier to demonstrate and easier to understand for non-technical users.

The immediate priority is:

1. The German furniture demo must work reliably.
2. The demo flow must feel simple: upload file, generate missing text, download result.
3. The UI should guide the user clearly through the next action.
4. The broader app should look more polished, but without breaking existing functionality.

## Priority Levels

- **P0 - Must fix before presentation:** Demo-breaking bugs and anything that prevents the main demo flow.
- **P1 - High value UX:** Changes that make the app easier to understand and present.
- **P2 - Useful polish:** Improvements that help quality but are not needed for the next demo.
- **P3 - Later:** Larger product ideas that should not distract from the current goal.

## Recommended Delivery Order

1. Fix German furniture demo bug.
2. Add a ready-to-use German furniture upload file.
3. Simplify and polish the `DE Demo` tab.
4. Improve main page and navigation clarity.
5. Improve button visibility and primary action styling.
6. Add tab-level guidance and empty states.
7. Plan language switch later.

## Backlog Items

### PBI-001 - Fix German Furniture Demo Export Bug

**Priority:** P0  
**Type:** Bug  
**User story:** As a presenter, I want the German furniture demo to generate the filled list without crashing, so that I can safely demonstrate the upload-to-download workflow.

**Problem observed:** After uploading a furniture Excel file and clicking `Demo-Liste erstellen`, the app shows: `Invalid value ... for dtype 'float64'`.

**Likely technical cause:** Some empty Excel text columns are inferred by pandas as `float64`. The demo logic later writes generated German text into those columns, which can fail with newer pandas dtype handling.

**Acceptance criteria:**

- Uploading the furniture Excel file works.
- Clicking `Demo-Liste erstellen` does not show a red error.
- Empty description, bulletpoint, and English translation fields are filled.
- Numeric columns such as width, height, depth, weight, and price remain usable.
- Original uploaded file is not overwritten.
- Download button appears after successful generation.

**Implementation notes:**

- In the demo export logic, explicitly cast target text columns to `object` or string-compatible dtype before assigning generated text.
- Keep the fix local to the German demo helper functions.
- Do not change the main audit/scoring logic.

**Suggested checks:**

- `python -m py_compile app.py`
- `python -m pytest`
- Manual test with the uploaded furniture file from the screenshot.

---

### PBI-002 - Add Ready-to-Use German Furniture Demo Upload File

**Priority:** P0  
**Type:** Demo readiness  
**User story:** As a presenter, I want a prepared German furniture Excel file in the project, so that I can start the demo without creating data manually.

**Acceptance criteria:**

- A German furniture demo upload file exists in `data/`.
- The file contains about 10 furniture products.
- It contains understandable German product names and attributes.
- The fields for description, bulletpoints, and English translation are intentionally empty.
- The file can be uploaded in the `DE Demo` tab.
- The file name is documented in README or demo docs.

**Implementation notes:**

- Recommended file name: `data/moebel_demo_upload.xlsx`.
- Use fictional furniture products.
- Keep the file small and presentation-friendly.

---

### PBI-003 - Simplify the German Demo Tab

**Priority:** P1  
**Type:** UX  
**User story:** As a non-technical viewer, I want the German demo tab to clearly show three steps, so that I immediately understand what the tool does.

**Acceptance criteria:**

- The tab starts with a simple German headline.
- The workflow is shown as three clear steps:
  1. Excel hochladen
  2. Texte erzeugen
  3. Ergebnis herunterladen
- The main button is visually clear and placed close to the uploaded file preview.
- The user sees a short explanation that no API key and no costs are required.
- The preview focuses on the relevant fields, not every technical column.

**Implementation notes:**

- Use `st.columns`, `st.info`, `st.success`, and concise German copy.
- Avoid showing too many technical details by default.
- Keep technical error details in an expander.

---

### PBI-004 - Make Primary Buttons Larger and Easier to See

**Priority:** P1  
**Type:** UI polish  
**User story:** As a user, I want important actions to stand out, so that I know where to click next.

**Acceptance criteria:**

- Primary demo actions use clear labels and primary button styling where possible.
- Important buttons are not visually lost below large data tables.
- Button labels are action-oriented, for example `Demo-Liste erstellen` and `Excel herunterladen`.
- The button order follows the user workflow.

**Implementation notes:**

- Streamlit supports `type="primary"` on buttons/download buttons.
- Keep the visual changes small and safe.
- Do not introduce a custom frontend framework.

---

### PBI-005 - Add a Cleaner Landing / Start Area

**Priority:** P1  
**Type:** UX  
**User story:** As a first-time user, I want to understand the product value within a few seconds, so that I know what the app is for.

**Acceptance criteria:**

- The top area explains the product in plain language.
- The user sees the main workflow: upload, check, review, export.
- The demo path is visible and easy to find.
- The header does not feel like a raw developer tool.

**Implementation notes:**

- Add a compact intro band or workflow summary near the top.
- Keep existing tabs and functionality.
- Do not create a marketing landing page that hides the tool.

---

### PBI-006 - Add Tab-Level Guidance

**Priority:** P1  
**Type:** Usability  
**User story:** As a user, I want each tab to tell me what it is for and what I should do there, so that I do not get lost.

**Acceptance criteria:**

- Every major tab has a one-sentence purpose statement.
- Complex tabs include a short “What to do here” note.
- AI and export tabs clearly explain safety boundaries.
- Guidance is concise and does not overload the UI.

**Implementation notes:**

- Good candidates: Product Data, Scores, Issues, Review Tasks, Management Export, AI Suggestions, DE Demo.
- Keep copy in English for existing app tabs unless a language switch is introduced later.
- `DE Demo` should remain German.

---

### PBI-007 - Improve Data Table Readability

**Priority:** P1  
**Type:** UX  
**User story:** As a user, I want large product tables to be easier to scan, so that I can understand the data without horizontal confusion.

**Acceptance criteria:**

- Product preview does not overwhelm the user immediately.
- Important columns are shown first.
- Optional raw/full data remains accessible.
- Long text columns do not dominate the first view.

**Implementation notes:**

- Consider a compact preview with selected columns.
- Keep full dataframe available in an expander.
- Do not change uploaded data or scoring inputs.

---

### PBI-008 - Improve Empty States and Error Messages

**Priority:** P1  
**Type:** UX / trust  
**User story:** As a user, I want helpful messages when something is missing or fails, so that I know what to do next.

**Acceptance criteria:**

- Demo upload errors explain the likely cause in plain German.
- Technical details remain available but collapsed.
- Missing API key messages are clear and non-alarming.
- Empty suggestion/export states tell the user the next action.

**Implementation notes:**

- Avoid exposing sensitive information.
- Keep tracebacks out of the main UI.
- Use `st.expander("Technische Details")` or `Technical details`.

---

### PBI-009 - Create a Guided Presentation Mode

**Priority:** P2  
**Type:** Demo experience  
**User story:** As a presenter, I want a simplified presentation mode, so that I can show the value without exposing all advanced workflow tabs.

**Acceptance criteria:**

- A simple demo path is available for presentations.
- Advanced audit/AI/export tools remain available but do not distract.
- The presenter can show a short end-to-end story in 3-5 minutes.

**Implementation notes:**

- Could be a separate tab or a sidebar toggle.
- Should not replace the full app.
- Keep this after the `DE Demo` bug and UX polish are stable.

---

### PBI-010 - Add Language Setting: English / German

**Priority:** P2  
**Type:** Internationalization planning  
**User story:** As a German-speaking user, I want to switch the app language to German, so that I can present or use the app more naturally.

**Acceptance criteria:**

- A language selector exists.
- Key UI labels can switch between English and German.
- The implementation does not require rewriting all business logic.
- Default language remains stable.

**Implementation notes:**

- Low priority according to user feedback.
- Should be planned before implementation.
- Avoid translating internal column names in exported data unless deliberately planned.

---

### PBI-011 - Separate Simple Demo from Advanced AI Workflow

**Priority:** P2  
**Type:** Product clarity  
**User story:** As a viewer, I want the simple demo and the advanced AI workflow to be clearly separated, so that I do not confuse deterministic demo output with real AI generation.

**Acceptance criteria:**

- `DE Demo` clearly states that it is deterministic and no-cost.
- AI Suggestions clearly state when OpenAI is required.
- Demo-generated output is not marketed as live AI unless an actual API call is used.
- Portfolio explanation remains honest.

**Implementation notes:**

- Important for credibility.
- Do not overclaim AI behavior.

---

### PBI-012 - Modernize Visual Styling Without Framework Change

**Priority:** P2  
**Type:** UI polish  
**User story:** As a user, I want the app to feel more modern and polished, so that it looks like a serious product prototype rather than a raw Streamlit table viewer.

**Acceptance criteria:**

- Better spacing between sections.
- Clearer hierarchy between title, explanation, metrics, and actions.
- Important actions are visually emphasized.
- Tables are placed after context, not as the first overwhelming element.
- Existing functionality remains unchanged.

**Implementation notes:**

- Use Streamlit-native layout first.
- Avoid custom CSS unless a small, controlled style block is clearly worth it.
- Do not redesign the whole app in one step.

## Suggested Next Execution Blocks

### Block 1 - German Demo Bug Fix v1

Goal: Fix the dtype crash shown in the screenshot and verify the furniture demo end-to-end.

Allowed scope:

- `app.py`, only German demo helper functions and `DE Demo` tab.
- `data/moebel_demo_upload.xlsx` if missing.
- Minimal README/project log update.

Do not change:

- AI Suggestions
- Main scoring
- Product checks
- Exports outside `DE Demo`

### Block 2 - German Demo UX Polish v1

Goal: Make the `DE Demo` tab simple, clear, and presentation-ready.

Main changes:

- Bigger primary action style.
- Three-step guidance.
- Cleaner preview.
- Better success and error messages.

### Block 3 - Main App Navigation Clarity v1

Goal: Make the current tab structure easier to understand without redesigning the full app.

Main changes:

- Short tab explanations.
- Better page intro.
- Clearer callouts.

### Block 4 - Data Table Readability v1

Goal: Reduce visual overload in product table views.

Main changes:

- Compact column preview.
- Full raw data in expander.
- Better captions.

### Block 5 - Language Switch Planning v1

Goal: Plan English/German language switching safely before implementation.

Main changes:

- Identify labels/copy to translate.
- Decide what should remain technical English.
- Avoid breaking tests or exports.

## Definition of Done for This UX Backlog

- The German demo works without red errors.
- A presenter can explain the demo in under 5 minutes.
- Main buttons are visually clearer.
- Each tab has enough guidance for a first-time user.
- Advanced AI/export safety remains honest and visible.
- Tests pass after code changes.
- No source data is overwritten automatically.
- No new database, login, SaaS, or marketplace integration is introduced.

