from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import SectionHeader
from portfolio.components.focus import FocusGrid


def FocusSection(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return ft.Container(
        key="focus",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "FOCUS",
                    "What I build",
                    "Three pillars where my delivery work compounds.",
                ),
                FocusGrid(content.get("engineering_focus", [])),
            ],
        ),
    )
