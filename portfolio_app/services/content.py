from __future__ import annotations

import json
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


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


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
