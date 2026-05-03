from __future__ import annotations

import httpx


GITHUB_API = "https://api.github.com"


def fetch_user(login: str) -> dict:
    response = httpx.get(f"{GITHUB_API}/users/{login}", timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_repositories(login: str, limit: int = 12) -> list[dict]:
    response = httpx.get(
        f"{GITHUB_API}/users/{login}/repos",
        params={"sort": "updated", "per_page": limit},
        timeout=30,
    )
    response.raise_for_status()
    repos = response.json()
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
