from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import BentoGrid, ConsoleFooter, ConsolePanel, SkillPill
from portfolio.interaction import attach_hover_lift, external_link_data, normalize_external_url
from portfolio.theme import MUTED, PRIMARY, SECONDARY, TEXT


def ContactCard(title: str, value: str, caption: str, url: str, accent: str) -> ft.Control:
    return attach_hover_lift(
        ConsolePanel(
            ft.Column(
                spacing=14,
                controls=[
                    SkillPill(title.upper(), accent),
                    ft.Text(
                        value,
                        color=TEXT,
                        size=22,
                        font_family="DisplayBold",
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(caption, color=MUTED, size=14),
                    ft.FilledButton(
                        content="Open",
                        style=ft.ButtonStyle(
                            bgcolor=accent,
                            color="#020617",
                            shape=ft.RoundedRectangleBorder(radius=16),
                        ),
                        url=normalize_external_url(url),
                        data=external_link_data(title, url),
                    ),
                ],
            ),
            title=f"contact://{title.lower()}",
            bgcolor="#111827",
        ),
        scale=1.02,
    )


def ContactGrid(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    profile = content["profile"]
    social_links = profile.get("social_links", {})
    cards = [
        (
            "Email",
            profile.get("email", ""),
            "Direct channel for platform, data, and AI engineering work.",
            f"mailto:{profile.get('email', '')}",
            PRIMARY,
        ),
        (
            "LinkedIn",
            "linkedin.com/in/mauricioobgo",
            "Public work history, certifications, and profile context.",
            social_links.get("linkedin", ""),
            SECONDARY,
        ),
        (
            "GitHub",
            "github.com/mauricioobgo",
            "Repository activity, engineering experiments, and current code.",
            profile.get("github_url", ""),
            "#A855F7",
        ),
    ]
    return ft.Column(
        spacing=18,
        controls=[
            BentoGrid(
                [
                    ft.Container(
                        col={"xs": 12, "md": 6, "xl": 4},
                        content=ContactCard(title, value, caption, url, accent),
                    )
                    for title, value, caption, url, accent in cards
                ]
                + [
                    ft.Container(
                        col={"xs": 12, "md": 6, "xl": 4},
                        content=attach_hover_lift(
                            ConsolePanel(
                                ft.Column(
                                    spacing=14,
                                    controls=[
                                        SkillPill("LOCATION", SECONDARY),
                                        ft.Text(
                                            profile.get("location", ""),
                                            color=TEXT,
                                            size=22,
                                            font_family="DisplayBold",
                                            weight=ft.FontWeight.W_700,
                                        ),
                                        ft.Text(
                                            "Open to backend, data, cloud, and AI platform work with a Python-first delivery focus.",
                                            color=MUTED,
                                            size=14,
                                        ),
                                    ],
                                ),
                                title="signal://availability",
                                glow=True,
                                bgcolor="#111827",
                            ),
                            scale=1.02,
                        ),
                    )
                ]
            ),
            ConsoleFooter(content["metadata"]),
            ft.Text(
                (
                    f"(c) {content['metadata']['generated_at'][:4]} Mauricio Obando - "
                    "built with Flet - reference-aligned console edition"
                ),
                color=MUTED,
                size=12,
                font_family="Mono",
                text_align=ft.TextAlign.CENTER,
            ),
        ],
    )
