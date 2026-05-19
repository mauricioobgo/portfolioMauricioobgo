from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import SectionHeader
from portfolio.components.github_feed import GitHubGrid


def GitHubSection(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return ft.Container(
        key="github",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "GITHUB",
                    "Open work",
                    "Selected repositories on GitHub.",
                ),
                GitHubGrid(page, content.get("github", {})),
            ],
        ),
    )
