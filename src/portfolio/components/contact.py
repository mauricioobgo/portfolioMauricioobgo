from __future__ import annotations

from collections.abc import Callable
from typing import Any

import flet as ft

from portfolio.components.cards import ConsoleFooter, ConsolePanel
from portfolio.theme import MUTED, PRIMARY, TEXT


def _contact_line(icon: str, value: str, action: Callable[[], None] | None = None) -> ft.Control:
    row = ft.Row(
        spacing=10,
        controls=[
            ft.Text(icon, color=PRIMARY, size=16, font_family="Mono"),
            ft.Text(value, color=TEXT if action else MUTED, size=14, font_family="Mono"),
        ],
    )
    if action is None:
        return row
    return ft.TextButton(
        content=row,
        style=ft.ButtonStyle(padding=ft.Padding.all(0)),
        on_click=lambda _: action(),
    )


def ContactGrid(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    profile = content["profile"]
    social_links = profile.get("social_links", {})
    return ft.Column(
        spacing=18,
        controls=[
            ConsolePanel(
                ft.Column(
                    spacing=14,
                    controls=[
                        _contact_line(
                            "mail",
                            profile.get("email", ""),
                            lambda: page.launch_url(f"mailto:{profile.get('email', '')}"),
                        ),
                        _contact_line(
                            "in",
                            "linkedin.com/in/mauricioobgo",
                            lambda: page.launch_url(social_links.get("linkedin", "")),
                        ),
                        _contact_line(
                            "gh",
                            "github.com/mauricioobgo",
                            lambda: page.launch_url(profile.get("github_url", "")),
                        ),
                        _contact_line("loc", profile.get("location", "")),
                        ft.Text(
                            "Open to backend, data, cloud, and AI platform work with a Python-first delivery focus.",
                            color=MUTED,
                            size=14,
                        ),
                    ],
                ),
                title="mauricio@cloud:~$ contact",
                glow=True,
                bgcolor="#111827",
            ),
            ConsoleFooter(content["metadata"]),
            ft.Text(
                f"(c) {content['metadata']['generated_at'][:4]} Mauricio Obando - built with Flet - reference-aligned console edition",
                color=MUTED,
                size=12,
                font_family="Mono",
                text_align=ft.TextAlign.CENTER,
            ),
        ],
    )
