"""Ambient, non-blocking animations: scroll progress chrome and scan sweeps."""

from __future__ import annotations

import asyncio

import flet as ft

from portfolio.theme import PRIMARY, PURPLE, SECONDARY, alpha


class ScrollProgressOverlay(ft.Container):
    """Thin reading-progress bar pinned to the top edge of the viewport."""

    def __init__(self) -> None:
        self._fill_ref = ft.Ref[ft.Container]()
        self._spark_ref = ft.Ref[ft.Container]()
        self._width = 0.0
        self.progress = 0.0
        super().__init__(
            left=0,
            right=0,
            top=0,
            height=4,
            data={"kind": "scroll_progress"},
            ignore_interactions=True,
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        left=0,
                        right=0,
                        top=1,
                        height=2,
                        bgcolor=alpha(PRIMARY, 0.08),
                    ),
                    ft.Container(
                        ref=self._fill_ref,
                        left=0,
                        top=0,
                        width=0,
                        height=4,
                        border_radius=999,
                        animate=ft.Animation(160, ft.AnimationCurve.EASE_OUT),
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(-1, 0),
                            end=ft.Alignment(1, 0),
                            colors=[PRIMARY, PURPLE],
                        ),
                        shadow=[ft.BoxShadow(blur_radius=10, color=alpha(PRIMARY, 0.45))],
                    ),
                    ft.Container(
                        ref=self._spark_ref,
                        left=-12,
                        top=-2,
                        width=8,
                        height=8,
                        border_radius=999,
                        bgcolor=PRIMARY,
                        animate=ft.Animation(160, ft.AnimationCurve.EASE_OUT),
                        shadow=[ft.BoxShadow(blur_radius=14, color=alpha(PRIMARY, 0.6))],
                    ),
                ],
            ),
        )

    def sync(self, *, pixels: float, max_scroll: float, width: float, height: float) -> None:
        del height
        self._width = float(width or 0)
        self.progress = 0.0 if max_scroll <= 0 else max(0.0, min(1.0, pixels / max_scroll))
        fill_width = self._width * self.progress
        if self._fill_ref.current:
            self._fill_ref.current.width = fill_width
            if self.parent is not None:
                self._fill_ref.current.update()
        if self._spark_ref.current:
            self._spark_ref.current.left = max(fill_width - 4, -12)
            if self.parent is not None:
                self._spark_ref.current.update()


class ConsoleSweep(ft.Container):
    """A radar-style light pulse that sweeps across a thin track."""

    def __init__(self, *, auto_start: bool = True, accent: str = PRIMARY) -> None:
        self._pulse_ref = ft.Ref[ft.Container]()
        self._running = False
        self._auto_start = auto_start
        self._animating = False
        self._queued = False
        self._accent = accent
        super().__init__(
            data={"kind": "console_sweep"},
            height=16,
            padding=ft.Padding.only(bottom=4),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        left=0,
                        right=0,
                        top=5,
                        height=2,
                        border_radius=999,
                        bgcolor=alpha(accent, 0.12),
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                width=4,
                                height=4,
                                margin=ft.Margin.only(top=4),
                                border_radius=999,
                                bgcolor=alpha(accent if index % 4 else SECONDARY, 0.5),
                            )
                            for index in range(14)
                        ],
                    ),
                    ft.Container(
                        ref=self._pulse_ref,
                        top=2,
                        width=140,
                        height=8,
                        border_radius=999,
                        offset=ft.Offset(-1.4, 0),
                        animate_offset=ft.Animation(950, ft.AnimationCurve.EASE_IN_OUT),
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(-1, 0),
                            end=ft.Alignment(1, 0),
                            colors=[
                                alpha(accent, 0.0),
                                alpha(accent, 0.85),
                                alpha(accent, 0.0),
                            ],
                        ),
                        shadow=[ft.BoxShadow(blur_radius=16, color=alpha(accent, 0.3))],
                    ),
                ],
            ),
        )

    def did_mount(self) -> None:
        self._running = True
        if self.page and self._auto_start:
            self.page.run_task(self._animate)

    def will_unmount(self) -> None:
        self._running = False

    def trigger(self) -> None:
        if self._animating:
            self._queued = True
            return
        if self.page:
            self.page.run_task(self._run_once)

    async def _animate(self) -> None:
        while self._running:
            await self._run_once()
            await asyncio.sleep(1.4)

    async def _run_once(self) -> None:
        pulse = self._pulse_ref.current
        if pulse is None:
            return

        self._animating = True
        pulse.offset = ft.Offset(-1.4, 0)
        pulse.update()
        await asyncio.sleep(0.05)

        pulse.offset = ft.Offset(9.2, 0)
        pulse.update()
        await asyncio.sleep(1.0)

        self._animating = False
        if self._queued and self.page:
            self._queued = False
            self.page.run_task(self._run_once)
