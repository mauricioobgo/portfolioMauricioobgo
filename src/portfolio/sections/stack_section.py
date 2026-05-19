from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import SectionHeader
from portfolio.components.focus import TechnicalStackGrid


def StackSection(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return ft.Container(
        key="stack",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "STACK",
                    "Tooling I reach for",
                ),
                TechnicalStackGrid(content.get("technical_stack", [])),
            ],
        ),
    )
