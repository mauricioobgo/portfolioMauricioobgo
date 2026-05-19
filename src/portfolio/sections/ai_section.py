from __future__ import annotations

from collections.abc import Callable
from typing import Any

import flet as ft

from portfolio.components.assistant import AICommandDeck
from portfolio.components.cards import SectionHeader


def AISection(
    page: ft.Page,
    content: dict[str, Any],
    *,
    on_prompt: Callable[[str], None],
) -> ft.Control:
    return ft.Container(
        key="ai",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "AI",
                    "Talk to MauricioOS",
                    "Click any prompt to send it to the terminal above.",
                ),
                AICommandDeck(page, content, on_prompt=on_prompt),
            ],
        ),
    )
