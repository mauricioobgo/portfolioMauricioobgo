from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.hero import HeroPanel


def HeroSection(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return ft.Container(key="hero", content=HeroPanel(page, content))
