from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.data_loader import load_portfolio_content
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


def build_portfolio_view(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return app_shell(
        ft.Column(
            spacing=28,
            controls=[
                HeroSection(page, content),
                FocusSection(page, content),
                ProjectsSection(page, content),
                ExperienceSection(page, content),
                CertificationsSection(page, content),
                GitHubSection(page, content),
                StackSection(page, content),
                ContactSection(page, content),
            ],
        )
    )


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
