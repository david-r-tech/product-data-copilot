# Product Data Copilot - README Final Polish Plan v1

This plan defines the final README polish before the project is presented on GitHub or in a portfolio.

The README should stay concise. The detailed story belongs in `docs/portfolio_case_study.md`; the README should act as the fast entry point for reviewers.

## 1. README Goal

The final README should help a new visitor understand the project quickly.

It should:

- Explain what Product Data Copilot does in the first 30 seconds.
- Show why the project is portfolio-worthy.
- Help someone run the app locally without confusion.
- Make the sample-data workflow clear.
- Explain AI safety and human review clearly.
- Explain export safety and source-data protection clearly.
- Link to the portfolio case study and screenshot checklist.
- Stay honest about current MVP limitations.

## 2. Recommended README Structure

Recommended final structure:

1. Project title
2. Short product pitch
3. Screenshot placeholder near the top
4. Problem / business value
5. Key features
6. Demo workflow
7. Installation
8. Run command
9. Tests
10. Architecture overview
11. AI safety / human review
12. Improved export workflow
13. Project status
14. Current limitations
15. Case study and documentation links
16. Roadmap
17. License note if applicable

The README should not duplicate the whole case study. It should link to it.

## 3. What To Improve From The Current README

Potential final polish items:

- Add a screenshot placeholder near the top, for example:
  - `TODO: Add final dashboard screenshot after manual capture.`
- Add a clear link to `docs/portfolio_case_study.md`.
- Add a clear link to `docs/portfolio_screenshot_checklist_v1.md`.
- Add a short `Run tests` section with:
  - `python -m pytest`
- Update the roadmap to reflect current status:
  - case study draft exists
  - screenshot checklist exists
  - README final polish is next
- Mention the improved Excel export workflow more clearly:
  - approved suggestions are export candidates only
  - original source data remains unchanged
  - workbook contains source snapshot
- Clarify Smart Suggestions v2 wording:
  - experimental
  - structured field-level suggestions
  - session-only human review
  - no automatic write-back
- Ensure old `Commerce Readiness AI` naming appears only as historical context.
- Keep installation and local start instructions short and visible.

## 4. What Not To Do

Do not:

- Overclaim production readiness.
- Claim SaaS, enterprise, or marketplace integration readiness.
- Add fake screenshots.
- Add screenshots before they are manually captured.
- Add unimplemented features.
- Change product logic.
- Turn the README into a long case study.
- Hide limitations such as no database, no login, no integrations, and session-only approval state.

## 5. Suggested README Acceptance Criteria

The final README should pass if:

- A visitor understands the product within 30 seconds.
- The local setup path is clear.
- The run command is easy to find.
- The test command is visible.
- AI safety and human review are clear.
- Export safety and unchanged source data are clear.
- The case study is linked.
- The screenshot checklist or screenshot plan is linked.
- Limitations are honest and not buried.
- The project feels like a polished local MVP and portfolio prototype, not an overclaimed production product.

It should fail if:

- It implies automatic AI approval or source data write-back.
- It implies production SaaS readiness.
- It lacks clear local setup instructions.
- It does not link to the case study.
- It uses stale product naming.
- It becomes too long for a GitHub landing page.

## 6. Recommended Next Implementation Block

Next block:

```text
README Final Polish v1
```

Recommended allowed files for the next block:

- `README.md`
- `docs/current_context.md`
- `docs/project_status.md`
- `docs/codex_task_backlog.md`
- `docs/commerce_readiness_ai_project_log.md`

Recommended forbidden files:

- `app.py`
- `src/`
- `tests/`
- `requirements.txt`
- `data/`
- `sample_data/`

Recommended checks:

```bash
git status
git diff --check
```

Running `pytest` can stay optional for the README-only implementation block unless runtime files are unexpectedly touched.
