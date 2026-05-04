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
                    "TECHNICAL STACK",
                    "The toolchain behind the cloud console.",
                    "This section groups the stack by application, data, AI, and cloud execution so it reads like "
                    "an architecture inventory instead of a single flat skills list.",
                ),
                TechnicalStackGrid(content.get("technical_stack", [])),
            ],
        ),
    )
