from __future__ import annotations

import asyncio
from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel
from portfolio.components.terminal import TerminalBlock
from portfolio.interaction import (
    attach_hover_lift,
    external_link_data,
    normalize_external_url,
    scroll_to,
    section_link_data,
)
from portfolio.responsive import hero_title_size, is_mobile
from portfolio.theme import MUTED, PRIMARY, PURPLE, SECONDARY, TEXT, WARNING


class SignalGrid(ft.Container):
    def __init__(self) -> None:
        self._bar_refs = [ft.Ref[ft.Container]() for _ in range(18)]
        self._patterns = [
            [14, 26, 20, 30, 18, 24, 12, 28, 22, 16, 32, 20, 26, 14, 30, 18, 24, 12],
            [24, 12, 28, 18, 30, 16, 26, 14, 32, 20, 24, 12, 28, 18, 30, 16, 22, 14],
            [18, 30, 16, 24, 12, 28, 20, 32, 18, 26, 14, 30, 16, 24, 12, 28, 20, 32],
            [28, 18, 24, 12, 26, 16, 30, 20, 22, 14, 32, 18, 24, 12, 26, 16, 30, 20],
        ]
        self._running = False
        super().__init__(content=self._build())

    def _build(self) -> ft.Control:
        rows: list[ft.Control] = []
        for row_index in range(6):
            controls: list[ft.Control] = []
            for column_index in range(3):
                ref = self._bar_refs[(row_index * 3) + column_index]
                controls.append(
                    ft.Container(
                        expand=True,
                        height=36,
                        alignment=ft.Alignment(0, 1),
                        content=ft.Container(
                            ref=ref,
                            height=20,
                            border_radius=4,
                            gradient=ft.LinearGradient(
                                begin=ft.Alignment(0, 1),
                                end=ft.Alignment(0, -1),
                                colors=[PRIMARY, PURPLE],
                            ),
                            opacity=0.84,
                            animate=ft.Animation(420, ft.AnimationCurve.EASE_IN_OUT),
                        ),
                    )
                )
            rows.append(ft.Row(spacing=8, controls=controls))
        return ft.Column(spacing=8, controls=rows)

    def did_mount(self) -> None:
        self._running = True
        if self.page:
            self.page.run_task(self._animate)

    def will_unmount(self) -> None:
        self._running = False

    async def _animate(self) -> None:
        pattern_index = 0
        while self._running:
            pattern = self._patterns[pattern_index % len(self._patterns)]
            for ref, height in zip(self._bar_refs, pattern, strict=False):
                if ref.current:
                    ref.current.height = height
            if self.parent is not None:
                self.update()
            pattern_index += 1
            await asyncio.sleep(0.62)


def HeroPanel(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    profile = content["profile"]

    ctas = [
        attach_hover_lift(
            ft.FilledButton(
                content=ft.Text("$ download_resume", font_family="Mono"),
                style=ft.ButtonStyle(
                    bgcolor=PRIMARY,
                    color="#020617",
                    padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                    shape=ft.RoundedRectangleBorder(radius=18),
                ),
                url=normalize_external_url(profile.get("resume_link")),
                data=external_link_data("Download Resume", profile.get("resume_link")),
            )
        ),
        attach_hover_lift(
            ft.OutlinedButton(
                content=ft.Text("$ open_contact", font_family="Mono"),
                style=ft.ButtonStyle(
                    color=TEXT,
                    padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                    shape=ft.RoundedRectangleBorder(radius=18),
                ),
                data=section_link_data("Open Contact", "contact"),
                on_click=lambda _: scroll_to(page, "contact"),
            )
        ),
    ]

    left = ft.Column(
        spacing=18,
        controls=[
            TerminalBlock(content.get("hero_commands", []), title="console://mauricio"),
            ft.Row(
                wrap=True,
                spacing=12,
                run_spacing=6,
                controls=[
                    ft.Text(
                        "Mauricio",
                        size=hero_title_size(page),
                        color=TEXT,
                        font_family="DisplayBold",
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(
                        "Obando",
                        size=hero_title_size(page),
                        color=PRIMARY,
                        font_family="DisplayBold",
                        weight=ft.FontWeight.W_700,
                    ),
                ],
            ),
            ft.Text(
                profile.get("title", ""),
                size=22 if is_mobile(page) else 26,
                color=PRIMARY,
                font_family="Display",
                weight=ft.FontWeight.W_600,
            ),
            ft.Text(profile.get("subtitle", ""), color=MUTED, size=17),
            ft.Row(wrap=True, spacing=12, run_spacing=12, controls=ctas),
        ],
    )

    right = ft.Column(
        spacing=14,
        controls=[
            ConsolePanel(
                ft.Column(
                    spacing=14,
                    controls=[
                        ft.Row(
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.AUTO_AWESOME, color=PRIMARY, size=18),
                                ft.Text(
                                    "AI / Cloud command center",
                                    color=PRIMARY,
                                    size=18,
                                    font_family="DisplayBold",
                                    weight=ft.FontWeight.W_700,
                                ),
                            ],
                        ),
                        ft.Text(
                            "Animated network signals, control-plane rhythm, and motion built for the hero console.",
                            color=MUTED,
                            size=14,
                        ),
                        SignalGrid(),
                    ],
                ),
                padding=ft.Padding.all(24),
                glow=True,
            ),
            ConsolePanel(
                ft.Row(
                    wrap=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("retro droid runway", color=WARNING, size=12, font_family="Mono"),
                        ft.Text(
                            "kinetic scan online",
                            color=SECONDARY,
                            size=12,
                            font_family="Mono",
                        ),
                    ],
                ),
                padding=ft.Padding.all(18),
            ),
            ConsolePanel(
                ft.Column(
                    spacing=14,
                    controls=[
                        ft.Row(
                            wrap=True,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("location", color=MUTED, size=12, font_family="Mono"),
                                ft.Text(
                                    profile.get("location", ""),
                                    color=TEXT,
                                    size=12,
                                    font_family="Mono",
                                ),
                            ],
                        ),
                        ft.Row(
                            wrap=True,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("status", color=MUTED, size=12, font_family="Mono"),
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Container(
                                            width=8,
                                            height=8,
                                            bgcolor=SECONDARY,
                                            border_radius=999,
                                        ),
                                        ft.Text(
                                            f"available / {profile.get('company', '')}",
                                            color=SECONDARY,
                                            size=12,
                                            font_family="Mono",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                padding=ft.Padding.all(18),
            ),
        ],
    )

    return ft.ResponsiveRow(
        columns=12,
        spacing=24,
        run_spacing=22,
        controls=[
            ft.Container(col={"xs": 12, "lg": 7}, content=left),
            ft.Container(col={"xs": 12, "lg": 5}, content=right),
        ],
    )
