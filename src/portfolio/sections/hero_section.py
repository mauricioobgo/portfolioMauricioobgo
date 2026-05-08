from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.hero import HeroPanel
from portfolio.components.nav import NavigationBar


def HeroSection(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return ft.Column(
        spacing=18,
        controls=[
            NavigationBar(page),
            ft.Container(key="hero", content=HeroPanel(page, content)),
        ],
    )
