from __future__ import annotations

import asyncio
from typing import Any

import flet as ft

from portfolio.components.assistant import PortfolioTerminalShell, build_terminal_shell
from portfolio.components.mascots import PacmanBorderOverlay
from portfolio.components.nav import NavigationBar
from portfolio.data_loader import load_portfolio_content
from portfolio.interaction import scroll_to
from portfolio.responsive import content_gutter, content_width, is_desktop, shell_top_padding
from portfolio.sections.ai_section import AISection
from portfolio.sections.certifications_section import CertificationsSection
from portfolio.sections.contact_section import ContactSection
from portfolio.sections.experience_section import ExperienceSection
from portfolio.sections.focus_section import FocusSection
from portfolio.sections.github_section import GitHubSection
from portfolio.sections.hero_section import HeroSection
from portfolio.sections.projects_section import ProjectsSection
from portfolio.sections.stack_section import StackSection
from portfolio.sections.terminal_section import TerminalSection
from portfolio.theme import MUTED, PRIMARY, TEXT, app_shell, apply_theme, panel


def _loading_view() -> ft.Control:
    return ft.Container(
        expand=True,
        bgcolor="#020617",
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            controls=[
                ft.ProgressRing(color=PRIMARY),
                ft.Text(
                    "loading mauricio cloud console...",
                    color=PRIMARY,
                    font_family="Mono",
                    size=13,
                ),
            ],
        ),
    )


def _error_view(message: str) -> ft.Control:
    return ft.Container(
        expand=True,
        bgcolor="#020617",
        alignment=ft.Alignment(0, 0),
        content=panel(
            ft.Column(
                spacing=14,
                controls=[
                    ft.Text(
                        "Unable to load portfolio content",
                        color=TEXT,
                        size=28,
                        font_family="DisplayBold",
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(message, color=MUTED, size=15),
                ],
            ),
            padding=ft.Padding.all(28),
        ),
    )


class PortfolioView(ft.Container):
    def __init__(self, page: ft.Page, content: dict[str, Any]) -> None:
        self._section_refs: list[ft.Ref[ft.Container]] = []
        self._revealing = False
        self._layout_ref = ft.Ref[ft.Container]()
        self._content_ref = ft.Ref[ft.Container]()
        self._border_overlay = PacmanBorderOverlay()
        self._desktop_topbar = NavigationBar(page)
        self._inline_topbar = NavigationBar(page)
        self._desktop_topbar_host = ft.Container(
            top=22,
            left=0,
            right=0,
            alignment=ft.Alignment(0, -1),
            visible=is_desktop(page),
            content=self._desktop_topbar,
        )
        self._inline_topbar_host = ft.Container(
            visible=not is_desktop(page),
            padding=ft.Padding.only(bottom=14),
            content=self._inline_topbar,
        )
        self._previous_scroll_handler = None
        self._previous_resize_handler = None
        self._scroll_pixels = 0.0
        self._max_scroll = 1.0
        self._nav_keys = [
            "focus",
            "projects",
            "experience",
            "terminal",
            "certifications",
            "github",
            "ai",
            "stack",
            "contact",
        ]
        self._terminal_shell: PortfolioTerminalShell = build_terminal_shell(page, content)
        sections = [
            ft.Column(spacing=18, controls=[self._inline_topbar_host, HeroSection(page, content)]),
            FocusSection(page, content),
            ProjectsSection(page, content),
            ExperienceSection(page, content),
            TerminalSection(page, self._terminal_shell),
            CertificationsSection(page, content),
            GitHubSection(page, content),
            AISection(page, content, on_prompt=self._handle_ai_prompt),
            StackSection(page, content),
            ContactSection(page, content),
        ]
        desktop_overlay = is_desktop(page)
        super().__init__(
            expand=True,
            content=app_shell(
                ft.Column(
                    spacing=88,
                    controls=[
                        self._animated_section(section, index)
                        for index, section in enumerate(sections)
                    ],
                ),
                overlays=[
                    self._border_overlay,
                    self._desktop_topbar_host,
                ],
                page_width=getattr(page, "width", 0),
                layout_ref=self._layout_ref,
                content_ref=self._content_ref,
                top_padding=shell_top_padding(page, desktop_overlay=desktop_overlay),
            ),
        )

    def _animated_section(self, control: ft.Control, index: int) -> ft.Control:
        ref = ft.Ref[ft.Container]()
        self._section_refs.append(ref)
        return ft.Container(
            ref=ref,
            opacity=0 if index else 1,
            offset=ft.Offset(0, 0.05 if index else 0),
            animate_opacity=ft.Animation(420, ft.AnimationCurve.EASE_OUT),
            animate_offset=ft.Animation(420, ft.AnimationCurve.EASE_OUT),
            content=control,
        )

    def did_mount(self) -> None:
        if self.page and not self._revealing:
            self._revealing = True
            self._previous_scroll_handler = getattr(self.page, "on_scroll", None)
            self._previous_resize_handler = getattr(self.page, "on_resize", None)
            self.page.on_scroll = self._handle_scroll
            self.page.on_resize = self._handle_resize
            self._sync_layout()
            self._sync_chrome(0, 1)
            self.page.run_task(self._reveal_sections)

    def will_unmount(self) -> None:
        if not self.page:
            return
        if self.page.on_scroll == self._handle_scroll:
            self.page.on_scroll = self._previous_scroll_handler
        if self.page.on_resize == self._handle_resize:
            self.page.on_resize = self._previous_resize_handler

    async def _reveal_sections(self) -> None:
        for index, ref in enumerate(self._section_refs):
            if not ref.current or index == 0:
                continue
            ref.current.opacity = 1
            ref.current.offset = ft.Offset(0, 0)
            ref.current.update()
            await asyncio.sleep(0.08)

    def _handle_scroll(self, event: ft.OnScrollEvent) -> None:
        self._scroll_pixels = float(getattr(event, "pixels", 0) or 0)
        self._max_scroll = float(
            getattr(event, "max_scroll_extent", 0) or getattr(event, "max_scroll", 0) or 0
        )
        self._sync_chrome(self._scroll_pixels, self._max_scroll or 1)
        if callable(self._previous_scroll_handler):
            self._previous_scroll_handler(event)

    def _handle_resize(self, event: ft.ControlEvent) -> None:
        self._sync_layout()
        self._sync_chrome(self._scroll_pixels, self._max_scroll or 1)
        if callable(self._previous_resize_handler):
            self._previous_resize_handler(event)

    def _handle_ai_prompt(self, prompt: str) -> None:
        self._terminal_shell.prefill(prompt)
        if self.page:
            scroll_to(self.page, "terminal", duration=720)

    def _set_active_section(self, section_key: str) -> None:
        self._desktop_topbar.set_active(section_key)
        self._inline_topbar.set_active(section_key)

    def _sync_layout(self) -> None:
        if not self.page:
            return
        width = float(getattr(self.page, "width", 0) or 0)
        desktop_overlay = is_desktop(width)
        gutter = content_gutter(width)
        clamped_width = content_width(width)
        top_padding = shell_top_padding(width, desktop_overlay=desktop_overlay)

        if self._layout_ref.current:
            self._layout_ref.current.padding = ft.Padding(
                left=gutter,
                right=gutter,
                top=top_padding,
                bottom=44,
            )
            self._layout_ref.current.update()

        if self._content_ref.current:
            self._content_ref.current.width = clamped_width
            self._content_ref.current.update()

        self._desktop_topbar.sync_width(width)
        self._inline_topbar.sync_width(width)
        self._desktop_topbar_host.visible = desktop_overlay
        self._inline_topbar_host.visible = not desktop_overlay
        self._desktop_topbar_host.update()
        self._inline_topbar_host.update()
        self._terminal_shell.sync_layout(width)

    def _sync_chrome(self, pixels: float, max_scroll: float) -> None:
        if not self.page:
            return
        width = float(getattr(self.page, "width", 0) or 0)
        height = float(getattr(self.page, "height", 0) or 0)
        self._border_overlay.sync(
            pixels=pixels,
            max_scroll=max_scroll,
            width=width,
            height=height,
        )
        if max_scroll > 0:
            progress = max(0.0, min(1.0, pixels / max_scroll))
            index = min(int(progress * len(self._nav_keys) * 1.04), len(self._nav_keys) - 1)
            self._set_active_section(self._nav_keys[index])


def build_portfolio_view(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return PortfolioView(page, content)


async def main(page: ft.Page) -> None:
    apply_theme(page)
    page.add(_loading_view())
    page.update()

    try:
        content = await load_portfolio_content(page)
    except Exception as error:
        page.clean()
        page.add(_error_view(str(error)))
        page.update()
        return

    page.clean()
    page.add(build_portfolio_view(page, content))
    page.update()


def run() -> None:
    ft.run(main, assets_dir="assets", route_url_strategy=ft.RouteUrlStrategy.HASH)
