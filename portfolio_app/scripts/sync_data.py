from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from portfolio_app.services.github import fetch_repositories, fetch_user


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _get_output_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "generated"


def run_sync(
    *,
    scope: str,
    login: str,
    out_dir: Path | None = None,
    fetch_repositories_fn: Callable[[str], list[dict]] = fetch_repositories,
    fetch_user_fn: Callable[[str], dict] = fetch_user,
) -> dict:
    out_dir = out_dir or _get_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    refresh_log = {
        "scope": scope,
        "executed_at": _utc_now_iso(),
        "updates": [],
    }

    if scope in {"weekly", "all"}:
        repos = fetch_repositories_fn(login)
        (out_dir / "repos.json").write_text(json.dumps(repos, indent=2), encoding="utf-8")
        refresh_log["updates"].append("github_repositories_weekly")

    if scope in {"monthly", "all"}:
        user = fetch_user_fn(login)
        (out_dir / "profile.json").write_text(json.dumps(user, indent=2), encoding="utf-8")
        refresh_log["updates"].extend(
            [
                "profile_monthly_review",
                "linkedin_monthly_review",
                "certifications_monthly_review",
            ]
        )

    (out_dir / "refresh_log.json").write_text(
        json.dumps(refresh_log, indent=2),
        encoding="utf-8",
    )
    return refresh_log


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync portfolio data by cadence scope.")
    parser.add_argument(
        "--scope",
        choices=["weekly", "monthly", "all"],
        default="all",
        help="weekly=GitHub repos only, monthly=profile/cert checks, all=everything",
    )
    parser.add_argument(
        "--login",
        default=os.getenv("GITHUB_USERNAME", "mauricioobgo"),
        help="GitHub login",
    )
    args = parser.parse_args()
    run_sync(scope=args.scope, login=args.login)


if __name__ == "__main__":
    main()
