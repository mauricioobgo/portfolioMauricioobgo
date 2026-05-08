from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.assistant import AssistantExperienceGrid
from portfolio.components.cards import SectionHeader


def AssistantSection(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return ft.Container(
        key="assistant",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "ASK MAURICIO AI",
                    "Local CV copilot preparation with generated context.",
                    "This section makes the upcoming AI assistant visible without exposing an API key in a static site. The public UI stays static while the local CLI uses the generated context bundle.",
                ),
                AssistantExperienceGrid(content),
            ],
        ),
    )
