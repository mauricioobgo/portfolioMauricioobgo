from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import (
    BentoGrid,
    ConsolePanel,
    LottiePanel,
    SkillPill,
    link_button,
    panel,
)
from portfolio.interaction import attach_hover_lift
from portfolio.theme import MUTED, PRIMARY, PURPLE, SECONDARY, TEXT, WARNING, alpha


FILTER_ORDER = ["All", "Backend", "Data Engineering", "LLM", "AWS", "FastAPI"]


def project_matches(project: dict[str, Any], active_filter: str) -> bool:
    if active_filter == "All":
        return True
    return active_filter in project.get("filters", [])


def ProjectCard(project: dict[str, Any]) -> ft.Control:
    links: list[ft.Control] = []
    if project.get("github_url"):
        links.append(link_button("GitHub", project["github_url"]))
    if project.get("demo_url"):
        links.append(link_button("Demo", project["demo_url"], accent=PURPLE))

    architecture = project.get("architecture", "Architecture details are not available yet.")
    tile = ft.ExpansionTile(
        title=ft.Text(
            project.get("name", ""),
            color=TEXT,
            size=22,
            font_family="DisplayBold",
            weight=ft.FontWeight.W_700,
        ),
        subtitle=ft.Text(project.get("summary", ""), color=MUTED, size=14),
        controls_padding=ft.Padding(left=18, right=18, bottom=18),
        tile_padding=ft.Padding.all(0),
        bgcolor=alpha("#111827", 0),
        collapsed_bgcolor=alpha("#111827", 0),
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
                    ft.Text("architecture", color=PRIMARY, size=12, font_family="Mono"),
                    panel(
                        ft.Text(architecture, color=TEXT, size=14),
                        padding=ft.Padding.all(16),
                        bgcolor=alpha("#0F172A", 0.95),
                    ),
                    ft.Text("highlights", color=PRIMARY, size=12, font_family="Mono"),
                    ft.Column(
                        spacing=8,
                        controls=[
                            ft.Row(
                                spacing=10,
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                controls=[
                                    ft.Text(">", color=PRIMARY, font_family="Mono"),
                                    ft.Container(
                                        expand=True,
                                        content=ft.Text(highlight, color=MUTED, size=14),
                                    ),
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
    return attach_hover_lift(
        ft.Container(
            data={"kind": "project_card", "filters": project.get("filters", [])},
            content=ConsolePanel(
                tile,
                title=(
                    f"{project.get('category', 'project').lower()} - "
                    f"{project.get('status', 'case study').lower()}"
                ),
                bgcolor="#111827",
            ),
        ),
        scale=1.01,
    )


class ProjectExplorer(ft.Column):
    def __init__(self, page: ft.Page, projects: list[dict[str, Any]]) -> None:
        self._page = page
        self.projects = projects
        self.active_filter = "All"
        self._chip_refs: dict[str, ft.Ref[ft.TextButton]] = {
            label: ft.Ref[ft.TextButton]() for label in FILTER_ORDER
        }
        self._project_refs: list[tuple[dict[str, Any], ft.Ref[ft.Container]]] = [
            (project, ft.Ref[ft.Container]()) for project in projects
        ]
        self._status_ref = ft.Ref[ft.Text]()

        super().__init__(
            spacing=18,
            controls=[
                ft.ResponsiveRow(
                    columns=12,
                    spacing=18,
                    run_spacing=18,
                    controls=[
                        ft.Container(
                            col={"xs": 12, "xl": 8},
                            content=ft.Column(
                                spacing=14,
                                controls=[
                                    ft.Row(
                                        wrap=True,
                                        spacing=10,
                                        run_spacing=10,
                                        controls=[
                                            self._filter_chip(label) for label in FILTER_ORDER
                                        ],
                                    ),
                                    ConsolePanel(
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            wrap=True,
                                            controls=[
                                                ft.Text(
                                                    "Project filter state",
                                                    color=PRIMARY,
                                                    size=12,
                                                    font_family="Mono",
                                                ),
                                                ft.Text(
                                                    self._status_text(),
                                                    ref=self._status_ref,
                                                    color=MUTED,
                                                    size=13,
                                                    font_family="Mono",
                                                ),
                                            ],
                                        ),
                                        title="filters://projects",
                                        bgcolor=alpha("#0F172A", 0.90),
                                        padding=ft.Padding.all(18),
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            col={"xs": 12, "xl": 4},
                            content=attach_hover_lift(
                                LottiePanel(
                                    "Case-study routing",
                                    "lottie/cloud_dashboard.json",
                                    caption=(
                                        "Use the project filters to pivot between backend, data, LLM, AWS, and FastAPI views."
                                    ),
                                    accent=SECONDARY,
                                    icon=ft.Icons.HUB,
                                ),
                                scale=1.01,
                            ),
                        ),
                    ],
                ),
                BentoGrid(
                    [
                        ft.Container(
                            ref=ref,
                            col={"xs": 12, "md": 6, "xl": 4},
                            visible=project_matches(project, self.active_filter),
                            content=ProjectCard(project),
                        )
                        for project, ref in self._project_refs
                    ]
                ),
            ],
        )

    def _filter_chip(self, label: str) -> ft.Control:
        active = label == self.active_filter
        return ft.TextButton(
            ref=self._chip_refs[label],
            content=ft.Text(label, color=PRIMARY if active else TEXT, size=13, font_family="Mono"),
            style=ft.ButtonStyle(
                bgcolor=alpha(PRIMARY, 0.14) if active else alpha("#0F172A", 0.88),
                side=ft.Border.all(1, alpha(PRIMARY if active else MUTED, 0.28)),
                padding=ft.Padding.symmetric(horizontal=16, vertical=14),
                shape=ft.RoundedRectangleBorder(radius=18),
            ),
            data={"kind": "project_filter", "filter": label},
            on_click=lambda _, selected=label: self.apply_filter(selected),
        )

    def _status_text(self) -> str:
        visible_count = sum(
            1 for project, _ in self._project_refs if project_matches(project, self.active_filter)
        )
        return (
            f"{self.active_filter}: showing {visible_count} of "
            f"{len(self._project_refs)} case studies"
        )

    def apply_filter(self, filter_name: str) -> None:
        self.active_filter = filter_name
        for project, ref in self._project_refs:
            if ref.current:
                ref.current.visible = project_matches(project, filter_name)
                ref.current.update()

        for label, ref in self._chip_refs.items():
            button = ref.current
            if not button:
                continue
            active = label == filter_name
            button.style = ft.ButtonStyle(
                bgcolor=alpha(PRIMARY, 0.14) if active else alpha("#0F172A", 0.88),
                side=ft.Border.all(1, alpha(PRIMARY if active else MUTED, 0.28)),
                padding=ft.Padding.symmetric(horizontal=16, vertical=14),
                shape=ft.RoundedRectangleBorder(radius=18),
            )
            button.content = ft.Text(
                label,
                color=PRIMARY if active else TEXT,
                size=13,
                font_family="Mono",
            )
            button.update()

        if self._status_ref.current:
            self._status_ref.current.value = self._status_text()
            self._status_ref.current.update()


def ProjectGrid(page: ft.Page, projects: list[dict[str, Any]]) -> ft.Control:
    return ProjectExplorer(page, projects)
