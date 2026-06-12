from __future__ import annotations

import asyncio
from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel, SkillPill
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
    MUTED,
    PRIMARY,
    PURPLE,
    SECONDARY,
    TEXT,
    WARNING,
    alpha,
    gradient_text,
)


class RoleTyper(ft.Container):
    """Types and erases rotating role names with a blinking caret."""

    def __init__(self, roles: list[str], *, size: int = 22) -> None:
        self._roles = [role for role in roles if role] or ["Software Engineer"]
        self._text_ref = ft.Ref[ft.Text]()
        self._caret_ref = ft.Ref[ft.Container]()
        self._running = False
        super().__init__(
            data={"kind": "role_typer"},
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(">", color=SECONDARY, size=size, font_family="Mono"),
                    ft.Text(
                        self._roles[0],
                        ref=self._text_ref,
                        color=PRIMARY,
                        size=size,
                        font_family="Mono",
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Container(
                        ref=self._caret_ref,
                        width=11,
                        height=size + 4,
                        bgcolor=PRIMARY,
                        border_radius=2,
                        animate_opacity=ft.Animation(240, ft.AnimationCurve.EASE_OUT),
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

    def _set_value(self, value: str) -> None:
        text = self._text_ref.current
        if text is not None:
            text.value = value
            text.update()

    async def _animate(self) -> None:
        index = 0
        while self._running and self._text_ref.current:
            role = self._roles[index % len(self._roles)]
            for cursor in range(1, len(role) + 1):
                if not self._running:
                    return
                self._set_value(role[:cursor])
                await asyncio.sleep(0.045)

            for _ in range(3):
                if not self._running:
                    return
                caret = self._caret_ref.current
                if caret is not None:
                    caret.opacity = 0.1
                    caret.update()
                    await asyncio.sleep(0.4)
                    caret.opacity = 1
                    caret.update()
                await asyncio.sleep(0.4)

            for cursor in range(len(role), 0, -1):
                if not self._running:
                    return
                self._set_value(role[: cursor - 1])
                await asyncio.sleep(0.022)
            index += 1


class MetricCounter(ft.Container):
    """A stat card that counts up to its value when it enters the page."""

    def __init__(self, value: int, label: str, caption: str, accent: str = PRIMARY) -> None:
        self._target = max(int(value), 0)
        self._value_ref = ft.Ref[ft.Text]()
        super().__init__(
            data={"kind": "hero_metric", "value": self._target},
            content=ConsolePanel(
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(
                            label.upper(),
                            color=accent,
                            size=11,
                            font_family="Mono",
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "0",
                            ref=self._value_ref,
                            color=TEXT,
                            size=34,
                            font_family="DisplayBold",
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(caption, color=MUTED, size=12),
                    ],
                ),
                padding=ft.Padding.all(18),
            ),
        )

    def did_mount(self) -> None:
        if self.page:
            self.page.run_task(self._count_up)

    async def _count_up(self) -> None:
        steps = 26
        for step in range(1, steps + 1):
            value_text = self._value_ref.current
            if value_text is None:
                return
            progress = 1 - (1 - step / steps) ** 3
            value_text.value = str(round(self._target * progress))
            value_text.update()
            await asyncio.sleep(0.035)


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
                            opacity=0.8,
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


class PulsingDot(ft.Container):
    def __init__(self, color: str = SECONDARY) -> None:
        self._running = False
        super().__init__(
            width=9,
            height=9,
            bgcolor=color,
            border_radius=999,
            animate_opacity=ft.Animation(620, ft.AnimationCurve.EASE_IN_OUT),
            shadow=[ft.BoxShadow(blur_radius=10, color=alpha(color, 0.55))],
        )

    def did_mount(self) -> None:
        self._running = True
        if self.page:
            self.page.run_task(self._pulse)

    def will_unmount(self) -> None:
        self._running = False

    async def _pulse(self) -> None:
        while self._running:
            self.opacity = 0.35
            if self.parent is not None:
                self.update()
            await asyncio.sleep(0.7)
            self.opacity = 1
            if self.parent is not None:
                self.update()
            await asyncio.sleep(0.7)


def _status_chip(profile: dict[str, Any]) -> ft.Control:
    location = profile.get("location", "")
    company = profile.get("company", "")
    label = " · ".join(part for part in (company, location) if part)
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=14, vertical=8),
        border_radius=999,
        bgcolor=alpha(SECONDARY, 0.08),
        border=ft.Border.all(1, alpha(SECONDARY, 0.3)),
        content=ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                PulsingDot(SECONDARY),
                ft.Text(
                    f"shipping in production · {label}" if label else "shipping in production",
                    color=SECONDARY,
                    size=12,
                    font_family="Mono",
                ),
            ],
        ),
    )


def _cta_row(page: ft.Page, profile: dict[str, Any]) -> ft.Control:
    social_links = profile.get("social_links", {})
    linkedin_url = social_links.get("linkedin", "")
    github_url = profile.get("github_url") or social_links.get("github", "")

    def outlined(label: str, icon: ft.IconData, url: str) -> ft.Control:
        return attach_hover_lift(
            ft.OutlinedButton(
                content=ft.Row(
                    spacing=8,
                    controls=[
                        ft.Icon(icon, size=16, color=PRIMARY),
                        ft.Text(label, font_family="Mono", color=TEXT, size=13),
                    ],
                ),
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, alpha(PRIMARY, 0.4)),
                    padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                    shape=ft.RoundedRectangleBorder(radius=14),
                ),
                url=normalize_external_url(url),
                data=external_link_data(label, url),
            )
        )

    return ft.Row(
        wrap=True,
        spacing=12,
        run_spacing=12,
        controls=[
            attach_hover_lift(
                ft.FilledButton(
                    content=ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.DOWNLOAD, size=16, color="#04070F"),
                            ft.Text(
                                "Download Resume",
                                font_family="Mono",
                                size=13,
                                weight=ft.FontWeight.W_700,
                            ),
                        ],
                    ),
                    style=ft.ButtonStyle(
                        bgcolor=PRIMARY,
                        color="#04070F",
                        padding=ft.Padding.symmetric(horizontal=20, vertical=16),
                        shape=ft.RoundedRectangleBorder(radius=14),
                    ),
                    url=normalize_external_url(profile.get("resume_link")),
                    data=external_link_data("Download Resume", profile.get("resume_link")),
                )
            ),
            outlined("LinkedIn", ft.Icons.WORK_OUTLINE, linkedin_url),
            outlined("GitHub", ft.Icons.CODE, github_url),
            attach_hover_lift(
                ft.TextButton(
                    content=ft.Row(
                        spacing=6,
                        controls=[
                            ft.Text("contact", font_family="Mono", color=MUTED, size=13),
                            ft.Icon(ft.Icons.ARROW_DOWNWARD, size=14, color=MUTED),
                        ],
                    ),
                    style=ft.ButtonStyle(padding=ft.Padding.symmetric(horizontal=14, vertical=16)),
                    data=section_link_data("Open Contact", "contact"),
                    on_click=lambda _: scroll_to(page, "contact"),
                )
            ),
        ],
    )


def _metrics_row(content: dict[str, Any]) -> ft.Control:
    certifications = content.get("certifications", [])
    featured_certs = [cert for cert in certifications if cert.get("featured")]
    projects = content.get("featured_projects", [])
    repo_count = content.get("github", {}).get("summary", {}).get("repo_count", 0)
    focus_areas = content.get("engineering_focus", [])

    metrics = [
        MetricCounter(
            len(certifications),
            "credentials",
            f"{len(featured_certs)} featured AWS certifications",
            WARNING,
        ),
        MetricCounter(
            len(projects),
            "case studies",
            "production-grade featured projects",
            PRIMARY,
        ),
        MetricCounter(
            repo_count,
            "public repos",
            "open work on GitHub",
            SECONDARY,
        ),
        MetricCounter(
            len(focus_areas),
            "focus areas",
            "backend · data · cloud · AI",
            PURPLE,
        ),
    ]
    return ft.ResponsiveRow(
        columns=12,
        spacing=16,
        run_spacing=16,
        data={"kind": "hero_metrics"},
        controls=[ft.Container(col={"xs": 6, "lg": 3}, content=metric) for metric in metrics],
    )


def HeroPanel(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    profile = content["profile"]
    roles = [item.get("name", "") for item in content.get("engineering_focus", [])]
    title_size = hero_title_size(page)

    left = ft.Column(
        spacing=20,
        controls=[
            _status_chip(profile),
            ft.Column(
                spacing=2,
                controls=[
                    ft.Text(
                        "$ whoami",
                        color=MUTED,
                        size=13,
                        font_family="Mono",
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=14,
                        run_spacing=0,
                        controls=[
                            ft.Text(
                                "Mauricio",
                                size=title_size,
                                color=TEXT,
                                font_family="DisplayBold",
                                weight=ft.FontWeight.W_700,
                            ),
                            gradient_text("Obando", size=title_size),
                        ],
                    ),
                ],
            ),
            RoleTyper(roles, size=18 if is_mobile(page) else 22),
            ft.Container(
                width=620,
                content=ft.Text(profile.get("subtitle", ""), color=MUTED, size=16),
            ),
            _cta_row(page, profile),
            ft.Row(
                wrap=True,
                spacing=8,
                run_spacing=8,
                controls=[SkillPill(skill) for skill in profile.get("skills", [])[:8]],
            ),
        ],
    )

    right = ft.Column(
        spacing=14,
        controls=[
            TerminalBlock(content.get("hero_commands", []), title="mauricio@cloud:~"),
            ConsolePanel(
                ft.Column(
                    spacing=14,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    "live telemetry",
                                    color=PRIMARY,
                                    size=12,
                                    font_family="Mono",
                                ),
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        PulsingDot(SECONDARY),
                                        ft.Text(
                                            "all systems nominal",
                                            color=SECONDARY,
                                            size=12,
                                            font_family="Mono",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        SignalGrid(),
                    ],
                ),
                padding=ft.Padding.all(20),
                glow=True,
            ),
        ],
    )

    return ft.Container(
        data={"kind": "hero_console"},
        content=ft.Column(
            spacing=26,
            controls=[
                ft.ResponsiveRow(
                    columns=12,
                    spacing=24,
                    run_spacing=22,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(col={"xs": 12, "lg": 7}, content=left),
                        ft.Container(col={"xs": 12, "lg": 5}, content=right),
                    ],
                ),
                _metrics_row(content),
            ],
        ),
    )
