# Codex Workflow - Product Data Copilot

This workflow keeps Codex work focused, reviewable, and safe while the project evolves from a working Streamlit MVP into a more professional Product Data Copilot.

## 1. Read the Project Instructions

Before starting a task, read:

- `AGENTS.md`

For larger tasks, also read:

- `docs/master_product_architecture_blueprint.md`
- `docs/codebase_refactor_inventory.md`
- `docs/testing_strategy.md`
- `docs/product_requirements.md`
- `docs/commerce_readiness_ai_project_log.md`

## 2. Work Only on the Current Task

Stay inside the requested scope.

Do not add unrelated features, architecture, UI redesigns, integrations, database work, login, marketplace presets, or automatic AI mass updates unless the task explicitly asks for them.

## 3. Check the Repo Before Editing

Run a status check before making changes:

```bash
git status --short
```

If unexpected files are already changed, do not overwrite them. Work around them or report the situation.

## 4. Edit Only Allowed Files

Each Codex task should list allowed and forbidden files.

If a task forbids changes to files such as `app.py`, `data/sample_products.csv`, `requirements.txt`, `src/`, or `tests/`, verify those files remain unchanged before committing.

## 5. Run Checks

Use the checks requested by the task. Common checks are:

```bash
python -m py_compile app.py
python -m pytest
git diff --name-only -- app.py data/sample_products.csv requirements.txt src tests
git status --short
```

If a check fails, stop and report the failure instead of committing broken work.

## 6. Commit and Push

Only commit and push when:

- the requested work is complete
- checks pass
- forbidden files were not modified
- the task explicitly asks for commit and push

Recommended flow:

```bash
git add .
git commit -m "Short clear commit message"
git push
git status
git log --oneline -1
```

## 7. Return the Codex Report

Use the standard report format from:

- `docs/codex_report_template.md`

The report should make it clear what changed, what was tested, what was not implemented, and what should happen next.
