from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlsplit, urlunsplit

import flet as ft


ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
CONTENT_ASSET = "portfolio_content.json"


def _asset_url(page: ft.Page, asset_name: str) -> str:
    url = page.url or "http://localhost:8000/"
    split = urlsplit(url)
    base_path = split.path or "/"
    if not base_path.endswith("/"):
        base_path = base_path.rsplit("/", 1)[0] + "/"
    asset_path = urljoin(base_path, asset_name)
    return urlunsplit((split.scheme, split.netloc, asset_path, "", ""))


def _assets_dir() -> Path:
    return Path(os.environ.get("FLET_ASSETS_DIR", str(ASSETS_DIR))).resolve()


async def load_portfolio_content(page: ft.Page) -> dict[str, Any]:
    if sys.platform == "emscripten":
        from pyodide.http import open_url

        response = open_url(_asset_url(page, CONTENT_ASSET))
        return json.loads(response.read())

    with (_assets_dir() / CONTENT_ASSET).open(encoding="utf-8") as file_handle:
        return json.load(file_handle)
