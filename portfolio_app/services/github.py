from __future__ import annotations

import os

import httpx


GITHUB_API = "https://api.github.com"
DEFAULT_TIMEOUT = 30


def _request(path: str, *, params: dict | None = None) -> dict | list[dict]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "portfolioMauricioobgo-sync",
    }
    if token := os.getenv("GITHUB_TOKEN"):
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
    return [
        {
            "name": repo["name"],
            "html_url": repo["html_url"],
            "description": repo.get("description"),
            "updated_at": repo["updated_at"],
            "stargazers_count": repo.get("stargazers_count", 0),
        }
        for repo in repos
    ]
