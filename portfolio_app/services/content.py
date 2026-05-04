from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


APP_DIR = Path(__file__).resolve().parents[1]


def _resolve_app_dir() -> Path:
    if (APP_DIR / "data").exists():
        return APP_DIR

    workspace_app_dir = Path.cwd() / "portfolio_app"
    if (workspace_app_dir / "data").exists():
        return workspace_app_dir

    return APP_DIR


DATA_DIR = _resolve_app_dir() / "data"
GENERATED_DIR = _resolve_app_dir() / "generated"
FRONTEND_CONTENT_PATH = APP_DIR.parent / "frontend" / "assets" / "data" / "portfolio_content.json"


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _trim_generated_profile(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "login": profile.get("login"),
        "name": profile.get("name"),
        "company": profile.get("company"),
        "location": profile.get("location"),
        "bio": profile.get("bio"),
        "avatar_url": profile.get("avatar_url"),
        "html_url": profile.get("html_url"),
        "followers": profile.get("followers"),
        "public_repos": profile.get("public_repos"),
        "updated_at": profile.get("updated_at"),
    }


def load_portfolio_content() -> dict[str, Any]:
    return {
        "profile": _load_yaml(DATA_DIR / "profile.yaml"),
        "projects": _load_yaml(DATA_DIR / "projects.yaml"),
        "experience": _load_yaml(DATA_DIR / "experience.yaml"),
        "certifications": _load_yaml(DATA_DIR / "certifications.yaml"),
        "generated_profile": _load_json(GENERATED_DIR / "profile.json") or {},
        "generated_repos": _load_json(GENERATED_DIR / "repos.json") or [],
        "refresh_log": _load_json(GENERATED_DIR / "refresh_log.json") or {},
    }


def build_frontend_content() -> dict[str, Any]:
    content = load_portfolio_content()
    generated_profile = content["generated_profile"]
    social_links = content["profile"].get("social_links", {})

    profile = {
        **content["profile"],
        "github_url": generated_profile.get("html_url") or social_links.get("github"),
        "linkedin_certifications_url": (
            "https://www.linkedin.com/in/mauricioobgo/details/certifications/"
        ),
        "avatar_url": generated_profile.get("avatar_url"),
        "location": generated_profile.get("location"),
        "company": generated_profile.get("company"),
        "bio": generated_profile.get("bio") or content["profile"].get("about"),
        "github_followers": generated_profile.get("followers", 0),
        "github_public_repos": generated_profile.get("public_repos", 0),
        "github_updated_at": generated_profile.get("updated_at"),
    }

    return {
        "metadata": {
            "generated_at": _utc_now_iso(),
            "frontend": "flutter",
            "refresh_log": content["refresh_log"],
        },
        "profile": profile,
        "experience": content["experience"],
        "projects": content["projects"],
        "certifications": content["certifications"],
        "github": {
            "profile": _trim_generated_profile(generated_profile),
            "repositories": content["generated_repos"],
        },
    }


def write_frontend_content(output_path: Path = FRONTEND_CONTENT_PATH) -> Path:
    payload = build_frontend_content()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path
