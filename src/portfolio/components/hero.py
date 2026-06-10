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
from portfolio.theme import (
    BACKGROUND,
    BORDER,
    MUTED,
    PRIMARY,
    PURPLE,
    ROSE,
    SECONDARY,
    TEXT,
    WARNING,
    alpha,
)


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


class ArcadeMazePanel(ft.Container):
    def __init__(self, *, compact: bool = False) -> None:
        self._pac_ref = ft.Ref[ft.Container]()
        self._mouth_ref = ft.Ref[ft.Container]()
        self._ghost_refs = [ft.Ref[ft.Container]() for _ in range(3)]
        self._running = False
        self._compact = compact
        self._scale = 0.68 if compact else 1.0
        super().__init__(
            data={"kind": "hero_arcade_maze"},
            height=214 if compact else 300,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            border_radius=18,
            border=ft.Border.all(1, alpha(PRIMARY, 0.36)),
            bgcolor=alpha(BACKGROUND, 0.56),
            content=ft.Stack(expand=True, controls=self._build_controls()),
        )

    def _build_controls(self) -> list[ft.Control]:
        pac = 54 * self._scale
        return [
            *_maze_walls(self._scale),
            *_pellets(self._scale),
            self._ghost(self._ghost_refs[0], left=292, top=44, color=ROSE),
            self._ghost(self._ghost_refs[1], left=360, top=152, color=PURPLE),
            self._ghost(self._ghost_refs[2], left=238, top=204, color=SECONDARY),
            ft.Container(
                ref=self._pac_ref,
                left=24 * self._scale,
                top=42 * self._scale,
                width=pac,
                height=pac,
                animate_position=ft.Animation(620, ft.AnimationCurve.EASE_IN_OUT),
                content=ft.Stack(
                    width=pac,
                    height=pac,
                    controls=[
                        ft.Container(
                            width=pac,
                            height=pac,
                            border_radius=999,
                            bgcolor=WARNING,
                            shadow=[ft.BoxShadow(blur_radius=26, color=alpha(WARNING, 0.35))],
                        ),
                        ft.Container(
                            left=18 * self._scale,
                            top=12 * self._scale,
                            width=6 * self._scale,
                            height=6 * self._scale,
                            border_radius=999,
                            bgcolor=BACKGROUND,
                        ),
                        ft.Container(
                            ref=self._mouth_ref,
                            right=-2,
                            top=17 * self._scale,
                            width=18 * self._scale,
                            height=20 * self._scale,
                            border_radius=999,
                            bgcolor=BACKGROUND,
                        ),
                    ],
                ),
            ),
        ]

    def _ghost(self, ref: ft.Ref[ft.Container], *, left: int, top: int, color: str) -> ft.Control:
        scale = self._scale
        return ft.Container(
            ref=ref,
            left=left * scale,
            top=top * scale,
            width=42 * scale,
            height=46 * scale,
            animate_position=ft.Animation(520, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Stack(
                width=42 * scale,
                height=46 * scale,
                controls=[
                    ft.Container(
                        width=42 * scale,
                        height=42 * scale,
                        border_radius=18,
                        bgcolor=color,
                    ),
                    ft.Container(
                        left=7 * scale,
                        top=13 * scale,
                        width=8 * scale,
                        height=8 * scale,
                        border_radius=999,
                        bgcolor=TEXT,
                    ),
                    ft.Container(
                        left=25 * scale,
                        top=13 * scale,
                        width=8 * scale,
                        height=8 * scale,
                        border_radius=999,
                        bgcolor=TEXT,
                    ),
                    ft.Container(
                        left=10 * scale,
                        top=16 * scale,
                        width=4 * scale,
                        height=4 * scale,
                        border_radius=999,
                        bgcolor=BORDER,
                    ),
                    ft.Container(
                        left=28 * scale,
                        top=16 * scale,
                        width=4 * scale,
                        height=4 * scale,
                        border_radius=999,
                        bgcolor=BORDER,
                    ),
                    ft.Container(
                        left=0,
                        top=32 * scale,
                        width=14 * scale,
                        height=14 * scale,
                        bgcolor=color,
                    ),
                    ft.Container(
                        left=14 * scale,
                        top=32 * scale,
                        width=14 * scale,
                        height=14 * scale,
                        bgcolor=color,
                    ),
                    ft.Container(
                        left=28 * scale,
                        top=32 * scale,
                        width=14 * scale,
                        height=14 * scale,
                        bgcolor=color,
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
        route = [(24, 42), (190, 42), (190, 138), (420, 138), (420, 218), (78, 218)]
        ghost_offsets = [(0, 0), (-30, 18), (22, -14), (-18, -8)]
        ghost_bases = [(292, 44), (360, 152), (238, 204)]
        index = 0
        while self._running:
            if self._pac_ref.current:
                left, top = route[index % len(route)]
                self._pac_ref.current.left = left * self._scale
                self._pac_ref.current.top = top * self._scale
                self._pac_ref.current.update()
            if self._mouth_ref.current:
                self._mouth_ref.current.width = (6 if index % 2 else 18) * self._scale
                self._mouth_ref.current.update()
            for ghost_index, ref in enumerate(self._ghost_refs):
                ghost = ref.current
                if not ghost:
                    continue
                dx, dy = ghost_offsets[(index + ghost_index) % len(ghost_offsets)]
                base_x, base_y = ghost_bases[ghost_index]
                ghost.left = (base_x + dx) * self._scale
                ghost.top = (base_y + dy) * self._scale
                ghost.update()
            index += 1
            await asyncio.sleep(0.72)


def _maze_walls(scale: float) -> list[ft.Control]:
    wall_specs = [
        (18, 18, 198, 10),
        (262, 18, 220, 10),
        (18, 84, 94, 10),
        (154, 84, 214, 10),
        (414, 84, 68, 10),
        (18, 150, 176, 10),
        (246, 150, 236, 10),
        (18, 238, 462, 10),
        (18, 18, 10, 76),
        (472, 18, 10, 232),
        (112, 84, 10, 76),
        (236, 18, 10, 76),
        (196, 150, 10, 96),
        (350, 84, 10, 76),
    ]
    return [
        ft.Container(
            left=left * scale,
            top=top * scale,
            width=width * scale,
            height=height * scale,
            border_radius=6,
            bgcolor=alpha(PRIMARY, 0.78),
            shadow=[ft.BoxShadow(blur_radius=14, color=alpha(PRIMARY, 0.22))],
        )
        for left, top, width, height in wall_specs
    ]


def _pellets(scale: float) -> list[ft.Control]:
    controls: list[ft.Control] = []
    for y in (56, 120, 186, 220):
        for x in range(48, 466, 42):
            if (y == 120 and 174 <= x <= 258) or (y == 186 and 330 <= x <= 414):
                continue
            size = 10 if x in {48, 468} else 5
            controls.append(
                ft.Container(
                    left=x * scale,
                    top=y * scale,
                    width=size * scale,
                    height=size * scale,
                    border_radius=999,
                    bgcolor=WARNING,
                    shadow=[ft.BoxShadow(blur_radius=12, color=alpha(WARNING, 0.24))],
                )
            )
    return controls


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
                        color=WARNING,
                        font_family="DisplayBold",
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(
                        "Obando",
                        size=hero_title_size(page),
                        color=TEXT,
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
                    spacing=16,
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
                            "Pac-Man routes the maze while the static portfolio stays browser-safe on GitHub Pages.",
                            color=MUTED,
                            size=14,
                        ),
                        ArcadeMazePanel(compact=is_mobile(page)),
                        ft.Row(
                            wrap=True,
                            spacing=10,
                            run_spacing=10,
                            controls=[
                                ft.Container(
                                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                                    border_radius=999,
                                    bgcolor=alpha(WARNING, 0.14),
                                    content=ft.Text(
                                        "PELLETS", color=WARNING, size=11, font_family="Mono"
                                    ),
                                ),
                                ft.Container(
                                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                                    border_radius=999,
                                    bgcolor=alpha(PRIMARY, 0.12),
                                    content=ft.Text(
                                        "MAZE", color=PRIMARY, size=11, font_family="Mono"
                                    ),
                                ),
                                ft.Container(
                                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                                    border_radius=999,
                                    bgcolor=alpha(PURPLE, 0.12),
                                    content=ft.Text(
                                        "GHOSTS", color=PURPLE, size=11, font_family="Mono"
                                    ),
                                ),
                            ],
                        ),
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
                        ft.Text(
                            "arcade cabinet online", color=WARNING, size=12, font_family="Mono"
                        ),
                        ft.Text(
                            "waka loop ready",
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
