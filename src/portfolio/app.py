from __future__ import annotations

import asyncio
from typing import Any

import flet as ft

from portfolio.components.mascots import ArcadeCommandRail
from portfolio.data_loader import load_portfolio_content
from portfolio.sections.assistant_section import AssistantSection
from portfolio.sections.certifications_section import CertificationsSection
from portfolio.sections.contact_section import ContactSection
from portfolio.sections.experience_section import ExperienceSection
from portfolio.sections.focus_section import FocusSection
from portfolio.sections.github_section import GitHubSection
from portfolio.sections.hero_section import HeroSection
from portfolio.sections.projects_section import ProjectsSection
from portfolio.sections.stack_section import StackSection
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
        self._arcade_rail = ArcadeCommandRail()
        sections = [
            HeroSection(page, content, accent_control=self._arcade_rail),
            FocusSection(page, content),
            ProjectsSection(page, content),
            ExperienceSection(page, content),
            CertificationsSection(page, content),
            GitHubSection(page, content),
            AssistantSection(page, content, on_enter_pacman=self._arcade_rail.boost),
            StackSection(page, content),
            ContactSection(page, content),
        ]
        super().__init__(
            expand=True,
            content=app_shell(
                ft.Column(
                    spacing=28,
                    controls=[
                        self._animated_section(section, index)
                        for index, section in enumerate(sections)
                    ],
                )
            ),
        )

    def _animated_section(self, control: ft.Control, index: int) -> ft.Control:
        ref = ft.Ref[ft.Container]()
        self._section_refs.append(ref)
        return ft.Container(
            ref=ref,
            opacity=0 if index else 1,
            offset=ft.Offset(0, 0.06 if index else 0),
            animate_opacity=ft.Animation(420, ft.AnimationCurve.EASE_OUT),
            animate_offset=ft.Animation(420, ft.AnimationCurve.EASE_OUT),
            content=control,
        )

    def did_mount(self) -> None:
        if self.page and not self._revealing:
            self._revealing = True
            self.page.run_task(self._reveal_sections)

    async def _reveal_sections(self) -> None:
        for index, ref in enumerate(self._section_refs):
            if not ref.current or index == 0:
                continue
            ref.current.opacity = 1
            ref.current.offset = ft.Offset(0, 0)
            ref.current.update()
            await asyncio.sleep(0.08)


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
