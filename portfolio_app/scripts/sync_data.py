from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from portfolio_app.services.github import fetch_repositories, fetch_user


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync portfolio data by cadence scope.")
    parser.add_argument(
        "--scope",
        choices=["weekly", "monthly", "all"],
        default="all",
        help="weekly=GitHub repos only, monthly=profile/cert checks, all=everything",
    )
    parser.add_argument("--login", default="mauricioobgo", help="GitHub login")
    args = parser.parse_args()

    out_dir = Path(__file__).resolve().parents[1] / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)

    refresh_log = {
        "scope": args.scope,
        "executed_at": _utc_now_iso(),
        "updates": [],
    }

    if args.scope in {"weekly", "all"}:
        repos = fetch_repositories(args.login)
        (out_dir / "repos.json").write_text(json.dumps(repos, indent=2), encoding="utf-8")
        refresh_log["updates"].append("github_repositories_weekly")

    if args.scope in {"monthly", "all"}:
        user = fetch_user(args.login)
        (out_dir / "profile.json").write_text(json.dumps(user, indent=2), encoding="utf-8")
        refresh_log["updates"].extend([
            "profile_monthly_review",
            "linkedin_monthly_review",
            "certifications_monthly_review",
        ])

    (out_dir / "refresh_log.json").write_text(json.dumps(refresh_log, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
