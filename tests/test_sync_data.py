import json

from portfolio_app.scripts.sync_data import run_sync


def test_run_sync_weekly_writes_repositories_only(tmp_path) -> None:
    repos = [{"name": "demo", "html_url": "https://github.com/example/demo"}]

    refresh_log = run_sync(
        scope="weekly",
        login="mauricioobgo",
        out_dir=tmp_path,
        fetch_repositories_fn=lambda _login, _limit: repos,
        fetch_user_fn=lambda _login: {"login": _login},
    )

    assert refresh_log["scope"] == "weekly"
    assert refresh_log["updates"] == ["github_repositories_weekly"]
    assert json.loads((tmp_path / "github_repos.json").read_text(encoding="utf-8")) == repos
    assert not (tmp_path / "github_profile.json").exists()


def test_run_sync_monthly_writes_profile_only(tmp_path) -> None:
    profile = {"login": "mauricioobgo", "avatar_url": "https://example.com/avatar.png"}

    refresh_log = run_sync(
        scope="monthly",
        login="mauricioobgo",
        out_dir=tmp_path,
        fetch_repositories_fn=lambda _login, _limit: [],
        fetch_user_fn=lambda _login: profile,
    )

    assert refresh_log["scope"] == "monthly"
    assert refresh_log["updates"] == [
        "profile_monthly_review",
        "linkedin_monthly_review",
        "certifications_monthly_review",
    ]
    assert json.loads((tmp_path / "github_profile.json").read_text(encoding="utf-8")) == profile
    assert not (tmp_path / "github_repos.json").exists()
