from __future__ import annotations

import asyncio

import flet as ft

from portfolio.theme import BACKGROUND, CARD, MUTED, PANEL, PRIMARY, SECONDARY, TEXT, WARNING, alpha


class RetroDroidRunway(ft.Container):
    def __init__(self) -> None:
        self._droid_ref = ft.Ref[ft.Container]()
        self._beam_ref = ft.Ref[ft.Container]()
        self._running = False
        super().__init__(
            padding=ft.Padding.all(20),
            bgcolor=alpha(PANEL, 0.88),
            border=ft.Border.all(1, alpha(PRIMARY, 0.20)),
            border_radius=24,
            shadow=[
                ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=18,
                    color="#000000",
                    offset=ft.Offset(0, 8),
                )
            ],
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "retro droid runway", color=PRIMARY, size=12, font_family="Mono"
                            ),
                            ft.Text("motion online", color=SECONDARY, size=12, font_family="Mono"),
                        ],
                    ),
                    ft.Container(
                        height=116,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Stack(
                            expand=True,
                            controls=[
                                ft.Container(
                                    left=0,
                                    right=0,
                                    top=58,
                                    height=2,
                                    bgcolor=alpha(PRIMARY, 0.20),
                                ),
                                ft.Container(
                                    left=0,
                                    right=0,
                                    top=74,
                                    height=1,
                                    bgcolor=alpha(MUTED, 0.18),
                                ),
                                ft.Container(
                                    ref=self._beam_ref,
                                    left=64,
                                    top=20,
                                    width=120,
                                    height=74,
                                    opacity=0,
                                    offset=ft.Offset(0, 0),
                                    animate_opacity=ft.Animation(280, ft.AnimationCurve.EASE_OUT),
                                    animate_offset=ft.Animation(2200, ft.AnimationCurve.LINEAR),
                                    gradient=ft.LinearGradient(
                                        begin=ft.Alignment(-1, 0),
                                        end=ft.Alignment(1, 0),
                                        colors=[
                                            alpha(PRIMARY, 0.0),
                                            alpha(PRIMARY, 0.26),
                                            alpha(PRIMARY, 0.0),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    ref=self._droid_ref,
                                    left=12,
                                    top=18,
                                    offset=ft.Offset(-1.15, 0),
                                    rotate=-0.04,
                                    animate_offset=ft.Animation(2200, ft.AnimationCurve.LINEAR),
                                    animate_rotation=ft.Animation(
                                        350, ft.AnimationCurve.EASE_IN_OUT
                                    ),
                                    content=self._build_droid(),
                                ),
                            ],
                        ),
                    ),
                    ft.Text(
                        "Original-inspired scout droid motion keeps the hero surface feeling active without relying on browser-side JavaScript.",
                        color=MUTED,
                        size=13,
                    ),
                ],
            ),
        )

    def _build_droid(self) -> ft.Control:
        return ft.Stack(
            width=88,
            height=88,
            controls=[
                ft.Container(
                    left=22,
                    top=18,
                    width=46,
                    height=46,
                    bgcolor=SECONDARY,
                    border_radius=999,
                    shadow=[ft.BoxShadow(blur_radius=20, color=alpha(SECONDARY, 0.22))],
                ),
                ft.Container(
                    left=12,
                    top=48,
                    width=66,
                    height=24,
                    bgcolor=CARD,
                    border=ft.Border.all(1, alpha(PRIMARY, 0.24)),
                    border_radius=16,
                ),
                ft.Container(
                    left=20,
                    top=56,
                    width=14,
                    height=26,
                    bgcolor=alpha(TEXT, 0.84),
                    border_radius=999,
                ),
                ft.Container(
                    left=56,
                    top=56,
                    width=14,
                    height=26,
                    bgcolor=alpha(TEXT, 0.84),
                    border_radius=999,
                ),
                ft.Container(
                    left=38,
                    top=26,
                    width=12,
                    height=12,
                    bgcolor=BACKGROUND,
                    border_radius=999,
                ),
                ft.Container(
                    left=42,
                    top=29,
                    width=4,
                    height=4,
                    bgcolor=PRIMARY,
                    border_radius=999,
                ),
            ],
        )

    def did_mount(self) -> None:
        self._running = True
        if self.page:
            self.page.run_task(self._animate)

    def will_unmount(self) -> None:
        self._running = False

    async def _animate(self) -> None:
        while self._running and self._droid_ref.current and self._beam_ref.current:
            droid = self._droid_ref.current
            beam = self._beam_ref.current

            droid.offset = ft.Offset(-1.15, 0)
            droid.rotate = -0.04
            beam.opacity = 0
            beam.offset = ft.Offset(0, 0)
            self.update()
            await asyncio.sleep(0.2)

            droid.offset = ft.Offset(1.18, 0)
            droid.rotate = 0.05
            beam.opacity = 1
            beam.offset = ft.Offset(0.48, 0)
            self.update()
            await asyncio.sleep(2.5)

            beam.opacity = 0
            self.update()
            await asyncio.sleep(0.45)


class ConsoleSweep(ft.Container):
    def __init__(self) -> None:
        self._chomper_ref = ft.Ref[ft.Container]()
        self._mouth_ref = ft.Ref[ft.Container]()
        self._running = False
        super().__init__(
            height=42,
            padding=ft.Padding.only(bottom=4),
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                width=8, height=8, bgcolor=alpha(WARNING, 0.85), border_radius=999
                            )
                            for _ in range(10)
                        ],
                    ),
                    ft.Container(
                        ref=self._chomper_ref,
                        left=0,
                        top=4,
                        width=30,
                        height=30,
                        offset=ft.Offset(-1.1, 0),
                        animate_offset=ft.Animation(1900, ft.AnimationCurve.LINEAR),
                        content=ft.Stack(
                            width=30,
                            height=30,
                            controls=[
                                ft.Container(
                                    width=28,
                                    height=28,
                                    bgcolor=WARNING,
                                    border_radius=999,
                                ),
                                ft.Container(
                                    left=9,
                                    top=6,
                                    width=4,
                                    height=4,
                                    bgcolor=BACKGROUND,
                                    border_radius=999,
                                ),
                                ft.Container(
                                    ref=self._mouth_ref,
                                    right=-1,
                                    top=8,
                                    width=9,
                                    height=11,
                                    bgcolor=BACKGROUND,
                                    border_radius=999,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def did_mount(self) -> None:
        self._running = True
        if self.page:
            self.page.run_task(self._animate)

    def will_unmount(self) -> None:
        self._running = False

    async def _animate(self) -> None:
        mouth_sizes = [9, 4, 10, 3, 9, 4]
        while self._running and self._chomper_ref.current and self._mouth_ref.current:
            chomper = self._chomper_ref.current
            mouth = self._mouth_ref.current
            chomper.offset = ft.Offset(-1.1, 0)
            mouth.width = 9
            self.update()
            await asyncio.sleep(0.15)

            chomper.offset = ft.Offset(1.1, 0)
            for mouth_width in mouth_sizes:
                mouth.width = mouth_width
                mouth.update()
                await asyncio.sleep(0.14)

            await asyncio.sleep(0.45)
