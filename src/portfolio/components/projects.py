from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel, SkillPill
from portfolio.interaction import attach_hover_lift, external_link_data, normalize_external_url
from portfolio.theme import MUTED, PRIMARY, SECONDARY, TEXT, WARNING, alpha


FILTER_ORDER = ["All", "Backend", "AWS", "LLM", "Data Engineering", "FastAPI"]


def project_matches(project: dict[str, Any], active_filter: str) -> bool:
    if active_filter == "All":
        return True
    return active_filter in project.get("filters", [])


def _project_link(url: str, label: str) -> ft.Control:
    normalized = normalize_external_url(url)
    return ft.IconButton(
        icon=ft.Icons.OPEN_IN_NEW,
        icon_color=MUTED,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1, alpha(TEXT, 0.12)),
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        url=normalized,
        disabled=normalized is None,
        data=external_link_data(label, url),
        tooltip=label,
    )


def ProjectCard(project: dict[str, Any]) -> ft.Control:
    top_line = f"{project.get('category', 'Project')} / {project.get('status', 'Case study')}"
    tech_stack = project.get("tech_stack", [])[:6]
    return attach_hover_lift(
        ConsolePanel(
            ft.Column(
                spacing=14,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Container(
                                expand=True,
                                content=ft.Column(
                                    spacing=4,
                                    controls=[
                                        ft.Text(
                                            top_line,
                                            color=PRIMARY,
                                            size=10,
                                            font_family="Mono",
                                            weight=ft.FontWeight.W_700,
                                        ),
                                        ft.Text(
                                            project.get("name", ""),
                                            color=TEXT,
                                            size=20,
                                            font_family="DisplayBold",
                                            weight=ft.FontWeight.W_700,
                                        ),
                                    ],
                                ),
                            ),
                            _project_link(
                                project.get("github_url", ""),
                                f"{project.get('name', 'Project')} on GitHub",
                            )
                            if project.get("github_url")
                            else ft.Container(width=0, height=0),
                        ],
                    ),
                    ft.Text(project.get("summary", ""), color=MUTED, size=14),
                    ft.ResponsiveRow(
                        columns=12,
                        spacing=12,
                        run_spacing=12,
                        controls=[
                            ft.Container(
                                col={"xs": 12, "sm": 6},
                                content=ft.Column(
                                    spacing=4,
                                    controls=[
                                        ft.Text(
                                            "problem",
                                            color=WARNING,
                                            size=10,
                                            font_family="Mono",
                                            weight=ft.FontWeight.W_700,
                                        ),
                                        ft.Text(project.get("problem", ""), color=MUTED, size=12),
                                    ],
                                ),
                            ),
                            ft.Container(
                                col={"xs": 12, "sm": 6},
                                content=ft.Column(
                                    spacing=4,
                                    controls=[
                                        ft.Text(
                                            "solution",
                                            color=SECONDARY,
                                            size=10,
                                            font_family="Mono",
                                            weight=ft.FontWeight.W_700,
                                        ),
                                        ft.Text(project.get("solution", ""), color=MUTED, size=12),
                                    ],
                                ),
                            ),
                        ],
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=6,
                        run_spacing=6,
                        controls=[SkillPill(item, TEXT) for item in tech_stack],
                    ),
                ],
            ),
            padding=ft.Padding.all(22),
        ),
        scale=1.01,
    )


def ProjectGrid(_page: ft.Page, projects: list[dict[str, Any]]) -> ft.Control:
    return ft.ResponsiveRow(
        columns=12,
        spacing=18,
        run_spacing=18,
        controls=[
            ft.Container(
                col={"xs": 12, "md": 6},
                data={"kind": "project_card", "filters": project.get("filters", [])},
                content=ProjectCard(project),
            )
            for project in projects
        ],
    )
