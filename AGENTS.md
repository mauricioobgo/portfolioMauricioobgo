# AGENTS.md

## Scope
This file applies to the whole repository.

## Python runtime
- Preferred runtime: **Python 3.14**.
- Use `uv` for environment and dependency management.

## Frontend runtime
- Frontend implementation: **Flet static web** from `src/main.py`.
- Use the official `flet build web` flow for production builds and GitHub Pages deploys.

## Setup
```bash
uv python install 3.14
uv python pin 3.14
uv sync
```

## Content build
Generate the Flet content payload from the Python source of truth:
```bash
uv run python -m portfolio_app.scripts.build_content
```

## Run
```bash
uv run flet run --web src/main.py
uv run flet serve build/web
```

## Data sync
```bash
uv run python -m portfolio_app.scripts.sync_data
uv run python -m portfolio_app.scripts.sync_github
```

## Agent/Skill utilities (uvx)
Use `uvx` for ephemeral tools when working as an agent:

```bash
uvx --from ruff ruff check .
uvx --from ruff ruff format .
uvx --from pytest pytest -q
```

## Notes for contributors
- Keep content in `portfolio_app/data/*.yaml` and avoid hardcoding profile text in the Flet UI.
- Keep Python service/API logic under `portfolio_app/services`.
- Keep the Flet controls thin and data-driven; load portfolio content through `src/assets/portfolio_content.json`.
- Treat `src/assets/portfolio_content.json` as generated output from Python, not the authoring source.

## Refresh cadence (required)
- GitHub repositories/project showcase: **weekly** refresh.
- LinkedIn/profile details: **monthly** refresh.
- Certifications: **monthly** refresh.

Use `docs-content-refresh.md` as the operating checklist.

Cadence commands:
- Weekly GitHub repo refresh: `uv run python -m portfolio_app.scripts.sync_data --scope weekly`
- Monthly profile/linkedin/certification refresh: `uv run python -m portfolio_app.scripts.sync_data --scope monthly`
