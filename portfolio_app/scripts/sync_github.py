from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Callable

from portfolio_app.services.github import fetch_repositories, fetch_user


def _get_output_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "generated"


def run_sync(
    *,
    login: str,
    limit: int = 12,
    out_dir: Path | None = None,
    fetch_user_fn: Callable[[str], dict] = fetch_user,
    fetch_repositories_fn: Callable[[str, int], list[dict]] = fetch_repositories,
) -> dict[str, Path]:
    out_dir = out_dir or _get_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    profile = fetch_user_fn(login)
    repositories = fetch_repositories_fn(login, limit)

    profile_path = out_dir / "github_profile.json"
    repos_path = out_dir / "github_repos.json"

    profile_path.write_text(json.dumps(profile, indent=2), encoding="utf-8")
    repos_path.write_text(json.dumps(repositories, indent=2), encoding="utf-8")

    return {"profile_path": profile_path, "repos_path": repos_path}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync GitHub profile and repositories for the portfolio."
    )
    parser.add_argument(
        "--login",
        default=os.getenv("GITHUB_USERNAME", "mauricioobgo"),
        help="GitHub username to fetch.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=12,
        help="How many repositories to fetch.",
    )
    args = parser.parse_args()
    run_sync(login=args.login, limit=args.limit)


if __name__ == "__main__":
    main()
