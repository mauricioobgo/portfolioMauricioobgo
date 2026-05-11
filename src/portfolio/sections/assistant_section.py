from __future__ import annotations

from collections.abc import Callable
from typing import Any

import flet as ft

from portfolio.components.assistant import AssistantExperienceGrid
from portfolio.components.cards import SectionHeader


def AssistantSection(
    page: ft.Page,
    content: dict[str, Any],
    *,
    on_enter_pacman: Callable[[str], None] | None = None,
) -> ft.Control:
    return ft.Container(
        key="assistant",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "TERMINAL",
                    "mauricio@cloud:~$",
                    "A full-width browser terminal inspired by the reference template. It keeps the public site static-safe while turning portfolio questions into CLI-style interactions with prompt prefills and arcade feedback.",
                ),
                AssistantExperienceGrid(content, on_enter_pacman=on_enter_pacman),
            ],
        ),
    )
