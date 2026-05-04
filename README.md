# portfolioMauricioobgo

Python-first portfolio repository for Mauricio Obando, built with Reflex and
deployed to GitHub Pages from the `gh-pages` branch.

## Architecture
- The Reflex application lives in `portfolio_app/`.
- Curated content is stored in YAML under `portfolio_app/data/`.
- Scheduled refreshes write generated GitHub data to `portfolio_app/generated/`
  right before each deploy.
- Static web assets live in `assets/`.

## Python 3.14 + uv workflow
```bash
uv python install 3.14
uv venv --python 3.14
uv sync
uv run reflex run
```

## Quality commands
Use `uvx` for ephemeral tooling without installing global packages:
```bash
uvx --from ruff ruff check .
uvx --from ruff ruff format --check .
uvx --with . --from pytest python -m pytest -q
```

See `AGENTS.md` for contributor and agent conventions.

## Data update cadence
- GitHub repositories/projects: weekly
- LinkedIn/profile information: monthly
- Certifications: monthly

Detailed checklist: `docs-content-refresh.md`.


Automated cadence is implemented in GitHub Actions with scoped sync runs:
- Weekly: `uv run python -m portfolio_app.scripts.sync_data --scope weekly`
- Monthly: `uv run python -m portfolio_app.scripts.sync_data --scope monthly`
- Manual/push: `uv run python -m portfolio_app.scripts.sync_data --scope all`

## GitHub Pages deployment
- Pull requests to `main` run `ci.yml` for lint, tests, and Reflex export validation.
- Pushes to `main` run `deploy-gh-pages.yml`, which syncs data, exports the
  Reflex frontend, and publishes `.web/build/client` to `gh-pages`.
- Scheduled refreshes run through `refresh-gh-pages.yml` and redeploy the same
  `gh-pages` branch after running the weekly or monthly sync scope.
- The GitHub Pages repository setting should be `Deploy from a branch`,
  targeting `gh-pages` and `/ (root)`.
