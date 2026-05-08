from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

import httpx


GITHUB_API = "https://api.github.com"
DEFAULT_TIMEOUT = 30


def _token() -> str | None:
    return os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")


def _request(path: str, *, params: dict | None = None) -> dict | list[dict]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "portfolioMauricioobgo-sync",
    }
    if token := _token():
        headers["Authorization"] = f"Bearer {token}"
    response = httpx.get(
        f"{GITHUB_API}{path}",
        params=params,
        headers=headers,
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def fetch_user(login: str) -> dict:
    return _request(f"/users/{login}")


def fetch_repositories(login: str, limit: int = 12) -> list[dict]:
    repos = _request(
        f"/users/{login}/repos",
        params={"sort": "updated", "per_page": limit},
    )
    return [normalize_repository(repo) for repo in repos]


def normalize_repository(repo: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": repo.get("name"),
        "full_name": repo.get("full_name"),
        "html_url": repo.get("html_url"),
        "description": repo.get("description"),
        "homepage": repo.get("homepage") or None,
        "language": repo.get("language"),
        "topics": repo.get("topics", []),
        "updated_at": repo.get("updated_at"),
        "pushed_at": repo.get("pushed_at"),
        "stargazers_count": repo.get("stargazers_count", 0),
        "forks_count": repo.get("forks_count", 0),
        "open_issues_count": repo.get("open_issues_count", 0),
        "archived": repo.get("archived", False),
        "fork": repo.get("fork", False),
    }


def fetch_snapshot(
    login: str,
    *,
    limit: int = 12,
    fetch_user_fn: Callable[[str], dict[str, Any]] = fetch_user,
    fetch_repositories_fn: Callable[[str, int], list[dict[str, Any]]] = fetch_repositories,
) -> dict[str, Any]:
    return {
        "profile": fetch_user_fn(login),
        "repositories": fetch_repositories_fn(login, limit),
    }
