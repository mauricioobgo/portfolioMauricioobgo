# portfolioMauricioobgo

Portfolio repository for Mauricio Obando.

## Current architecture
- Legacy React portfolio remains in `src/`.
- New Python/Reflex migration lives in `portfolio_app/`.
- Profile and section content is data-driven via YAML in `portfolio_app/data/`.

## Python 3.14 + uv workflow
```bash
uv python install 3.14
uv venv --python 3.14
uv sync
uv run reflex run
```

## Agent-oriented uvx skills/tooling
For quick ephemeral quality checks without installing global packages:
```bash
uvx --from ruff ruff check .
uvx --from ruff ruff format .
uvx --from pytest pytest -q
```

See `AGENTS.md` for contributor and agent conventions.

## Data update cadence
- GitHub repositories/projects: weekly
- LinkedIn/profile information: monthly
- Certifications: monthly

Detailed checklist: `docs-content-refresh.md`.


Automated cadence is implemented in CI with scoped sync runs:
- Weekly: `uv run python -m portfolio_app.scripts.sync_data --scope weekly`
- Monthly: `uv run python -m portfolio_app.scripts.sync_data --scope monthly`
- Manual/push: `uv run python -m portfolio_app.scripts.sync_data --scope all`
