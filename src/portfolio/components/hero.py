from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel, LottiePanel, MetricCard, SkillPill
from portfolio.components.mascots import RetroDroidRunway
from portfolio.components.terminal import TerminalBlock
from portfolio.responsive import hero_title_size, is_mobile
from portfolio.theme import MUTED, PRIMARY, PURPLE, SECONDARY, TEXT, WARNING


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
            content="$ open_projects",
            style=ft.ButtonStyle(
                bgcolor=PRIMARY,
                color="#020617",
                padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=18),
            ),
            on_click=lambda _: _scroll_to(page, "projects"),
        ),
        ft.OutlinedButton(
            content="$ github",
            style=ft.ButtonStyle(
                color=TEXT,
                padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=18),
            ),
            on_click=lambda _: page.launch_url(profile.get("github_url")),
        ),
        ft.OutlinedButton(
            content="$ linkedin",
            style=ft.ButtonStyle(
                color=TEXT,
                padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=18),
            ),
            on_click=lambda _: page.launch_url(social_links.get("linkedin")),
        ),
        ft.OutlinedButton(
            content="$ download_resume",
            style=ft.ButtonStyle(
                color=TEXT,
                padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=18),
            ),
            on_click=lambda _: page.launch_url(profile.get("resume_link")),
        ),
    ]

    left = ft.Column(
        spacing=18,
        controls=[
            TerminalBlock(content.get("hero_commands", []), title="console://mauricio"),
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
            ft.Row(
                wrap=True,
                spacing=12,
                run_spacing=0,
                controls=[
                    ft.Text(
                        "Mauricio",
                        size=hero_title_size(page),
                        color=TEXT,
                        font_family="DisplayBold",
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(
                        "Obando",
                        size=hero_title_size(page),
                        color=PRIMARY,
                        font_family="DisplayBold",
                        weight=ft.FontWeight.W_700,
                    ),
                ],
            ),
            ft.Text(
                profile.get("title", ""),
                size=22 if is_mobile(page) else 28,
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
        ],
    )

    right = ft.Column(
        spacing=18,
        controls=[
            LottiePanel(
                "AI / Cloud command center",
                "lottie/ai_network.json",
                caption="Animated network pulses, terminal energy, and command-center motion inspired by the reference Pac-Man console portfolio.",
                accent=PRIMARY,
            ),
            RetroDroidRunway(),
            ConsolePanel(
                ft.Column(
                    spacing=16,
                    controls=[
                        ft.Row(
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
                                            f"available - {profile.get('company', '')}",
                                            color=SECONDARY,
                                            size=12,
                                            font_family="Mono",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.ResponsiveRow(
                            columns=12,
                            spacing=14,
                            run_spacing=14,
                            controls=[
                                ft.Container(col={"xs": 6, "md": 6}, content=metric)
                                for metric in metrics
                            ],
                        ),
                    ],
                ),
                title="console://status",
                padding=ft.Padding.all(18),
            ),
        ],
    )

    return ConsolePanel(
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
        glow=True,
    )
