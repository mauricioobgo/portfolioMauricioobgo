from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.hero import HeroPanel
from portfolio.components.nav import NavigationBar


def HeroSection(
    page: ft.Page, content: dict[str, Any], *, accent_control: ft.Control | None = None
) -> ft.Control:
    controls: list[ft.Control] = [NavigationBar(page)]
    if accent_control is not None:
        controls.append(accent_control)
    controls.append(ft.Container(key="hero", content=HeroPanel(page, content)))
    return ft.Column(
        spacing=18,
        controls=controls,
    )
