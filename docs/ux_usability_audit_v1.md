# UX & Usability Audit v1 - Product Data Copilot

## Scope

This audit reviews the current Streamlit app from a product and usability perspective. It is analysis only. No runtime behavior, business logic, AI logic, export logic, or navigation behavior was changed in this block.

The current app already has strong functional coverage: upload, product checks, scores, issues, review tasks, AI suggestions, Smart Suggestions v2, human approval, management export, and improved export. The completed German furniture presentation demo has been removed from the active product workflow, so the next UX work should focus only on the core Product Data Copilot app.

## Target User Journey

The intended workflow should be immediately recognizable:

`Upload -> Data Check -> Review -> AI Improvements -> Approval -> Export`

Today, this workflow exists in the product, but it is spread across many tabs and several different export/AI concepts. A new user can use the tool, but needs guidance to understand the normal audit-to-export workflow.

## Current UX Strengths

- Clear final product branding with Product Data Copilot.
- Useful end-to-end capabilities for a local MVP.
- Strong safety positioning: AI suggestions are drafts, human review is required, and source product data is not overwritten automatically.
- Smart Suggestions v2 includes source/reason/confidence and review-required states, which makes the AI workflow more credible.
- Export workflows are intentionally separate from source data mutation.
- Tests and documentation make the project look more disciplined than a typical one-file demo.

## Critical Findings

### 1. Full app workflow is not visually guided enough

- Problem: The main tab row lists many capabilities, but it does not clearly frame the intended workflow from upload to export.
- Why it matters: A new user may see many tools but not immediately understand the correct order of work.
- Improvement idea: Add a small workflow orientation near the top: `1 Upload -> 2 Check -> 3 Review -> 4 Improve -> 5 Export`. Keep it as concise copy, not a new navigation system.
- Affected area / file: `app.py`, main app header area.
- Effort: Small
- Risk: Low

### 2. AI Suggestions tab mixes V1, V2, approval, fixture demo, preview, and export

- Problem: The `AI Suggestions` tab contains several concepts at once: AI Suggestions v1, Smart Suggestions v2, fixture loading, human approval, export preview, and improved Excel download.
- Why it matters: For a business user, it can be unclear which AI flow is current, which is experimental, and which output is safe to use.
- Improvement idea: Add clearer section grouping and short labels such as `Classic AI Suggestions`, `Structured Smart Suggestions v2`, `Human Review`, and `Improved Export Preview`. Do not change logic.
- Affected area / file: `app.py`, `AI Suggestions` tab.
- Effort: Medium
- Risk: Low

### 3. Export purpose is split across multiple places

- Problem: There are several downloads: product scores CSV, issues CSV, review tasks CSV, management workbook, AI suggestions CSV, and improved product data workbook.
- Why it matters: Users may not understand which export is for management, which is for review work, and which is for improved product data.
- Improvement idea: Add short purpose text beside each major export. For example: `Management Export = audit report`, `Improved Export = approved suggestion candidates`.
- Affected area / file: `app.py`, export-related sections.
- Effort: Small
- Risk: Low

### 4. Review workflow should clearly separate task review and AI suggestion review

- Problem: The `Review Tasks` tab manages product data audit tasks, while Smart Suggestions v2 has its own session-only suggestion approval flow.
- Why it matters: Both are valid, but users may not immediately understand the difference between reviewing issues and approving AI suggestion candidates.
- Improvement idea: Add a short distinction: `Review Tasks = audit task management`, `Smart Suggestions v2 Review = suggestion approval before export candidates`.
- Affected area / file: `app.py`, `Review Tasks` and `AI Suggestions` tabs.
- Effort: Small
- Risk: Low

## High-Value Findings

### 1. Start/upload area could explain the next action more strongly

- Problem: Upload/sample data works, but the next best step is not always obvious.
- Why it matters: New users need immediate confidence after loading data.
- Improvement idea: Add one short line after data source notice: `Next: open Scores or Issues to see what needs attention.`
- Affected area / file: `app.py`, top data input/status area.
- Effort: Small
- Risk: Low

### 2. Dashboard KPIs are useful but lack interpretation

- Problem: Metrics show counts and average scores, but do not explain whether the dataset is healthy or problematic.
- Why it matters: Product managers and business reviewers need interpretation, not only numbers.
- Improvement idea: Add a compact status message based on critical issues or average overall score, without changing scoring logic.
- Affected area / file: `app.py`, `Dashboard` tab.
- Effort: Small
- Risk: Low to Medium, depending on whether interpretation text is purely descriptive.

### 3. Tables are functional but visually heavy

- Problem: Several tabs lead with wide tables, which can feel technical and dense.
- Why it matters: A portfolio/demo user may struggle to identify the important columns first.
- Improvement idea: Use short intros and selected column previews where appropriate. Keep full tables available in expanders or existing table views.
- Affected area / file: `app.py`, `Product Data`, `Scores`, `Issues`, `Review Tasks`, `AI Suggestions`.
- Effort: Medium
- Risk: Medium if column selection changes user expectations.

### 4. Manual Review Status Override could sound more like a product workflow

- Problem: The label is accurate but a little technical.
- Why it matters: Business users respond better to task language than internal override language.
- Improvement idea: Rename visible copy to something like `Set Product Review Status` while keeping session-state keys unchanged.
- Affected area / file: `app.py`, `Review Tasks` tab.
- Effort: Small
- Risk: Low

### 5. Button hierarchy could be clearer

- Problem: Some primary actions and secondary actions compete visually, especially in AI/export areas.
- Why it matters: Users should know which button to click next.
- Improvement idea: Keep only the main step action as `type="primary"` in each section and treat secondary actions as normal buttons.
- Affected area / file: `app.py`, `AI Suggestions` and export areas.
- Effort: Small
- Risk: Low

### 6. Smart Suggestions v2 safety details are good but technical

- Problem: Concepts such as parser output, fixture data, raw response, and blocked records are useful but can dominate the business story.
- Why it matters: A non-technical user needs the simple trust model first: source, reason, confidence, human approval.
- Improvement idea: Keep technical details collapsed and lead with a simple explanation: `Every suggestion must show source, reason, confidence, and review status.`
- Affected area / file: `app.py`, `AI Suggestions` tab.
- Effort: Small
- Risk: Low

## Nice-to-Have Findings

### 1. Language toggle would improve accessibility but is lower priority

- Problem: The app is primarily English, which may be less comfortable for German-speaking business users.
- Why it matters: German business users may prefer a fully German UI.
- Improvement idea: Plan a later lightweight language mode for visible copy only. Avoid translating internal field names or data model keys too early.
- Affected area / file: likely `app.py` and future UI copy helpers.
- Effort: Large
- Risk: Medium

### 2. Icons or badges could improve status scanning

- Problem: Statuses are text-heavy.
- Why it matters: Badges for severity, approval, blocked, and ready states would make tables easier to scan.
- Improvement idea: Add simple status badges or consistent symbols in visible labels, without changing stored values.
- Affected area / file: `app.py`, table display sections.
- Effort: Medium
- Risk: Low to Medium

### 3. Tab names could be more workflow-oriented later

- Problem: Current tabs are feature names, not workflow steps.
- Why it matters: A task-based workflow may be easier for new users.
- Improvement idea: Later consider labels like `1 Data`, `2 Scores`, `3 Review`, `4 AI`, `5 Export`. Do not change navigation in the first polish pass.
- Affected area / file: `app.py`.
- Effort: Small
- Risk: Medium because it changes navigation familiarity.

### 4. More visual summary charts could help portfolio screenshots

- Problem: Metrics and tables are solid, but screenshots may look table-heavy.
- Why it matters: Portfolio viewers often judge quickly from screenshots.
- Improvement idea: Add simple bar charts for issue severity or review status in a later polish pass.
- Affected area / file: `app.py`, dashboard/review areas.
- Effort: Medium
- Risk: Low

### 5. CSS polish could make Streamlit feel less default

- Problem: Streamlit default styling can still feel like a technical demo.
- Why it matters: A stronger visual shell would improve perceived product quality.
- Improvement idea: Add minimal CSS for spacing, max-width on intro sections, and button clarity. Avoid a full redesign.
- Affected area / file: `app.py` or a future UI style helper.
- Effort: Medium
- Risk: Medium

## Export Experience Notes

- Management Export should be described as the audit/reporting workbook.
- Improved Product Data Export should be described as approved suggestion candidates only.
- The safest UX principle: exports should always say whether they are reporting, reviewing, or preparing improved data.

## AI Suggestions Notes

- The AI safety model is strong and should stay visible.
- The business-facing explanation should come before technical details.
- Raw response, parser details, and fixture details should remain collapsed.
- V1 should remain available but visually subordinate to the safer Smart Suggestions v2 story later.

## Review Workflow Notes

- The main review workflow would benefit from similarly clear "what remains" language.
- Export should continue to show only final business status where appropriate, while detailed review state stays inside the tool.

## Recommended UX Polish Phase 1

Phase 1 should stay small and avoid business logic, AI logic, export logic, and navigation changes.

### Included improvements

1. Add a compact workflow orientation below the app header: `Upload -> Check -> Review -> Improve -> Export`.
2. Add short purpose labels for the two major export concepts: Management Export and Improved Product Data Export.
3. Improve visible section headings in the `AI Suggestions` tab so V1, Smart Suggestions v2, Human Review, and Improved Export Preview are easier to distinguish.
4. Improve `Review Tasks` copy from internal override language toward business review language while keeping state keys unchanged.

### Explicit exclusions for Phase 1

- No tab reorder.
- No CSS redesign.
- No new data model.
- No AI prompt changes.
- No export behavior changes.
- No scoring or rule changes.
- No package/module refactor.
- No language toggle implementation.

### Acceptance criteria for Phase 1

- A new user can understand the workflow in under 30 seconds.
- The difference between audit task review, AI suggestion review, and export candidates is clearer.
- No existing button behavior changes.
- No session-state keys change.
- Existing tests still pass.
- The presentation demo remains stable.

## Risks and Constraints

- The current working tree already contains uncommitted runtime and documentation changes from previous blocks. This audit should not be mixed into those changes without explicit review.
- Streamlit is still the correct UI technology for now; replacing it would be scope creep.
- The biggest UX risk is trying to solve everything with one polish pass. The next implementation block should remain small.
- The current product is powerful enough for portfolio use, but the UI should increasingly communicate workflow instead of feature inventory.
