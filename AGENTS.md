# AGENTS.md - Product Data Copilot

## Product Context

Product Data Copilot is the professional product direction for the current Commerce Readiness AI Streamlit MVP.

The goal is to evolve the working local MVP into a professional, almost sellable product-data tool for e-commerce teams. The app should help users check product data, detect missing or inconsistent values, prioritize issues, generate review tasks, support safe AI suggestions, and export useful business artifacts.

Primary users:

- Product Data Managers
- Marketplace Managers
- E-Commerce Operations teams
- Category teams
- Business stakeholders reviewing product data readiness

Core value:

- Check product data quality
- Evaluate product readiness
- Prioritize problems
- Generate review tasks
- Support human-reviewed AI suggestions
- Provide useful exports for business workflows

## Core Rule: No Scope Creep

Work only on the current approved task.

Do not add these without explicit task approval:

- Release or deployment work
- SaaS billing
- Login, user accounts, or multi-user features
- Database migrations or persistence layers
- Shopware API
- Plentymarkets API
- Shopify app or API integration
- Marketplace-specific rule presets
- Large framework refactoring
- Tkinter UI
- Desktop drag-and-drop UI
- Automatic mass generation of AI text
- Automatic application of AI suggestions to product data
- Legal advice or compliance guarantees

## Development Mode

- Keep existing app behavior stable unless the current task explicitly allows behavior changes.
- Prefer focused, safe increments over broad rewrites.
- Do not refactor code unless refactoring is the explicit task.
- Do not add app features unless the task explicitly asks for them.
- Keep code readable and beginner-friendly.
- Add comments only where they explain non-obvious logic.
- Preserve current CSV/XLSX upload, checks, scores, review workflow, exports, and AI fallback behavior unless explicitly instructed otherwise.

## Required Reading Before Larger Work

For larger tasks, read the relevant context before editing:

- `AGENTS.md`
- `docs/master_product_architecture_blueprint.md`
- `docs/codebase_refactor_inventory.md`
- `docs/testing_strategy.md`
- `docs/product_requirements.md`
- `docs/commerce_readiness_ai_project_log.md`

## Codex Workflow

For each task:

1. Confirm the requested scope and forbidden changes.
2. Inspect the current repo state.
3. Edit only the files allowed by the task.
4. Run the required checks.
5. Verify forbidden files were not modified.
6. Commit and push only if checks pass and the task requests it.
7. Return a structured Codex Report.

For larger product or architecture changes:

- Plan first.
- Include implementation steps, risks, and acceptance criteria.
- Wait for approval before implementation.

## Testing Rules

After Python code changes, run:

```bash
python -m py_compile app.py
```

When tests exist or testable modules are touched, run:

```bash
python -m pytest
```

When the task forbids changes to specific files, run an explicit diff check, for example:

```bash
git diff --name-only -- app.py data/sample_products.csv requirements.txt src tests
```

Before committing, run:

```bash
git status --short
```

Commit and push only if checks pass. If checks fail, stop, report the failure, and do not push broken work.

## Documentation Rules

- Update `docs/commerce_readiness_ai_project_log.md` after every meaningful change.
- Update `README.md` when usage, setup, startup, export, AI Suggestions, or workflow behavior changes.
- Create new documents only when they clearly help the project.
- Keep project log entries short and structured:
  - What changed
  - Why it matters
  - How to test
  - Next recommended step

## Security Rules

- Never store API keys, tokens, or secrets.
- Keep `.env` ignored.
- Keep `.env.example` limited to placeholders.
- Do not print secrets in error messages.
- AI Suggestions are draft recommendations and require human review.

## Current Important Files

- `app.py`: main Streamlit app
- `requirements.txt`: dependencies
- `README.md`: setup and usage instructions
- `AGENTS.md`: Codex working rules for this project
- `.env.example`: environment variable template with placeholders only
- `start_app.bat`: Windows double-click launcher
- `data/sample_products.csv`: demo product data
- `src/product_data_copilot/`: import-safe modules extracted from the app
- `tests/`: pytest safety net for extracted helpers
- `docs/master_product_architecture_blueprint.md`: long-term product and architecture direction
- `docs/codebase_refactor_inventory.md`: current app inventory and safe refactor map
- `docs/testing_strategy.md`: test-first refactor strategy
- `docs/commerce_readiness_ai_project_log.md`: central project log and context
- `docs/demo_test_checklist.md`: manual demo and smoke-test checklist

## Required Codex Report

After finishing a task, return:

1. Prompt executed
2. Changed files committed
3. What was implemented
4. Tests/checks performed
5. Commit and push result
6. What was consciously not implemented
7. Risks / limitations
8. Next recommended Codex block
