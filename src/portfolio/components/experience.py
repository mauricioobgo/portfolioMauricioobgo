from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import SkillPill, link_button
from portfolio.theme import MUTED, PRIMARY, SECONDARY, TEXT, alpha, panel


def _timeline_item(page: ft.Page, item: dict[str, Any], *, accent: str) -> ft.Control:
    return ft.Row(
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Column(
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=14, height=14, bgcolor=accent, border_radius=999),
                    ft.Container(width=2, height=180, bgcolor=alpha(accent, 0.35)),
                ],
            ),
            ft.Expanded(
                panel(
                    ft.Column(
                        spacing=14,
                        controls=[
                            ft.Row(
                                wrap=True,
                                spacing=10,
                                run_spacing=10,
                                controls=[
                                    SkillPill(item.get("date", ""), accent),
                                    SkillPill(item.get("location", ""), SECONDARY),
                                ],
                            ),
                            ft.Text(
                                item.get("role", ""),
                                color=TEXT,
                                size=24,
                                font_family="DisplayBold",
                                weight=ft.FontWeight.W_700,
                            ),
                            ft.Text(
                                item.get("company", ""),
                                color=PRIMARY,
                                size=18,
                                font_family="Display",
                            ),
                            ft.Text(item.get("description", ""), color=MUTED, size=15),
                            ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Row(
                                        spacing=10,
                                        vertical_alignment=ft.CrossAxisAlignment.START,
                                        controls=[
                                            ft.Text(">", color=accent, font_family="Mono"),
                                            ft.Expanded(ft.Text(highlight, color=TEXT, size=14)),
                                        ],
                                    )
                                    for highlight in item.get("highlights", [])
                                ],
                            ),
                            ft.Row(
                                wrap=True,
                                spacing=10,
                                controls=[
                                    link_button(
                                        item.get("reference_label", "Reference"),
                                        item.get("reference_url", ""),
                                        page,
                                    ),
                                    link_button(
                                        "Company",
                                        item.get("company_url", ""),
                                        page,
                                        accent=SECONDARY,
                                    ),
                                ],
                            ),
                        ],
                    )
                )
            ),
        ],
    )


def ExperienceTimeline(page: ft.Page, items: list[dict[str, Any]]) -> ft.Control:
    accents = [PRIMARY, SECONDARY, "#A855F7"]
    return ft.Column(
        spacing=0,
        controls=[
            _timeline_item(page, item, accent=accents[index % len(accents)])
            for index, item in enumerate(items[:3])
        ],
    )
