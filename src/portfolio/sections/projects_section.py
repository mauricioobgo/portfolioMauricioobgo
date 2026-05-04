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
                    "FEATURED PROJECTS",
                    "Technical case studies with architecture notes.",
                    "Project cards expand in place so the portfolio can show problem framing, solution details, "
                    "and architecture context without turning into a wall of text.",
                ),
                ProjectGrid(page, content.get("featured_projects", [])),
            ],
        ),
    )
