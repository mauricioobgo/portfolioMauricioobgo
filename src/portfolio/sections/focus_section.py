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
                    "ENGINEERING FOCUS",
                    "Backend, data, AI, and cloud capability areas.",
                    "These focus cards are shaped like a technical console instead of a static resume, "
                    "so the page reads like an engineering operating surface.",
                ),
                FocusGrid(content.get("engineering_focus", [])),
            ],
        ),
    )
