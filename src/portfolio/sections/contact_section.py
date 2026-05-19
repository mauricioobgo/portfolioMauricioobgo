from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import SectionHeader
from portfolio.components.contact import ContactGrid


def ContactSection(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return ft.Container(
        key="contact",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "CONTACT",
                    "Open a connection",
                ),
                ContactGrid(page, content),
            ],
        ),
    )
