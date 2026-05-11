from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel, MetricCard, SkillPill
from portfolio.components.mascots import RetroDroidRunway
from portfolio.components.terminal import TerminalBlock
from portfolio.interaction import (
    attach_hover_lift,
    external_link_data,
    normalize_external_url,
    scroll_to,
    section_link_data,
)
from portfolio.responsive import hero_title_size, is_mobile
from portfolio.theme import MUTED, PRIMARY, PURPLE, SECONDARY, TEXT, WARNING


def _signal_bars() -> ft.Control:
    heights = [24, 46, 34, 58, 26, 52, 38, 62, 28, 56, 32, 48]
    return ft.Row(
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.END,
        controls=[
            ft.Container(
                width=12,
                height=height,
                border_radius=6,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(0, 1),
                    end=ft.Alignment(0, -1),
                    colors=[PRIMARY, PURPLE],
                ),
                opacity=0.84,
            )
            for height in heights
        ],
    )


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
        attach_hover_lift(
            ft.FilledButton(
                content=ft.Text("$ open_projects", font_family="Mono"),
                style=ft.ButtonStyle(
                    bgcolor=PRIMARY,
                    color="#020617",
                    padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                    shape=ft.RoundedRectangleBorder(radius=18),
                ),
                data=section_link_data("View Projects", "projects"),
                on_click=lambda _: scroll_to(page, "projects"),
            )
        ),
        attach_hover_lift(
            ft.OutlinedButton(
                content=ft.Text("$ github", font_family="Mono"),
                style=ft.ButtonStyle(
                    color=TEXT,
                    padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                    shape=ft.RoundedRectangleBorder(radius=18),
                ),
                url=normalize_external_url(profile.get("github_url")),
                data=external_link_data("GitHub", profile.get("github_url")),
            )
        ),
        attach_hover_lift(
            ft.OutlinedButton(
                content=ft.Text("$ linkedin", font_family="Mono"),
                style=ft.ButtonStyle(
                    color=TEXT,
                    padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                    shape=ft.RoundedRectangleBorder(radius=18),
                ),
                url=normalize_external_url(social_links.get("linkedin")),
                data=external_link_data("LinkedIn", social_links.get("linkedin")),
            )
        ),
        attach_hover_lift(
            ft.OutlinedButton(
                content=ft.Text("$ download_resume", font_family="Mono"),
                style=ft.ButtonStyle(
                    color=TEXT,
                    padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                    shape=ft.RoundedRectangleBorder(radius=18),
                ),
                url=normalize_external_url(profile.get("resume_link")),
                data=external_link_data("Download Resume", profile.get("resume_link")),
            )
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
                size=22 if is_mobile(page) else 26,
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
        spacing=14,
        controls=[
            ConsolePanel(
                ft.Column(
                    spacing=14,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                SkillPill("AI / CLOUD COMMAND CENTER", PRIMARY),
                                SkillPill("SIGNAL LIVE", SECONDARY),
                            ],
                        ),
                        ft.Text(
                            "Network rhythm, status pulses, and console motion shaped after the reference portfolio hero stack.",
                            color=MUTED,
                            size=14,
                        ),
                        _signal_bars(),
                    ],
                ),
                padding=ft.Padding.all(20),
                glow=True,
            ),
            RetroDroidRunway(),
            ConsolePanel(
                ft.Column(
                    spacing=14,
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
                            spacing=10,
                            run_spacing=10,
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
            spacing=24,
            run_spacing=22,
            controls=[
                ft.Container(col={"xs": 12, "xl": 7}, content=left),
                ft.Container(col={"xs": 12, "xl": 5}, content=right),
            ],
        ),
        padding=ft.Padding.all(30),
        glow=True,
    )
