# AGENTS.md - Product Data Copilot

## Product

Product Data Copilot is a local Streamlit MVP for e-commerce product data quality, readiness scoring, review tasks, user-triggered product-copy creation and translation, and safe Excel exports.

The project direction is professional, maintainable, and deliberately local-first. Future work should improve usefulness and code quality without drifting into SaaS, integrations, or production infrastructure unless explicitly requested.

## Default Context

For most future Codex tasks, read:

1. `docs/current_context.md`
2. `AGENTS.md`
3. The specific files named by the task

Read longer docs such as the master blueprint, refactor inventory, or requirements only when the task is about architecture, planning, or product scope.

## Scope Rules

Work only on the requested block. Do not add these without explicit approval:

- Deployment, hosting, SaaS billing, login, user accounts, or database persistence
- Shopware, Shopify, Plentymarkets, marketplace presets, or external integrations
- Tkinter UI, desktop drag-and-drop, or major UI rewrites
- Automatic AI mass generation
- Automatic write-back or auto-approval of AI suggestions
- Legal advice or compliance guarantees

## Code Rules

- Preserve app behavior unless the task explicitly allows behavior changes.
- Keep changes small, reviewable, and targeted.
- Prefer pure, import-safe helpers in `src/product_data_copilot/`.
- Avoid broad refactors and unrelated formatting churn.
- Keep `.env` ignored and never store secrets.

## Documentation Rules

- Update `README.md` only when setup, usage, export, AI, or workflow behavior changes.
- Future prompts should reference `docs/current_context.md` instead of repeating full project history.

## Checks

Run the checks requested by the task. Common checks:

```bash
python -m py_compile app.py
python -m pytest
git diff --check
git diff --name-only -- app.py src tests requirements.txt data/sample_products.csv
git status --short
```

Commit and push only when checks pass and the task asks for it. Stage only allowed files.

## Compact Report

Use this format unless the task asks for a different one:

1. Result
2. Files changed
3. What changed
4. Checks
5. Commit/push
6. Risks
7. Next
