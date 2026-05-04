import json

from portfolio_app.scripts.sync_github import run_sync
from portfolio_app.services.github import normalize_repository


def test_normalize_repository_handles_missing_optional_fields() -> None:
    repo = normalize_repository(
        {
            "name": "portfolioMauricioobgo",
            "html_url": "https://github.com/mauricioobgo/portfolioMauricioobgo",
            "updated_at": "2026-05-04T00:00:00Z",
        }
    )

    assert repo["description"] is None
    assert repo["homepage"] is None
    assert repo["language"] is None
    assert repo["topics"] == []
    assert repo["stargazers_count"] == 0


def test_sync_github_writes_profile_and_repositories(tmp_path) -> None:
    profile = {"login": "mauricioobgo"}
    repositories = [
        {
            "name": "portfolioMauricioobgo",
            "html_url": "https://github.com/mauricioobgo/portfolioMauricioobgo",
        }
    ]

    result = run_sync(
        login="mauricioobgo",
        out_dir=tmp_path,
        fetch_user_fn=lambda _login: profile,
        fetch_repositories_fn=lambda _login, _limit: repositories,
    )

    assert json.loads(result["profile_path"].read_text(encoding="utf-8")) == profile
    assert json.loads(result["repos_path"].read_text(encoding="utf-8")) == repositories
