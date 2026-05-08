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
                    "ASK MAURICIO AI",
                    "Browser CLI for the Mauricio CV copilot.",
                    "This section now feels like a command-line console instead of a static stub. The UI stays GitHub-Pages-safe while using predefined portfolio responses and leaving the full OpenAI-powered assistant in the local CLI flow.",
                ),
                AssistantExperienceGrid(content, on_enter_pacman=on_enter_pacman),
            ],
        ),
    )
