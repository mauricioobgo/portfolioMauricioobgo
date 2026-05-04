from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import BentoGrid, SkillPill, link_button
from portfolio.theme import MUTED, PRIMARY, PURPLE, TEXT, WARNING, alpha, panel


def ProjectCard(page: ft.Page, project: dict[str, Any]) -> ft.Control:
    links: list[ft.Control] = []
    if project.get("github_url"):
        links.append(link_button("GitHub", project["github_url"], page))
    if project.get("demo_url"):
        links.append(link_button("Demo", project["demo_url"], page, accent=PURPLE))

    architecture = project.get("architecture", "Architecture details are not available yet.")
    return ft.ExpansionTile(
        title=ft.Text(
            project.get("name", ""),
            color=TEXT,
            size=22,
            font_family="DisplayBold",
            weight=ft.FontWeight.W_700,
        ),
        subtitle=ft.Text(project.get("summary", ""), color=MUTED, size=14),
        controls_padding=ft.Padding(left=18, right=18, bottom=18),
        tile_padding=ft.Padding.all(18),
        bgcolor="#111827",
        collapsed_bgcolor="#111827",
        text_color=TEXT,
        collapsed_text_color=TEXT,
        icon_color=PRIMARY,
        collapsed_icon_color=PRIMARY,
        shape=ft.RoundedRectangleBorder(radius=22),
        collapsed_shape=ft.RoundedRectangleBorder(radius=22),
        controls=[
            ft.Column(
                spacing=14,
                controls=[
                    ft.Row(
                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                        controls=[
                            SkillPill(project.get("category", "Platform"), WARNING),
                            SkillPill(project.get("status", "Case study"), PURPLE),
                        ],
                    ),
                    ft.Text(f"Problem: {project.get('problem', '')}", color=MUTED, size=15),
                    ft.Text(f"Solution: {project.get('solution', '')}", color=MUTED, size=15),
                    ft.Text(
                        "Architecture",
                        color=PRIMARY,
                        size=13,
                        font_family="Mono",
                    ),
                    panel(
                        ft.Text(architecture, color=TEXT, size=14),
                        padding=ft.Padding.all(16),
                        bgcolor=alpha("#0F172A", 0.95),
                    ),
                    ft.Text("Highlights", color=PRIMARY, size=13, font_family="Mono"),
                    ft.Column(
                        spacing=8,
                        controls=[
                            ft.Row(
                                spacing=10,
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                controls=[
                                    ft.Text(">", color=PRIMARY, font_family="Mono"),
                                    ft.Expanded(ft.Text(highlight, color=MUTED, size=14)),
                                ],
                            )
                            for highlight in project.get("highlights", [])
                        ],
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                        controls=[
                            SkillPill(item, PRIMARY) for item in project.get("tech_stack", [])
                        ],
                    ),
                    ft.Row(wrap=True, spacing=10, controls=links),
                ],
            )
        ],
    )


def ProjectGrid(page: ft.Page, projects: list[dict[str, Any]]) -> ft.Control:
    return BentoGrid(
        [
            ft.Container(col={"xs": 12, "md": 6, "xl": 4}, content=ProjectCard(page, project))
            for project in projects
        ]
    )
