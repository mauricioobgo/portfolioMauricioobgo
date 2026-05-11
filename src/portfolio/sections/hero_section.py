from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.hero import HeroPanel


def HeroSection(
    page: ft.Page, content: dict[str, Any], *, accent_control: ft.Control | None = None
) -> ft.Control:
    controls: list[ft.Control] = [ft.Container(key="hero", content=HeroPanel(page, content))]
    if accent_control is not None:
        controls.append(ft.Container(padding=ft.Padding.only(top=8), content=accent_control))
    return ft.Column(
        spacing=20,
        controls=controls,
    )
