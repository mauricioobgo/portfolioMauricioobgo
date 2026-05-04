from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import LottiePanel, MetricCard, SkillPill
from portfolio.components.terminal import TerminalBlock
from portfolio.responsive import hero_title_size, is_mobile
from portfolio.theme import (
    CARD,
    MUTED,
    PANEL,
    PRIMARY,
    PURPLE,
    SECONDARY,
    TEXT,
    WARNING,
    alpha,
    panel,
)


def _scroll_to(page: ft.Page, section_key: str) -> None:
    page.scroll_to(scroll_key=section_key, duration=700)


def HeroPanel(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    profile = content["profile"]
    metadata = content["metadata"]
    social_links = profile.get("social_links", {})
    metrics = [
        MetricCard("Runtime", "Flet", "Python-only static web UI", PRIMARY),
        MetricCard(
            "Repos", str(profile.get("github_public_repos", 0)), "Public repositories", SECONDARY
        ),
        MetricCard("Followers", str(profile.get("github_followers", 0)), "GitHub signal", PURPLE),
        MetricCard(
            "Refresh",
            str(metadata.get("refresh_log", {}).get("scope", "all")).upper(),
            "Latest cadence",
            WARNING,
        ),
    ]

    ctas = [
        ft.FilledButton(
            text="View Projects",
            style=ft.ButtonStyle(
                bgcolor=PRIMARY,
                color="#020617",
                padding=ft.Padding.symmetric(horizontal=20, vertical=18),
                shape=ft.RoundedRectangleBorder(radius=18),
            ),
            on_click=lambda _: _scroll_to(page, "projects"),
        ),
        ft.OutlinedButton(
            text="GitHub",
            style=ft.ButtonStyle(
                color=TEXT,
                padding=ft.Padding.symmetric(horizontal=20, vertical=18),
                shape=ft.RoundedRectangleBorder(radius=18),
            ),
            on_click=lambda _: page.launch_url(profile.get("github_url")),
        ),
        ft.OutlinedButton(
            text="LinkedIn",
            style=ft.ButtonStyle(
                color=TEXT,
                padding=ft.Padding.symmetric(horizontal=20, vertical=18),
                shape=ft.RoundedRectangleBorder(radius=18),
            ),
            on_click=lambda _: page.launch_url(social_links.get("linkedin")),
        ),
        ft.OutlinedButton(
            text="Download Resume",
            style=ft.ButtonStyle(
                color=TEXT,
                padding=ft.Padding.symmetric(horizontal=20, vertical=18),
                shape=ft.RoundedRectangleBorder(radius=18),
            ),
            on_click=lambda _: page.launch_url(profile.get("resume_link")),
        ),
    ]

    left = ft.Column(
        spacing=18,
        controls=[
            ft.Row(
                wrap=True,
                spacing=10,
                run_spacing=10,
                controls=[
                    SkillPill("PYTHON 3.14", SECONDARY),
                    SkillPill("FLET STATIC WEB", PRIMARY),
                    SkillPill("GITHUB ACTIONS PAGES", PURPLE),
                ],
            ),
            ft.Text(
                profile.get("name", "Mauricio Obando"),
                size=hero_title_size(page),
                color=TEXT,
                font_family="DisplayBold",
                weight=ft.FontWeight.W_700,
            ),
            ft.Text(
                profile.get("title", ""),
                size=20 if is_mobile(page) else 24,
                color=PRIMARY,
                font_family="Display",
                weight=ft.FontWeight.W_600,
            ),
            ft.Text(profile.get("subtitle", ""), color=MUTED, size=17),
            ft.Row(
                wrap=True,
                spacing=10,
                run_spacing=10,
                controls=[SkillPill(skill) for skill in profile.get("skills", [])],
            ),
            ft.Row(wrap=True, spacing=12, run_spacing=12, controls=ctas),
            TerminalBlock(content.get("hero_commands", []), title="mauricio.cloud.status"),
        ],
    )

    right = ft.Column(
        spacing=18,
        controls=[
            LottiePanel(
                "AI / Cloud command center",
                "lottie/ai_network.json",
                caption="Static-web-safe animation panel with graceful fallback when assets are missing or unsupported.",
                accent=PRIMARY,
            ),
            panel(
                ft.ResponsiveRow(
                    columns=12,
                    spacing=14,
                    run_spacing=14,
                    controls=[
                        ft.Container(col={"xs": 6, "md": 6}, content=metric) for metric in metrics
                    ],
                ),
                bgcolor=alpha(PANEL, 0.95),
                padding=ft.Padding.all(18),
            ),
        ],
    )

    return panel(
        ft.ResponsiveRow(
            columns=12,
            spacing=20,
            run_spacing=20,
            controls=[
                ft.Container(col={"xs": 12, "xl": 7}, content=left),
                ft.Container(col={"xs": 12, "xl": 5}, content=right),
            ],
        ),
        padding=ft.Padding.all(28),
        bgcolor=alpha(CARD, 0.95),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[alpha(PANEL, 0.98), alpha("#111827", 0.98), alpha("#091321", 0.98)],
        ),
    )
