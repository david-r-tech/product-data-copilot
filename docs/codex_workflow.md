# Codex Workflow - Product Data Copilot

This workflow keeps future Codex runs shorter, safer, and easier to review.

## Efficient Prompt Rules

- Reference `docs/current_context.md` instead of pasting the full project history.
- Name the exact goal block, allowed files, forbidden files, checks, and commit message.
- Keep prompts focused on one meaningful block.
- Use planning mode for high-risk runtime changes before implementation.

## What To Read

Always read:

- `docs/current_context.md`
- `AGENTS.md`
- The files directly named by the task

Read only when relevant:

- `docs/master_product_architecture_blueprint.md` for product/architecture direction
- `docs/codebase_refactor_inventory.md` for app split/refactor work
- `docs/helper_integration_v1_plan.md` for helper wiring history
- `docs/commerce_readiness_ai_project_log.md` for historical context
- `README.md` for public-facing usage/docs changes

Do not reread every long document for small helper, test, or documentation tasks.

## Goal-Mode Block Size

Good blocks:

- One helper module plus tests
- One documentation/planning pass
- One safe integration phase
- One UI polish pass with clear acceptance criteria

Too large:

- Multiple runtime features at once
- Refactor plus UI redesign plus AI behavior changes
- Integration work plus product feature changes

## Checks

Use the checks requested by the task. Defaults:

```bash
python -m pytest
git diff --check
git diff --name-only -- app.py src tests requirements.txt data/sample_products.csv
git status --short
```

Run `python -m py_compile app.py` when `app.py` changes.

## Safety Stop Rules

Stop and report without committing if:

- Forbidden files changed
- Tests fail and the fix is outside scope
- Behavior changes become necessary but were not approved
- The diff becomes too broad or unclear
- Secrets or private data appear in changed files

## Compact Report

Use:

1. Result
2. Files changed
3. What changed
4. Checks
5. Commit/push
6. Risks
7. Next
