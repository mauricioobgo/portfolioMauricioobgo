from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import SectionHeader
from portfolio.components.experience import ExperienceTimeline


def ExperienceSection(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return ft.Container(
        key="experience",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "EXPERIENCE TIMELINE",
                    "Latest three roles with source-backed context.",
                    "The timeline keeps the newest three experience entries prominent and structured like an "
                    "engineering command log rather than a conventional CV block.",
                ),
                ExperienceTimeline(page, content.get("experience", [])),
            ],
        ),
    )
