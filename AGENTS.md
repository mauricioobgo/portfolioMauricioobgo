# AGENTS.md

## Scope
This file applies to the whole repository.

## Python runtime
- Preferred runtime: **Python 3.14**.
- Use `uv` for environment and dependency management.

## Frontend runtime
- Frontend implementation: **Flutter Web** in `frontend/`.
- Use Flutter stable for local frontend work and CI builds.

## Setup
```bash
uv python install 3.14
uv venv --python 3.14
uv sync
```

## Content build
Generate the Flutter content payload from the Python source of truth:
```bash
uv run python -m portfolio_app.scripts.build_frontend_content
```

## Run
```bash
cd frontend
flutter pub get
flutter run -d chrome --web-port 3000
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
- Keep content in `portfolio_app/data/*.yaml` and avoid hardcoding profile text in the Flutter UI.
- Keep Python service/API logic under `portfolio_app/services`.
- Keep Flutter widgets thin and data-driven; load portfolio content through `frontend/lib/services/portfolio_repository.dart`.
- Treat `frontend/assets/data/portfolio_content.json` as generated output from Python, not the authoring source.

## Refresh cadence (required)
- GitHub repositories/project showcase: **weekly** refresh.
- LinkedIn/profile details: **monthly** refresh.
- Certifications: **monthly** refresh.

Use `docs-content-refresh.md` as the operating checklist.

Cadence commands:
- Weekly GitHub repo refresh: `uv run python -m portfolio_app.scripts.sync_data --scope weekly`
- Monthly profile/linkedin/certification refresh: `uv run python -m portfolio_app.scripts.sync_data --scope monthly`
