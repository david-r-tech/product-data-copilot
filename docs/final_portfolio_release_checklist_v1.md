# Product Data Copilot - Final Portfolio Release Checklist v1

This checklist is the final owner-facing readiness pass before Product Data Copilot is shared in a portfolio, CV, GitHub review, or colleague review.

It does not rename the GitHub repository, change source code, or change app behavior. It documents the final checks and manual owner tasks.

## 1. Code Readiness

Confirm the repository is technically clean:

- [ ] Working tree is clean:

```bash
git status
```

- [ ] Latest commit is pushed to GitHub.
- [ ] Automated tests pass:

```bash
python -m pytest
```

- [ ] App syntax check passes:

```bash
python -m py_compile app.py
```

- [ ] No forbidden runtime changes are pending.
- [ ] No `.env`, API keys, generated exports, private data, or local-only secrets are committed.

PASS if the repo is clean, tests are green, and no sensitive or generated files are staged.

FAIL if tests fail, the working tree is dirty without explanation, or secrets/generated files appear in Git.

## 2. App Manual QA

Run the app locally:

```bash
python -m streamlit run app.py
```

Check the main demo path:

- [ ] App starts without red runtime errors.
- [ ] Product name is visible as `Product Data Copilot`.
- [ ] Sample data loads when no file is uploaded.
- [ ] CSV/XLSX upload path still works.
- [ ] Product checks and dashboard results are understandable.
- [ ] Readiness scores are visible and understandable.
- [ ] Issues table and severity filters work.
- [ ] Review Tasks table and filters work.
- [ ] Manual review status override is understandable and session-only.
- [ ] Smart Suggestions v2 demo fixture flow works without an API key.
- [ ] Human Approval UI is understandable.
- [ ] Improved Product Data Export Preview groups suggestions correctly.
- [ ] Improved Excel export downloads.
- [ ] Workbook opens and planned sheets are present.

Required workbook sheets:

- Export Summary
- Approved Improvements
- Pending Suggestions
- Rejected Suggestions
- Blocked Suggestions
- Unknown Suggestions
- Original Source Snapshot

PASS if the app walkthrough works end to end with sample data and demo Smart Suggestions v2 records.

FAIL if the app crashes, the main tabs are missing, or the workbook cannot be opened.

## 3. AI Safety Readiness

Confirm AI safety is clear in the app and documentation:

- [ ] AI suggestions are clearly described as draft recommendations.
- [ ] No invented facts policy is visible in documentation.
- [ ] Structured suggestions include or explain source, reason, confidence, and risk context.
- [ ] Human approval is required.
- [ ] AI cannot approve itself.
- [ ] Blocked suggestions cannot be approved.
- [ ] Approved means export candidate only.
- [ ] Missing API key fallback is understandable.

PASS if a reviewer can understand that AI supports review but does not replace it.

FAIL if the app or docs imply AI suggestions are automatically trusted, approved, or applied.

## 4. Export Safety Readiness

Confirm source protection is clear:

- [ ] Original uploaded data is not overwritten.
- [ ] Improved export is generated as a separate workbook.
- [ ] Source snapshot is included in the workbook.
- [ ] No source write-back exists.
- [ ] No automatic mass change exists.
- [ ] Approved suggestions are export candidates only.
- [ ] Pending, rejected, blocked, and unknown suggestions stay separated.

PASS if the improved export is clearly a review handoff artifact.

FAIL if source product data is changed, or if the UI suggests automatic product updates.

## 5. GitHub / Portfolio Readiness

Confirm public-facing materials are present:

- [ ] README is clear and current.
- [ ] README explains product value within the first screen.
- [ ] README includes setup, run command, tests, architecture, safety, limitations, and roadmap.
- [ ] Portfolio case study exists:

```text
docs/portfolio_case_study.md
```

- [ ] Portfolio screenshot checklist exists:

```text
docs/portfolio_screenshot_checklist_v1.md
```

- [ ] GitHub repo rename checklist exists:

```text
docs/github_repo_rename_manual_checklist_v1.md
```

- [ ] Final screenshots still need to be captured manually.
- [ ] GitHub repository can later be renamed manually to:

```text
product-data-copilot
```

PASS if the repo explains the product, shows professional discipline, and has honest limitations.

FAIL if the README/case study overclaims production readiness or hides important limitations.

## 6. CV / Bewerbung Readiness

Recommended project title:

```text
Product Data Copilot
```

Current repository URL before manual rename:

```text
https://github.com/david-r-tech/commerce-readiness-ai
```

Future repository URL after manual rename:

```text
https://github.com/david-r-tech/product-data-copilot
```

Before using the project in a CV or Bewerbung:

- [ ] Use `Product Data Copilot` as the project title.
- [ ] Do not use the old product name as the current title.
- [ ] Use the current repository URL until the GitHub rename is complete.
- [ ] After manual rename, update CV, portfolio, LinkedIn, and saved links.
- [ ] Include a short description that mentions product data quality, AI-assisted suggestions, human review, and safe Excel export.

Example CV wording:

```text
Product Data Copilot - Local Streamlit product-data audit tool with CSV/XLSX upload, rule-based checks, readiness scoring, human-reviewed AI suggestions, pytest-covered helper modules, and safe Excel export workflow.
```

## 7. Known Limitations To Keep Honest

Do not hide these current boundaries:

- Not SaaS.
- No database.
- No login or multi-user roles.
- No marketplace integration.
- No automatic product write-back.
- No automatic AI mass generation.
- Session-only approval state.
- AI suggestions need human review.
- No legal compliance guarantees.
- Final screenshots are manual owner work.
- GitHub repository rename is still manual until the owner performs it.

These limitations are acceptable for a portfolio-grade local product prototype.

## 8. Final Manual Tasks For The Project Owner

Before sharing publicly:

- [ ] Run the app locally.
- [ ] Perform browser QA using `docs/ux_manual_qa_v1.md`.
- [ ] Perform improved export QA using `docs/improved_export_manual_qa.md`.
- [ ] Download and open the improved Excel export.
- [ ] Capture screenshots using `docs/portfolio_screenshot_checklist_v1.md`.
- [ ] Add final screenshots to the README or portfolio page when ready.
- [ ] Rename the GitHub repo manually when ready using `docs/github_repo_rename_manual_checklist_v1.md`.
- [ ] Update the local git remote after the GitHub rename.
- [ ] Update CV, GitHub profile, LinkedIn, and portfolio links.
- [ ] Ask a colleague to review the README, case study, and app walkthrough.

## 9. Acceptance Criteria

The project is portfolio-release ready when:

- [ ] It can be shown confidently as a portfolio-grade product prototype.
- [ ] README and case study explain the value clearly.
- [ ] Tests are green.
- [ ] App starts locally.
- [ ] Sample data demo path works.
- [ ] Smart Suggestions v2 demo and approval workflow are understandable.
- [ ] Improved Excel export downloads and opens.
- [ ] Export safety is clear.
- [ ] AI safety and human review are clear.
- [ ] No old product branding is prominent.
- [ ] No source write-back or auto-approval is implied.
- [ ] Manual screenshots and optional repo rename are the only major owner tasks left.

## 10. Recommended Next Step

Next recommended block:

```text
Final Docs Link Polish v1
```

Alternative: pause Codex work and complete manual owner tasks first:

- browser QA
- final screenshots
- colleague review
- manual GitHub repository rename
- CV / portfolio link updates
