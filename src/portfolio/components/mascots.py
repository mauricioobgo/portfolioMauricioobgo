from __future__ import annotations

import asyncio
from collections.abc import Callable

import flet as ft

from portfolio.theme import (
    BACKGROUND,
    CARD,
    MUTED,
    PANEL,
    PRIMARY,
    SECTION_WIDTH,
    SECONDARY,
    TEXT,
    WARNING,
    alpha,
)


class RetroDroidRunway(ft.Container):
    def __init__(self) -> None:
        self._droid_ref = ft.Ref[ft.Container]()
        self._beam_ref = ft.Ref[ft.Container]()
        self._trail_ref = ft.Ref[ft.Container]()
        self._pulse_ref = ft.Ref[ft.Container]()
        self._running = False
        super().__init__(
            padding=ft.Padding.all(22),
            bgcolor=alpha(PANEL, 0.9),
            border=ft.Border.all(1, alpha(PRIMARY, 0.24)),
            border_radius=24,
            shadow=[
                ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=24,
                    color="#000000",
                    offset=ft.Offset(0, 10),
                )
            ],
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "retro droid runway", color=PRIMARY, size=12, font_family="Mono"
                            ),
                            ft.Text(
                                "kinetic scan online",
                                color=SECONDARY,
                                size=12,
                                font_family="Mono",
                            ),
                        ],
                    ),
                    ft.Container(
                        height=154,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Stack(
                            expand=True,
                            controls=[
                                ft.Container(
                                    left=0,
                                    right=0,
                                    top=78,
                                    height=2,
                                    bgcolor=alpha(PRIMARY, 0.22),
                                ),
                                ft.Container(
                                    left=0,
                                    right=0,
                                    top=106,
                                    height=1,
                                    bgcolor=alpha(MUTED, 0.2),
                                ),
                                ft.Container(
                                    ref=self._pulse_ref,
                                    left=156,
                                    top=14,
                                    width=132,
                                    height=132,
                                    opacity=0.12,
                                    animate_opacity=ft.Animation(420, ft.AnimationCurve.EASE_OUT),
                                    border_radius=999,
                                    border=ft.Border.all(1, alpha(SECONDARY, 0.26)),
                                ),
                                ft.Container(
                                    ref=self._trail_ref,
                                    left=8,
                                    top=70,
                                    width=116,
                                    height=26,
                                    opacity=0.18,
                                    animate_position=ft.Animation(
                                        1500, ft.AnimationCurve.EASE_IN_OUT
                                    ),
                                    animate_opacity=ft.Animation(240, ft.AnimationCurve.EASE_OUT),
                                    gradient=ft.LinearGradient(
                                        begin=ft.Alignment(-1, 0),
                                        end=ft.Alignment(1, 0),
                                        colors=[
                                            alpha(PRIMARY, 0.0),
                                            alpha(SECONDARY, 0.55),
                                            alpha(PRIMARY, 0.0),
                                        ],
                                    ),
                                    border_radius=999,
                                ),
                                ft.Container(
                                    ref=self._beam_ref,
                                    left=108,
                                    top=20,
                                    width=170,
                                    height=94,
                                    opacity=0.24,
                                    animate_opacity=ft.Animation(240, ft.AnimationCurve.EASE_OUT),
                                    gradient=ft.LinearGradient(
                                        begin=ft.Alignment(-1, 0),
                                        end=ft.Alignment(1, 0),
                                        colors=[
                                            alpha(PRIMARY, 0.0),
                                            alpha(PRIMARY, 0.38),
                                            alpha(PRIMARY, 0.0),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    ref=self._droid_ref,
                                    left=18,
                                    top=26,
                                    scale=0.94,
                                    rotate=-0.05,
                                    animate_position=ft.Animation(
                                        1500, ft.AnimationCurve.EASE_IN_OUT
                                    ),
                                    animate_scale=ft.Animation(320, ft.AnimationCurve.EASE_IN_OUT),
                                    animate_rotation=ft.Animation(
                                        320, ft.AnimationCurve.EASE_IN_OUT
                                    ),
                                    content=self._build_droid(),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _build_droid(self) -> ft.Control:
        return ft.Stack(
            width=124,
            height=112,
            controls=[
                ft.Container(
                    left=26,
                    top=4,
                    width=72,
                    height=72,
                    bgcolor=alpha(SECONDARY, 0.26),
                    border_radius=999,
                    shadow=[ft.BoxShadow(blur_radius=26, color=alpha(SECONDARY, 0.32))],
                ),
                ft.Container(
                    left=32,
                    top=16,
                    width=60,
                    height=60,
                    bgcolor=SECONDARY,
                    border_radius=999,
                    border=ft.Border.all(1, alpha(TEXT, 0.14)),
                ),
                ft.Container(
                    left=20,
                    top=58,
                    width=84,
                    height=28,
                    bgcolor=CARD,
                    border=ft.Border.all(1, alpha(PRIMARY, 0.26)),
                    border_radius=18,
                ),
                ft.Container(
                    left=26,
                    top=88,
                    width=18,
                    height=18,
                    bgcolor=alpha(SECONDARY, 0.9),
                    border_radius=999,
                    shadow=[ft.BoxShadow(blur_radius=16, color=alpha(SECONDARY, 0.28))],
                ),
                ft.Container(
                    left=80,
                    top=88,
                    width=18,
                    height=18,
                    bgcolor=alpha(PRIMARY, 0.9),
                    border_radius=999,
                    shadow=[ft.BoxShadow(blur_radius=16, color=alpha(PRIMARY, 0.28))],
                ),
                ft.Container(
                    left=48,
                    top=32,
                    width=18,
                    height=18,
                    bgcolor=BACKGROUND,
                    border_radius=999,
                ),
                ft.Container(
                    left=54,
                    top=38,
                    width=6,
                    height=6,
                    bgcolor=PRIMARY,
                    border_radius=999,
                ),
                ft.Container(
                    left=60,
                    top=10,
                    width=4,
                    height=16,
                    bgcolor=TEXT,
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
        while (
            self._running
            and self._droid_ref.current
            and self._beam_ref.current
            and self._trail_ref.current
            and self._pulse_ref.current
        ):
            droid = self._droid_ref.current
            beam = self._beam_ref.current
            trail = self._trail_ref.current
            pulse = self._pulse_ref.current

            droid.left = 18
            droid.top = 26
            droid.scale = 0.94
            droid.rotate = -0.05
            beam.opacity = 0.18
            trail.left = 12
            trail.opacity = 0.18
            pulse.opacity = 0.12
            self.update()
            await asyncio.sleep(0.2)

            droid.left = 214
            droid.top = 8
            droid.scale = 1.1
            droid.rotate = 0.08
            beam.opacity = 0.92
            trail.left = 120
            trail.opacity = 0.88
            pulse.opacity = 0.34
            self.update()
            await asyncio.sleep(1.45)

            droid.left = 98
            droid.top = 20
            droid.scale = 1.0
            droid.rotate = 0
            beam.opacity = 0.44
            trail.left = 72
            trail.opacity = 0.58
            pulse.opacity = 0.22
            self.update()
            await asyncio.sleep(1.05)

            droid.left = 32
            droid.top = 24
            droid.scale = 0.98
            droid.rotate = -0.03
            beam.opacity = 0.22
            trail.left = 20
            trail.opacity = 0.28
            pulse.opacity = 0.14
            self.update()
            await asyncio.sleep(0.8)


class ConsoleSweep(ft.Container):
    def __init__(self, *, auto_start: bool = True, accent: str = WARNING) -> None:
        self._chomper_ref = ft.Ref[ft.Container]()
        self._mouth_ref = ft.Ref[ft.Container]()
        self._running = False
        self._auto_start = auto_start
        self._animating = False
        self._queued = False
        super().__init__(
            height=46,
            padding=ft.Padding.only(bottom=4),
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                width=9,
                                height=9,
                                bgcolor=alpha(accent, 0.85),
                                border_radius=999,
                            )
                            for _ in range(14)
                        ],
                    ),
                    ft.Container(
                        ref=self._chomper_ref,
                        left=0,
                        top=2,
                        width=34,
                        height=34,
                        offset=ft.Offset(-1.08, 0),
                        animate_offset=ft.Animation(980, ft.AnimationCurve.LINEAR),
                        content=ft.Stack(
                            width=34,
                            height=34,
                            controls=[
                                ft.Container(
                                    width=32,
                                    height=32,
                                    bgcolor=accent,
                                    border_radius=999,
                                    shadow=[
                                        ft.BoxShadow(blur_radius=18, color=alpha(accent, 0.28))
                                    ],
                                ),
                                ft.Container(
                                    left=10,
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
                                    width=11,
                                    height=12,
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
            await asyncio.sleep(0.55)

    async def _run_once(self) -> None:
        if not self._chomper_ref.current or not self._mouth_ref.current:
            return

        self._animating = True
        chomper = self._chomper_ref.current
        mouth = self._mouth_ref.current
        chomper.offset = ft.Offset(-1.08, 0)
        mouth.width = 11
        self.update()
        await asyncio.sleep(0.05)

        chomper.offset = ft.Offset(1.12, 0)
        chomper.update()
        for mouth_width in (11, 3, 10, 4, 11, 3, 10, 4):
            mouth.width = mouth_width
            mouth.update()
            await asyncio.sleep(0.11)

        await asyncio.sleep(0.16)
        self._animating = False
        if self._queued and self.page:
            self._queued = False
            self.page.run_task(self._run_once)


class ArcadeCommandRail(ft.Container):
    def __init__(self) -> None:
        self._runner_ref = ft.Ref[ft.Container]()
        self._mouth_ref = ft.Ref[ft.Container]()
        self._trail_ref = ft.Ref[ft.Container]()
        self._status_ref = ft.Ref[ft.Text]()
        self._direction = 1
        self._lane_index = 1
        self._lanes = [16, 48, 80]
        self._animating = False
        self._queued_reason: str | None = None
        self._previous_keyboard_handler: Callable | None = None
        self._previous_resize_handler: Callable | None = None
        super().__init__(
            width=SECTION_WIDTH,
            padding=ft.Padding.all(22),
            bgcolor=alpha(PANEL, 0.82),
            border=ft.Border.all(1, alpha(PRIMARY, 0.2)),
            border_radius=24,
            shadow=[
                ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=18,
                    color="#000000",
                    offset=ft.Offset(0, 8),
                )
            ],
            data={"kind": "arcade_rail"},
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        wrap=True,
                        controls=[
                            ft.Row(
                                spacing=10,
                                controls=[
                                    ft.Text(
                                        "pacman border rail",
                                        color=PRIMARY,
                                        size=12,
                                        font_family="Mono",
                                    ),
                                    ft.Text(
                                        "arrow-left/right = vector",
                                        color=MUTED,
                                        size=12,
                                        font_family="Mono",
                                    ),
                                    ft.Text(
                                        "arrow-up/down = lane shift",
                                        color=MUTED,
                                        size=12,
                                        font_family="Mono",
                                    ),
                                ],
                            ),
                            ft.Text(
                                "pacman boost ready",
                                ref=self._status_ref,
                                color=SECONDARY,
                                size=12,
                                font_family="Mono",
                            ),
                        ],
                    ),
                    ft.Container(
                        height=124,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Stack(
                            expand=True,
                            controls=[
                                *self._lane_guides(),
                                *self._dot_field(),
                                ft.Container(
                                    ref=self._trail_ref,
                                    left=18,
                                    top=26,
                                    width=148,
                                    height=18,
                                    opacity=0.0,
                                    animate_position=ft.Animation(1180, ft.AnimationCurve.LINEAR),
                                    animate_opacity=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
                                    gradient=ft.LinearGradient(
                                        begin=ft.Alignment(-1, 0),
                                        end=ft.Alignment(1, 0),
                                        colors=[
                                            alpha(PRIMARY, 0.0),
                                            alpha(WARNING, 0.55),
                                            alpha(PRIMARY, 0.0),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    ref=self._runner_ref,
                                    left=18,
                                    top=self._lanes[self._lane_index],
                                    width=54,
                                    height=54,
                                    animate_position=ft.Animation(
                                        1180, ft.AnimationCurve.EASE_IN_OUT
                                    ),
                                    animate_scale=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
                                    content=ft.Stack(
                                        width=54,
                                        height=54,
                                        controls=[
                                            ft.Container(
                                                width=48,
                                                height=48,
                                                bgcolor=WARNING,
                                                border_radius=999,
                                                shadow=[
                                                    ft.BoxShadow(
                                                        blur_radius=24,
                                                        color=alpha(WARNING, 0.32),
                                                    )
                                                ],
                                            ),
                                            ft.Container(
                                                left=16,
                                                top=10,
                                                width=6,
                                                height=6,
                                                bgcolor=BACKGROUND,
                                                border_radius=999,
                                            ),
                                            ft.Container(
                                                ref=self._mouth_ref,
                                                right=2,
                                                top=15,
                                                width=15,
                                                height=18,
                                                bgcolor=BACKGROUND,
                                                border_radius=999,
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _lane_guides(self) -> list[ft.Control]:
        return [
            ft.Container(
                left=0,
                right=0,
                top=lane + 22,
                height=1,
                bgcolor=alpha(PRIMARY if index == 1 else MUTED, 0.24),
            )
            for index, lane in enumerate(self._lanes)
        ]

    def _dot_field(self) -> list[ft.Control]:
        controls: list[ft.Control] = []
        for lane in self._lanes:
            for dot_index in range(28):
                controls.append(
                    ft.Container(
                        left=24 + dot_index * 42,
                        top=lane + 20,
                        width=6,
                        height=6,
                        border_radius=999,
                        bgcolor=alpha(WARNING, 0.78 if dot_index % 2 == 0 else 0.46),
                    )
                )
        return controls

    def did_mount(self) -> None:
        if not self.page:
            return
        self._previous_keyboard_handler = getattr(self.page, "on_keyboard_event", None)
        self._previous_resize_handler = getattr(self.page, "on_resize", None)
        self.page.on_keyboard_event = self._handle_keyboard_event
        self.page.on_resize = self._handle_resize
        self.width = self._rail_width()
        self.page.run_task(self._run_once, "boot")

    def will_unmount(self) -> None:
        if not self.page:
            return
        if self.page.on_keyboard_event == self._handle_keyboard_event:
            self.page.on_keyboard_event = self._previous_keyboard_handler
        if self.page.on_resize == self._handle_resize:
            self.page.on_resize = self._previous_resize_handler

    def boost(self, reason: str = "manual") -> None:
        if self._animating:
            self._queued_reason = reason
            return
        if self.page:
            self.page.run_task(self._run_once, reason)

    def _rail_width(self) -> int:
        if not self.page:
            return SECTION_WIDTH
        page_width = int(getattr(self.page, "width", 0) or 0)
        if page_width <= 0:
            return SECTION_WIDTH
        return max(min(page_width - 72, SECTION_WIDTH), 360)

    def _status_text(self, reason: str) -> str:
        direction = "vector east" if self._direction > 0 else "vector west"
        lane = self._lane_index + 1
        return f"{direction} | lane {lane} | trigger={reason}"

    def _handle_resize(self, _: ft.ControlEvent) -> None:
        self.width = self._rail_width()
        if self._status_ref.current:
            self._status_ref.current.value = self._status_text("resize")
            self._status_ref.current.update()
        self.update()

    def _handle_keyboard_event(self, event: ft.KeyboardEvent) -> None:
        key = (event.key or "").lower()
        if key in {"arrow left", "left"}:
            self._direction = -1
            self.boost("arrow-left")
        elif key in {"arrow right", "right"}:
            self._direction = 1
            self.boost("arrow-right")
        elif key in {"arrow up", "up"}:
            self._lane_index = max(0, self._lane_index - 1)
            self.boost("arrow-up")
        elif key in {"arrow down", "down"}:
            self._lane_index = min(len(self._lanes) - 1, self._lane_index + 1)
            self.boost("arrow-down")

    async def _run_once(self, reason: str) -> None:
        if (
            not self._runner_ref.current
            or not self._mouth_ref.current
            or not self._trail_ref.current
        ):
            return
        self._animating = True
        width = self._rail_width()
        end_left = max(width - 80, 18)
        start_left = 18 if self._direction > 0 else end_left
        finish_left = end_left if self._direction > 0 else 18
        lane_top = self._lanes[self._lane_index]

        runner = self._runner_ref.current
        mouth = self._mouth_ref.current
        trail = self._trail_ref.current

        self.width = width
        runner.left = start_left
        runner.top = lane_top
        runner.scale = 0.98
        trail.left = max(start_left - 72, 0)
        trail.top = lane_top + 16
        trail.opacity = 0.0
        if self._status_ref.current:
            self._status_ref.current.value = self._status_text(reason)
            self._status_ref.current.update()
        self.update()
        await asyncio.sleep(0.06)

        runner.left = finish_left
        runner.top = lane_top
        runner.scale = 1.08
        trail.left = max(finish_left - 84, 0)
        trail.top = lane_top + 16
        trail.opacity = 0.92
        self.update()

        if self._direction < 0:
            mouth.right = None
            mouth.left = -1
        else:
            mouth.left = None
            mouth.right = 2
        mouth.update()

        for mouth_width in (15, 4, 13, 5, 15, 4, 13, 5, 15):
            mouth.width = mouth_width
            mouth.update()
            await asyncio.sleep(0.12)

        trail.opacity = 0.0
        runner.scale = 1.0
        self.update()
        await asyncio.sleep(0.18)
        self._animating = False

        if self._queued_reason and self.page:
            queued_reason = self._queued_reason
            self._queued_reason = None
            self.page.run_task(self._run_once, queued_reason)
