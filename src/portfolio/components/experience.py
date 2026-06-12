from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel
from portfolio.interaction import normalize_external_url
from portfolio.theme import MUTED, PRIMARY, TEXT, WARNING, alpha


def _highlight_row(highlight: str) -> ft.Control:
    return ft.Row(
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Container(
                width=4,
                height=4,
                margin=ft.Margin.only(top=7),
                bgcolor=WARNING,
                border_radius=999,
            ),
            ft.Container(expand=True, content=ft.Text(highlight, color=MUTED, size=14)),
        ],
    )


def _experience_card(item: dict[str, Any]) -> ft.Control:
    company_name = item.get("company", "")
    company_url = normalize_external_url(item.get("company_url"))
    company_control: ft.Control
    if company_url:
        company_control = ft.TextButton(
            content=ft.Text(company_name, color=PRIMARY, size=18, font_family="Display"),
            url=company_url,
            style=ft.ButtonStyle(padding=0),
        )
    else:
        company_control = ft.Text(
            company_name,
            color=PRIMARY,
            size=18,
            font_family="Display",
        )

    return ConsolePanel(
        ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    wrap=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            wrap=True,
                            spacing=6,
                            controls=[
                                ft.Text(
                                    item.get("role", ""),
                                    color=TEXT,
                                    size=18,
                                    font_family="DisplayBold",
                                    weight=ft.FontWeight.W_700,
                                ),
                                ft.Text("/", color=TEXT, size=18),
                                company_control,
                            ],
                        ),
                        ft.Text(
                            f"{item.get('date', '')} / {item.get('location', '')}",
                            color=MUTED,
                            size=12,
                            font_family="Mono",
                        ),
                    ],
                ),
                ft.Text(item.get("description", ""), color=MUTED, size=14),
                ft.Column(
                    spacing=8,
                    controls=[
                        _highlight_row(highlight) for highlight in item.get("highlights", [])
                    ],
                ),
            ],
        ),
        padding=ft.Padding.all(22),
    )


def ExperienceTimeline(_page: ft.Page, items: list[dict[str, Any]]) -> ft.Control:
    controls: list[ft.Control] = []
    visible_items = items[:3]
    for index, item in enumerate(visible_items):
        controls.append(
            ft.Row(
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Column(
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=12,
                                height=12,
                                bgcolor=PRIMARY,
                                border_radius=999,
                                shadow=[
                                    ft.BoxShadow(
                                        blur_radius=14,
                                        color=alpha(PRIMARY, 0.26),
                                        offset=ft.Offset(0, 0),
                                    )
                                ],
                            ),
                            ft.Container(
                                width=1,
                                height=176 if index < len(visible_items) - 1 else 0,
                                bgcolor=alpha(TEXT, 0.12),
                            ),
                        ],
                    ),
                    ft.Container(expand=True, content=_experience_card(item)),
                ],
            )
        )
    return ft.Column(spacing=18, controls=controls)
