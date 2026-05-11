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
    PURPLE,
    SECONDARY,
    SECTION_WIDTH,
    TEXT,
    WARNING,
    alpha,
)


class PacmanBorderOverlay(ft.Container):
    def __init__(self) -> None:
        self._stack_ref = ft.Ref[ft.Stack]()
        self._runner_ref = ft.Ref[ft.Container]()
        self._mouth_ref = ft.Ref[ft.Container]()
        self._eye_ref = ft.Ref[ft.Container]()
        self._direction = "east"
        self._width = 0
        self._height = 0
        self._running = False
        super().__init__(
            expand=True,
            data={"kind": "border_pacman"},
            ignore_interactions=True,
            content=ft.Stack(ref=self._stack_ref, expand=True, controls=[]),
        )

    def did_mount(self) -> None:
        self._running = True
        if self.page:
            self.page.run_task(self._animate_chomp)

    def will_unmount(self) -> None:
        self._running = False

    def sync(self, *, pixels: float, max_scroll: float, width: float, height: float) -> None:
        width = int(width or 0)
        height = int(height or 0)
        if width < 768 or height < 600:
            self.visible = False
            self.update()
            return

        self.visible = True
        if width != self._width or height != self._height:
            self._width = width
            self._height = height
            self._rebuild()

        progress = 0.0 if max_scroll <= 0 else max(0.0, min(1.0, pixels / max_scroll))
        self._position_runner(progress)

    def _metrics(self) -> dict[str, float]:
        small = min(self._width, self._height)
        scale = max(0.7, min(1.3, small / 900))
        return {
            "inset": round(26 * scale),
            "radius": round(22 * scale),
            "spacing": round(38 * scale),
            "dot": 5 * scale,
            "power": 9 * scale,
            "pac": 24 * scale,
            "glow": 36 * scale,
        }

    def _rebuild(self) -> None:
        if not self._stack_ref.current:
            return
        metrics = self._metrics()
        controls: list[ft.Control] = []
        inset = metrics["inset"]

        controls.extend(
            [
                ft.Container(
                    left=inset,
                    top=inset,
                    right=inset,
                    height=1,
                    bgcolor=alpha(PRIMARY, 0.18),
                ),
                ft.Container(
                    left=inset,
                    bottom=inset,
                    right=inset,
                    height=1,
                    bgcolor=alpha(PRIMARY, 0.18),
                ),
                ft.Container(
                    left=inset,
                    top=inset,
                    bottom=inset,
                    width=1,
                    bgcolor=alpha(PRIMARY, 0.18),
                ),
                ft.Container(
                    right=inset,
                    top=inset,
                    bottom=inset,
                    width=1,
                    bgcolor=alpha(PRIMARY, 0.18),
                ),
            ]
        )

        points = self._perimeter_points(metrics)
        power_indexes = {0, len(points) // 4, len(points) // 2, (len(points) * 3) // 4}
        for index, (x, y) in enumerate(points):
            power = index in power_indexes
            size = metrics["power"] if power else metrics["dot"]
            controls.append(
                ft.Container(
                    left=x - size / 2,
                    top=y - size / 2,
                    width=size,
                    height=size,
                    border_radius=999,
                    bgcolor=alpha(WARNING, 0.9 if power else 0.72),
                    shadow=(
                        [ft.BoxShadow(blur_radius=14, color=alpha(WARNING, 0.22))]
                        if power
                        else None
                    ),
                )
            )

        controls.append(
            ft.Container(
                ref=self._runner_ref,
                width=metrics["pac"],
                height=metrics["pac"],
                animate_position=ft.Animation(260, ft.AnimationCurve.LINEAR),
                content=ft.Stack(
                    width=metrics["pac"],
                    height=metrics["pac"],
                    controls=[
                        ft.Container(
                            width=metrics["glow"],
                            height=metrics["glow"],
                            left=-(metrics["glow"] - metrics["pac"]) / 2,
                            top=-(metrics["glow"] - metrics["pac"]) / 2,
                            border_radius=999,
                            bgcolor=alpha(WARNING, 0.14),
                        ),
                        ft.Container(
                            width=metrics["pac"],
                            height=metrics["pac"],
                            bgcolor=WARNING,
                            border_radius=999,
                            shadow=[ft.BoxShadow(blur_radius=22, color=alpha(WARNING, 0.28))],
                        ),
                        ft.Container(
                            ref=self._eye_ref,
                            left=8,
                            top=6,
                            width=4,
                            height=4,
                            bgcolor=BACKGROUND,
                            border_radius=999,
                        ),
                        ft.Container(
                            ref=self._mouth_ref,
                            right=-1,
                            top=7,
                            width=10,
                            height=11,
                            bgcolor=BACKGROUND,
                            border_radius=999,
                        ),
                    ],
                ),
            )
        )
        self._stack_ref.current.controls = controls
        self._stack_ref.current.update()

    def _perimeter_points(self, metrics: dict[str, float]) -> list[tuple[float, float]]:
        inset = metrics["inset"]
        spacing = metrics["spacing"]
        width = self._width - inset * 2
        height = self._height - inset * 2
        points: list[tuple[float, float]] = []

        top_count = max(8, int(width // spacing))
        side_count = max(8, int(height // spacing))
        step_x = width / top_count
        step_y = height / side_count

        points.extend((inset + step_x * index, inset) for index in range(1, top_count))
        points.extend(
            (self._width - inset, inset + step_y * index) for index in range(1, side_count)
        )
        points.extend(
            (self._width - inset - step_x * index, self._height - inset)
            for index in range(1, top_count)
        )
        points.extend(
            (inset, self._height - inset - step_y * index) for index in range(1, side_count)
        )
        return points

    def _position_runner(self, progress: float) -> None:
        if not self._runner_ref.current:
            return
        metrics = self._metrics()
        inset = metrics["inset"]
        width = self._width - inset * 2
        height = self._height - inset * 2
        perimeter = (width * 2) + (height * 2)
        distance = perimeter * progress
        pac_half = metrics["pac"] / 2

        if distance <= width:
            x = inset + distance
            y = inset
            direction = "east"
        elif distance <= width + height:
            x = self._width - inset
            y = inset + (distance - width)
            direction = "south"
        elif distance <= (width * 2) + height:
            x = self._width - inset - (distance - width - height)
            y = self._height - inset
            direction = "west"
        else:
            x = inset
            y = self._height - inset - (distance - (width * 2) - height)
            direction = "north"

        runner = self._runner_ref.current
        runner.left = x - pac_half
        runner.top = y - pac_half
        runner.update()
        self._direction = direction
        self._apply_direction()

    def _apply_direction(self) -> None:
        mouth = self._mouth_ref.current
        eye = self._eye_ref.current
        if not mouth or not eye:
            return

        mouth.left = None
        mouth.right = None
        mouth.top = None
        mouth.bottom = None

        if self._direction == "east":
            eye.left, eye.top = 8, 6
            mouth.right, mouth.top = -1, 7
            mouth.width, mouth.height = 10, 11
        elif self._direction == "west":
            eye.left, eye.top = 12, 6
            mouth.left, mouth.top = -1, 7
            mouth.width, mouth.height = 10, 11
        elif self._direction == "south":
            eye.left, eye.top = 12, 8
            mouth.left, mouth.bottom = 7, -1
            mouth.width, mouth.height = 11, 10
        else:
            eye.left, eye.top = 12, 12
            mouth.left, mouth.top = 7, -1
            mouth.width, mouth.height = 11, 10
        eye.update()
        mouth.update()

    async def _animate_chomp(self) -> None:
        open_close = [(10, 11), (3, 4), (8, 9), (4, 5)]
        while self._running:
            mouth = self._mouth_ref.current
            if not mouth:
                await asyncio.sleep(0.1)
                continue
            for width, height in open_close:
                if not self._running or not self._mouth_ref.current:
                    return
                if self._direction in {"east", "west"}:
                    mouth.width = width
                    mouth.height = max(height, 9)
                else:
                    mouth.height = width
                    mouth.width = max(height, 9)
                mouth.update()
                await asyncio.sleep(0.12)


class RetroDroidRunway(ft.Container):
    def __init__(self) -> None:
        self._droid_ref = ft.Ref[ft.Container]()
        self._trail_ref = ft.Ref[ft.Container]()
        self._beam_ref = ft.Ref[ft.Container]()
        self._glow_ref = ft.Ref[ft.Container]()
        self._running = False
        super().__init__(
            padding=ft.Padding.all(20),
            bgcolor=alpha(PANEL, 0.9),
            border=ft.Border.all(1, alpha(PRIMARY, 0.22)),
            border_radius=24,
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "retro droid runway", color=WARNING, size=12, font_family="Mono"
                            ),
                            ft.Text(
                                "kinetic scan online", color=SECONDARY, size=12, font_family="Mono"
                            ),
                        ],
                    ),
                    ft.Container(
                        height=164,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Stack(
                            expand=True,
                            controls=[
                                ft.Container(
                                    left=0, right=0, top=88, height=2, bgcolor=alpha(PRIMARY, 0.2)
                                ),
                                ft.Container(
                                    left=0, right=0, top=116, height=1, bgcolor=alpha(MUTED, 0.18)
                                ),
                                ft.Container(
                                    ref=self._glow_ref,
                                    left=170,
                                    top=18,
                                    width=144,
                                    height=144,
                                    border_radius=999,
                                    bgcolor=alpha(PURPLE, 0.14),
                                    animate_opacity=ft.Animation(240, ft.AnimationCurve.EASE_OUT),
                                ),
                                ft.Container(
                                    ref=self._trail_ref,
                                    left=16,
                                    top=78,
                                    width=132,
                                    height=26,
                                    opacity=0.22,
                                    animate_position=ft.Animation(
                                        1350, ft.AnimationCurve.EASE_IN_OUT
                                    ),
                                    animate_opacity=ft.Animation(240, ft.AnimationCurve.EASE_OUT),
                                    gradient=ft.LinearGradient(
                                        begin=ft.Alignment(-1, 0),
                                        end=ft.Alignment(1, 0),
                                        colors=[
                                            alpha(PRIMARY, 0.0),
                                            alpha(SECONDARY, 0.66),
                                            alpha(PRIMARY, 0.0),
                                        ],
                                    ),
                                    border_radius=999,
                                ),
                                ft.Container(
                                    ref=self._beam_ref,
                                    left=104,
                                    top=16,
                                    width=192,
                                    height=112,
                                    opacity=0.2,
                                    animate_opacity=ft.Animation(240, ft.AnimationCurve.EASE_OUT),
                                    gradient=ft.LinearGradient(
                                        begin=ft.Alignment(-1, 0),
                                        end=ft.Alignment(1, 0),
                                        colors=[
                                            alpha(PRIMARY, 0.0),
                                            alpha(PRIMARY, 0.42),
                                            alpha(PRIMARY, 0.0),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    ref=self._droid_ref,
                                    left=24,
                                    top=28,
                                    animate_position=ft.Animation(
                                        1350, ft.AnimationCurve.EASE_IN_OUT
                                    ),
                                    animate_scale=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
                                    animate_rotation=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
                                    content=self._droid(),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _droid(self) -> ft.Control:
        return ft.Stack(
            width=124,
            height=112,
            controls=[
                ft.Container(
                    left=24,
                    top=6,
                    width=74,
                    height=74,
                    bgcolor=alpha(SECONDARY, 0.18),
                    border_radius=999,
                ),
                ft.Container(
                    left=32, top=16, width=60, height=60, bgcolor=SECONDARY, border_radius=999
                ),
                ft.Container(
                    left=20,
                    top=60,
                    width=84,
                    height=28,
                    bgcolor=CARD,
                    border=ft.Border.all(1, alpha(PRIMARY, 0.28)),
                    border_radius=18,
                ),
                ft.Container(
                    left=26,
                    top=88,
                    width=18,
                    height=18,
                    bgcolor=alpha(SECONDARY, 0.92),
                    border_radius=999,
                ),
                ft.Container(
                    left=80,
                    top=88,
                    width=18,
                    height=18,
                    bgcolor=alpha(PRIMARY, 0.92),
                    border_radius=999,
                ),
                ft.Container(
                    left=48, top=34, width=18, height=18, bgcolor=BACKGROUND, border_radius=999
                ),
                ft.Container(
                    left=54, top=40, width=6, height=6, bgcolor=PRIMARY, border_radius=999
                ),
                ft.Container(left=60, top=10, width=4, height=16, bgcolor=TEXT, border_radius=999),
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
            and self._trail_ref.current
            and self._beam_ref.current
            and self._glow_ref.current
        ):
            droid = self._droid_ref.current
            trail = self._trail_ref.current
            beam = self._beam_ref.current
            glow = self._glow_ref.current

            droid.left, droid.top, droid.scale, droid.rotate = 22, 28, 0.96, -0.05
            trail.left, trail.opacity = 18, 0.24
            beam.opacity = 0.18
            glow.opacity = 0.08
            self.update()
            await asyncio.sleep(0.25)

            droid.left, droid.top, droid.scale, droid.rotate = 218, 10, 1.08, 0.08
            trail.left, trail.opacity = 122, 0.88
            beam.opacity = 0.94
            glow.opacity = 0.24
            self.update()
            await asyncio.sleep(1.22)

            droid.left, droid.top, droid.scale, droid.rotate = 102, 20, 1.0, 0.0
            trail.left, trail.opacity = 78, 0.54
            beam.opacity = 0.44
            glow.opacity = 0.16
            self.update()
            await asyncio.sleep(0.96)


class ConsoleSweep(ft.Container):
    def __init__(self, *, auto_start: bool = True, accent: str = WARNING) -> None:
        self._chomper_ref = ft.Ref[ft.Container]()
        self._mouth_ref = ft.Ref[ft.Container]()
        self._running = False
        self._auto_start = auto_start
        self._animating = False
        self._queued = False
        self._accent = accent
        super().__init__(
            data={"kind": "console_sweep"},
            height=42,
            padding=ft.Padding.only(bottom=4),
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                width=8 if index % 5 else 12,
                                height=8 if index % 5 else 12,
                                bgcolor=alpha(accent, 0.86 if index % 5 else 0.96),
                                border_radius=999,
                            )
                            for index in range(12)
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
                                    shadow=[ft.BoxShadow(blur_radius=18, color=alpha(accent, 0.3))],
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

        chomper.offset = ft.Offset(1.1, 0)
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
        self._lanes = [16, 42, 68]
        self._animating = False
        self._queued_reason: str | None = None
        self._previous_keyboard_handler: Callable | None = None
        super().__init__(
            width=SECTION_WIDTH,
            padding=ft.Padding.all(18),
            bgcolor=alpha(PANEL, 0.72),
            border=ft.Border.all(1, alpha(PRIMARY, 0.18)),
            border_radius=22,
            data={"kind": "arcade_rail"},
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        wrap=True,
                        controls=[
                            ft.Text(
                                "secondary pacman rail | arrows steer | enter boosts from terminal",
                                color=MUTED,
                                size=12,
                                font_family="Mono",
                            ),
                            ft.Text(
                                "ready",
                                ref=self._status_ref,
                                color=SECONDARY,
                                size=12,
                                font_family="Mono",
                            ),
                        ],
                    ),
                    ft.Container(
                        height=104,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Stack(
                            expand=True,
                            controls=[
                                *self._lane_guides(),
                                *self._dot_field(),
                                ft.Container(
                                    ref=self._trail_ref,
                                    left=18,
                                    top=24,
                                    width=152,
                                    height=16,
                                    opacity=0.0,
                                    animate_position=ft.Animation(980, ft.AnimationCurve.LINEAR),
                                    animate_opacity=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
                                    gradient=ft.LinearGradient(
                                        begin=ft.Alignment(-1, 0),
                                        end=ft.Alignment(1, 0),
                                        colors=[
                                            alpha(PRIMARY, 0.0),
                                            alpha(PURPLE, 0.52),
                                            alpha(PRIMARY, 0.0),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    ref=self._runner_ref,
                                    left=18,
                                    top=self._lanes[self._lane_index],
                                    width=48,
                                    height=48,
                                    animate_position=ft.Animation(
                                        980, ft.AnimationCurve.EASE_IN_OUT
                                    ),
                                    animate_scale=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
                                    content=ft.Stack(
                                        width=48,
                                        height=48,
                                        controls=[
                                            ft.Container(
                                                width=42,
                                                height=42,
                                                bgcolor=WARNING,
                                                border_radius=999,
                                            ),
                                            ft.Container(
                                                left=14,
                                                top=9,
                                                width=5,
                                                height=5,
                                                bgcolor=BACKGROUND,
                                                border_radius=999,
                                            ),
                                            ft.Container(
                                                ref=self._mouth_ref,
                                                right=1,
                                                top=13,
                                                width=12,
                                                height=14,
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
                top=lane + 18,
                height=1,
                bgcolor=alpha(PRIMARY if index == 1 else MUTED, 0.2),
            )
            for index, lane in enumerate(self._lanes)
        ]

    def _dot_field(self) -> list[ft.Control]:
        controls: list[ft.Control] = []
        for lane in self._lanes:
            for dot_index in range(24):
                controls.append(
                    ft.Container(
                        left=22 + dot_index * 48,
                        top=lane + 16,
                        width=6,
                        height=6,
                        border_radius=999,
                        bgcolor=alpha(WARNING, 0.72 if dot_index % 2 == 0 else 0.42),
                    )
                )
        return controls

    def did_mount(self) -> None:
        if not self.page:
            return
        self._previous_keyboard_handler = getattr(self.page, "on_keyboard_event", None)
        self.page.on_keyboard_event = self._handle_keyboard_event
        self.width = self._rail_width()
        self.page.run_task(self._run_once, "boot")

    def will_unmount(self) -> None:
        if self.page and self.page.on_keyboard_event == self._handle_keyboard_event:
            self.page.on_keyboard_event = self._previous_keyboard_handler

    def boost(self, reason: str = "manual") -> None:
        if self._animating:
            self._queued_reason = reason
            return
        if self.page:
            self.page.run_task(self._run_once, reason)

    def sync_width(self, width: float) -> None:
        if width <= 0:
            return
        self.width = max(min(int(width) - 72, SECTION_WIDTH), 360)
        self.update()

    def _rail_width(self) -> int:
        if not self.page:
            return SECTION_WIDTH
        page_width = int(getattr(self.page, "width", 0) or 0)
        if page_width <= 0:
            return SECTION_WIDTH
        return max(min(page_width - 72, SECTION_WIDTH), 360)

    def _status_text(self, reason: str) -> str:
        direction = "vector east" if self._direction > 0 else "vector west"
        return f"{direction} | lane {self._lane_index + 1} | {reason}"

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
        runner.scale = 1.06
        trail.left = max(finish_left - 84, 0)
        trail.opacity = 0.88
        self.update()

        if self._direction < 0:
            mouth.right = None
            mouth.left = -1
        else:
            mouth.left = None
            mouth.right = 1
        mouth.update()

        for mouth_width in (12, 3, 10, 4, 12, 3, 10, 4):
            mouth.width = mouth_width
            mouth.update()
            await asyncio.sleep(0.11)

        trail.opacity = 0.0
        runner.scale = 1.0
        self.update()
        await asyncio.sleep(0.12)
        self._animating = False

        if self._queued_reason and self.page:
            queued_reason = self._queued_reason
            self._queued_reason = None
            self.page.run_task(self._run_once, queued_reason)
