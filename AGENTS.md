# AGENTS.md

## Scope
This file applies to the whole repository.

## Python runtime
- Preferred runtime: **Python 3.14**.
- Use `uv` for environment and dependency management.

## Setup
```bash
uv python install 3.14
uv venv --python 3.14
uv sync
```

## Run
```bash
uv run reflex run
```

## Data sync
```bash
uv run python -m portfolio_app.scripts.sync_data
```

## Agent/Skill utilities (uvx)
Use `uvx` for ephemeral tools when working as an agent:

```bash
uvx --from ruff ruff check .
uvx --from ruff ruff format .
uvx --from pytest pytest -q
```

## Notes for contributors
- Keep content in `portfolio_app/data/*.yaml` and avoid hardcoding profile text in UI.
- Keep service/API logic under `portfolio_app/services`.
- Keep pages/components thin and data-driven.

## Refresh cadence (required)
- GitHub repositories/project showcase: **weekly** refresh.
- LinkedIn/profile details: **monthly** refresh.
- Certifications: **monthly** refresh.

Use `docs-content-refresh.md` as the operating checklist.


Cadence commands:
- Weekly GitHub repo refresh: `uv run python -m portfolio_app.scripts.sync_data --scope weekly`
- Monthly profile/linkedin/certification refresh: `uv run python -m portfolio_app.scripts.sync_data --scope monthly`
