from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import BentoGrid, SkillPill
from portfolio.interaction import attach_hover_lift
from portfolio.theme import MUTED, PRIMARY, SECONDARY, TEXT, panel


def _focus_card(item: dict[str, Any], accent: str) -> ft.Control:
    return attach_hover_lift(
        panel(
            ft.Column(
                spacing=14,
                controls=[
                    SkillPill(item.get("eyebrow", "FOCUS"), accent),
                    ft.Text(
                        item.get("name", ""),
                        color=TEXT,
                        size=22,
                        font_family="DisplayBold",
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(item.get("description", ""), color=MUTED, size=15),
                    ft.Row(
                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                        controls=[SkillPill(skill, SECONDARY) for skill in item.get("skills", [])],
                    ),
                ],
            )
        ),
        scale=1.025,
    )


def FocusGrid(items: list[dict[str, Any]]) -> ft.Control:
    accents = [PRIMARY, SECONDARY, "#A855F7", "#F59E0B"]
    return BentoGrid(
        [
            ft.Container(
                col={"xs": 12, "md": 6},
                content=_focus_card(item, accents[index % len(accents)]),
            )
            for index, item in enumerate(items)
        ]
    )


def TechnicalStackGrid(groups: list[dict[str, Any]]) -> ft.Control:
    return BentoGrid(
        [
            ft.Container(
                col={"xs": 12, "md": 6, "xl": 3},
                content=attach_hover_lift(
                    panel(
                        ft.Column(
                            spacing=14,
                            controls=[
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
                        )
                    ),
                    scale=1.02,
                ),
            )
            for group in groups
        ]
    )
