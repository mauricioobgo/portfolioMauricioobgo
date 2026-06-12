from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import BentoGrid, ConsolePanel, SkillPill
from portfolio.interaction import attach_hover_lift
from portfolio.theme import MUTED, PRIMARY, PURPLE, SECONDARY, TEXT, WARNING, alpha


def _focus_card(item: dict[str, Any], accent: str) -> ft.Control:
    return attach_hover_lift(
        ConsolePanel(
            ft.Column(
                spacing=14,
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Container(width=12, height=12, bgcolor=accent, border_radius=4),
                            ft.Text(
                                item.get("eyebrow", "FOCUS"),
                                color=accent,
                                size=12,
                                font_family="Mono",
                            ),
                        ],
                    ),
                    ft.Text(
                        item.get("name", ""),
                        color=TEXT,
                        size=22,
                        font_family="DisplayBold",
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(item.get("description", ""), color=MUTED, size=15),
                    ft.Container(height=1, bgcolor=alpha(accent, 0.4)),
                ],
            ),
        ),
        scale=1.025,
    )


def FocusGrid(items: list[dict[str, Any]]) -> ft.Control:
    accents = [PRIMARY, SECONDARY, PURPLE, WARNING]
    return BentoGrid(
        [
            ft.Container(
                col={"xs": 12, "md": 4},
                content=_focus_card(item, accents[index % len(accents)]),
            )
            for index, item in enumerate(items)
        ]
    )


def TechnicalStackGrid(groups: list[dict[str, Any]]) -> ft.Control:
    return BentoGrid(
        [
            ft.Container(
                col={"xs": 12, "md": 6, "lg": 4},
                content=attach_hover_lift(
                    ConsolePanel(
                        ft.Column(
                            spacing=14,
                            controls=[
                                ft.Text(
                                    f"// {group.get('name', '').lower()}",
                                    color=PRIMARY,
                                    size=12,
                                    font_family="Mono",
                                ),
                                ft.Text(
                                    group.get("name", ""),
                                    color=TEXT,
                                    size=20,
                                    font_family="DisplayBold",
                                    weight=ft.FontWeight.W_700,
                                ),
                                ft.Row(
                                    wrap=True,
                                    spacing=10,
                                    run_spacing=10,
                                    controls=[SkillPill(item) for item in group.get("items", [])],
                                ),
                            ],
                        ),
                    ),
                    scale=1.02,
                ),
            )
            for group in groups
        ]
    )
