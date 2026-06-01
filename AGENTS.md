# AGENTS.md - Commerce Readiness AI

## Strategic Context

Commerce Readiness AI is a Streamlit MVP for e-commerce product data audits.

The current goal is not release or deployment. The current goal is fast, structured expansion into a useful enterprise demo tool for real e-commerce teams.

Primary users:

- Product Data Managers
- Marketplace Managers
- E-Commerce Operations teams
- Category teams

Core value:

- Check product data quality
- Evaluate product readiness
- Prioritize problems
- Generate review tasks
- Support human-reviewed AI suggestions
- Provide useful exports for business workflows

## Development Mode

- Prefer larger, meaningful product increments over tiny cosmetic edits.
- Make small changes only when they have a clear purpose or fix a clear issue.
- For larger changes, create a plan first, then implement after approval.
- Preserve existing working functionality.
- Avoid unnecessary refactoring.
- Do not over-engineer.
- Do not add enterprise architecture unless explicitly requested.
- Keep code readable and beginner-friendly.
- Add comments only where they help a beginner understand non-obvious logic.

## Current Product Priorities

Current priority order:

1. Stable local MVP
2. Useful demo workflow for real product data
3. Excel management export as a real work artifact
4. Better rule catalog / Rule Engine v2
5. AI Suggestions v2 with storage/export integration
6. Review Workflow v2
7. UI/UX polish for usability
8. Portfolio documentation later, not the current focus

## Scope Control

Do not add these without explicit instruction:

- Release/deployment
- SaaS billing
- Login or multi-user features
- Shopware API
- Plentymarkets API
- Shopify App
- Database migration
- Large framework refactoring
- Automatic mass generation of AI text
- Automatic application of AI suggestions to product data
- Real legal advice or compliance guarantees

## Codex Workflow

After every task, summarize:

1. What changed
2. Which files changed
3. Tests performed
4. Whether README was updated
5. Whether the project log was updated
6. Risks or notes

For larger tasks:

- Use Plan Mode first.
- Provide implementation steps, risks, and acceptance criteria.
- Wait for approval before implementation.

## Documentation Rules

- Update `docs/commerce_readiness_ai_project_log.md` after every meaningful change.
- Update `README.md` when usage, setup, startup, export, AI Suggestions, or workflow behavior changes.
- Create new documents only when they clearly help the project.
- Keep project log entries short and structured:
  - What changed
  - Why it matters
  - How to test
  - Next recommended step

## Testing Rules

After Python code changes, run:

```bash
python -m py_compile app.py
```

After export changes:

- Check whether the export file can be produced.
- Check whether expected sheets or columns are present.

After UI changes:

- Provide manual test steps.

After requirements changes:

- Check `requirements.txt`.

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
- `docs/commerce_readiness_ai_project_log.md`: central project log and context
- `docs/demo_test_checklist.md`: manual demo and smoke-test checklist
