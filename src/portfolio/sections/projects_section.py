from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import SectionHeader
from portfolio.components.projects import ProjectGrid


def ProjectsSection(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return ft.Container(
        key="projects",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "PROJECTS",
                    "Selected work",
                    "Production patterns from backend, data, cloud, and AI delivery with expandable architecture notes.",
                ),
                ProjectGrid(page, content.get("featured_projects", [])),
            ],
        ),
    )
