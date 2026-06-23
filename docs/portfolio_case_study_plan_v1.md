# Product Data Copilot - Portfolio Case Study Plan v1

This plan defines how the final portfolio case study for Product Data Copilot should be structured.

The case study should present the project strongly and honestly. It should show product thinking, engineering discipline, AI safety awareness, and practical e-commerce business value without claiming that the MVP is already a production SaaS product.

## 1. Target Audience

The case study should work for several reader groups:

- Developers who want to see code structure, tests, helper extraction, and safety boundaries.
- Product managers who want to understand the user problem, workflow, trade-offs, and roadmap.
- Project managers who want to see phased delivery, documentation discipline, QA, and scope control.
- E-commerce and marketing teams who care about product data quality, marketplace readiness, review work, and exports.
- Recruiters or technical reviewers who need a clear overview of what was built and why it matters.

Tone:

- Professional
- Practical
- Honest about MVP limits
- Business-aware, not just technical
- Clear enough for non-coders

## 2. Core Story

### Problem

E-commerce teams often manage product data in CSV/XLSX files, PIM exports, and marketplace templates. Before publishing, they need to know which products have missing, weak, risky, or incomplete data.

Typical pain points:

- Missing required fields
- Weak titles and descriptions
- Missing EAN/GTIN values
- Missing translations
- Missing warning notes for safety-relevant categories
- No clear prioritization
- Manual spreadsheet review work
- Unclear handoff between business review and data improvement

### Product Idea

Product Data Copilot turns a product file into a structured audit workflow:

1. Load product data.
2. Detect product data issues.
3. Score readiness.
4. Create review tasks.
5. Generate draft AI suggestions for selected products.
6. Require human review.
7. Export management and improvement handoff workbooks.

### Solution

The MVP is a local Streamlit tool that combines:

- Product data quality checks
- Readiness scoring
- Review task creation
- Session-based review decisions
- Safe AI suggestions
- Management and improved-data export workflows
- Manual QA documentation

### Why AI Is Useful Here

AI can help draft product titles, descriptions, bullet points, translations, and field-level improvement suggestions faster than manual writing from scratch.

AI is useful because it can:

- Turn weak product content into better drafts
- Summarize likely improvements
- Suggest field-level corrections or enrichments
- Support product data managers during review

### Why Human Review Is Required

AI can invent facts, misunderstand product context, or produce unsafe claims. Product data is business-critical and sometimes compliance-relevant.

The case study should emphasize:

- AI suggestions are drafts
- AI cannot approve itself
- Source fields are required
- Reasons and confidence are required
- Blocked/unsafe output stays non-approvable
- Approved suggestions are export candidates only
- No automatic write-back to source product data

## 3. Suggested Case Study Structure

### 1. Short Product Summary

Explain Product Data Copilot in 3-5 sentences.

Include:

- Local Streamlit MVP
- E-commerce product data audit workflow
- Readiness scoring, review tasks, AI suggestions, and exports
- Human-in-the-loop safety model

### 2. Problem Statement

Describe the product data operations problem.

Cover:

- Messy product files
- Missing marketplace-critical fields
- Manual review effort
- Lack of prioritization
- Risk of publishing incomplete product data

### 3. Target Users

Describe:

- Product data managers
- Marketplace managers
- E-commerce operations teams
- Category managers
- Marketing/content teams

Explain what each user gets from the tool.

### 4. Key Workflows

Recommended workflow sections:

- CSV/XLSX upload and sample data fallback
- Product data audit
- Readiness scores
- Issues and severity filtering
- Review tasks and manual review status
- AI Suggestions v1
- Smart Suggestions v2
- Human approval UI
- Management Export
- Improved Product Data Export

### 5. Architecture Overview

Show that the project moved beyond a single rough script.

Cover:

- Streamlit as local-first UI
- `app.py` as the runtime shell
- Import-safe helper modules under `src/product_data_copilot/`
- Rules / validators
- Scoring helpers
- Review helpers
- Export helpers
- AI schema / parser / prompt adapter helpers
- UI helper extraction
- Pytest coverage for pure helpers

Keep this section high-level; do not paste large code blocks.

### 6. AI Safety Design

Explain the safety model:

- No invented facts policy
- Source fields required
- Reason required
- Confidence/risk status visible
- Parser-normalized output
- Blocked rows cannot be approved
- AI cannot mark suggestions approved
- User approval is session-only
- Approved suggestions are export candidates only
- No automatic write-back

### 7. Data Quality Rules

Summarize practical checks:

- Missing product name
- Short/generic product name
- Missing or short description
- Missing brand/manufacturer
- Missing category
- Missing or invalid EAN
- Missing or invalid price
- Missing attributes
- Missing/suspicious image URL
- Missing translations
- Missing warning notes for safety-relevant categories

Show that checks are business-relevant and understandable.

### 8. Review Workflow

Explain how issues become tasks.

Cover:

- Task type
- Priority
- Review status
- Filters
- Manual status override
- Session-only limitation
- No automatic data changes

### 9. Improved Export Workflow

Explain the improved export path:

- Smart Suggestions v2 review decisions
- Approved / pending / rejected / blocked / unknown groups
- Original Source Snapshot
- Excel workbook as a review handoff artifact
- Approved suggestions as export candidates only
- Source data unchanged

### 10. Testing Strategy

Cover:

- Pytest coverage for extracted helpers
- Parser and schema tests for Smart Suggestions v2
- Export helper tests
- Manual QA checklists
- Browser QA for UX clarity
- Syntax checks for `app.py`

Mention current known test count from status docs when drafting.

### 11. Roadmap / Next Steps

Keep this honest and scoped:

- Finish portfolio case study and screenshots
- Improve UI grouping if needed after manual QA
- Expand tests around business rules
- Improve Excel formatting
- Plan persistence only later
- Plan marketplace presets only later
- Keep integrations out of current MVP

### 12. Screenshots To Capture Later

Screenshots should be captured after final manual UI QA.

Recommended screenshots:

- Landing / upload area: shows product identity and local workflow.
- Dashboard: shows management-level overview.
- Readiness Scores: shows explainable product scoring.
- Issues Table: shows detected product data problems.
- Review Tasks: shows operational task workflow.
- AI Suggestions v1: shows draft content support and missing-key fallback if useful.
- Smart Suggestions v2: shows structured field-level suggestion rows.
- Human Approval UI: shows approve/reject/pending/blocked review model.
- Improved Product Data Export Preview: shows export group separation.
- Excel Export Workbook: shows workbook sheets and source snapshot.

Each screenshot should have a short caption explaining why it matters.

## 4. What Makes This Project Portfolio-Worthy

The case study should highlight:

- Professional Python structure with extracted helper modules
- Tests for pure business/helper logic
- Streamlit UI for a fast local product workflow
- Realistic sample data with intentional quality issues
- Rule-based product data checks
- Explainable readiness scoring
- Review task workflow
- Human-in-the-loop AI design
- AI guardrails and parser normalization
- No invented facts policy
- Session-only approval and blocked-row protection
- Safe export design with source data protection
- Management and improved Excel exports
- Clear documentation, QA checklists, and project logs
- Phased delivery with scope control

The project should be positioned as:

- A strong local MVP
- A portfolio-ready product demo
- A foundation for a more production-ready tool

It should not be positioned as:

- A finished enterprise SaaS product
- A deployed marketplace integration
- A legally/compliance-certified tool

## 5. What Not To Claim

Avoid these claims:

- Not a SaaS product yet
- No production database
- No user accounts or multi-user roles
- No real marketplace integrations
- No automatic product data write-back
- No guaranteed AI correctness
- No legal compliance guarantee
- Not fully enterprise-ready yet
- No permanent approval persistence yet
- No bulk AI generation for full catalogs

Safe wording:

- "local MVP"
- "portfolio demo"
- "human-reviewed draft suggestions"
- "export candidates"
- "source data remains unchanged"
- "foundation for future productization"

## 6. Recommended Writing Phases

### Phase 1: Case Study Plan

This document.

Output:

- target audience
- story arc
- structure
- screenshot list
- claims boundary

### Phase 2: Draft Case Study Markdown

Create or update:

- `docs/portfolio_case_study.md`

Scope:

- write a polished but honest first full draft
- use placeholders for screenshots
- keep claims aligned with current app capabilities

### Phase 3: Screenshot Checklist

Update screenshot planning docs after the draft exists.

Scope:

- screenshot name
- where to capture it
- what it proves
- caption text

### Phase 4: README / Portfolio Linking

After the case study draft is stable:

- link the case study from README if useful
- keep README concise
- avoid turning README into a long case study

### Phase 5: Final Polish

Final pass should check:

- consistency with app UI
- no exaggerated claims
- no stale names or old branding
- screenshot placeholders are clear
- technical sections are understandable
- business value is visible

## 7. Drafting Guidelines

When writing the actual case study:

- Start with the problem and user value, not the tech stack.
- Use concise paragraphs and short bullet lists.
- Mention technical architecture only after the product workflow is clear.
- Include trade-offs: local-first Streamlit, session-only review, no database yet.
- Keep AI safety explicit and easy to understand.
- Show engineering maturity through tests, helper modules, QA docs, and scope control.
- Do not apologize for MVP limitations; frame them as deliberate scope choices.

## 8. Acceptance Criteria For The Future Draft

The future case study draft should pass if:

- A non-technical reviewer understands the product problem and workflow.
- A developer sees evidence of code quality, tests, and modularization.
- A product/project manager sees phased delivery and scope control.
- AI safety and human review are clear.
- Export safety is clear.
- Limitations are honest.
- Screenshots to add later are clearly marked.

It should fail if:

- It claims production readiness that does not exist.
- It hides current limitations.
- It sounds like marketing fluff instead of a grounded product case study.
- It does not explain why human review matters.
- It does not show the engineering work behind the MVP.
