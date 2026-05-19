from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel
from portfolio.interaction import external_link_data, normalize_external_url
from portfolio.theme import MUTED, PRIMARY, TEXT, WARNING


def _contact_row(icon: ft.IconData, label: str, value: str, url: str | None = None) -> ft.Control:
    normalized = normalize_external_url(url) if url else None
    value_control: ft.Control
    if normalized:
        value_control = ft.TextButton(
            content=ft.Text(value, color=TEXT, size=14),
            url=normalized,
            data=external_link_data(label, url),
            style=ft.ButtonStyle(padding=0),
        )
    else:
        value_control = ft.Text(value, color=MUTED, size=14)

    return ft.Row(
        spacing=12,
        controls=[
            ft.Icon(icon, color=PRIMARY, size=16),
            value_control,
        ],
    )


def ContactGrid(_page: ft.Page, content: dict[str, Any]) -> ft.Control:
    profile = content["profile"]
    social_links = profile.get("social_links", {})
    footer_year = str(content.get("metadata", {}).get("generated_at", ""))[:4] or "2026"
    return ft.Column(
        spacing=18,
        controls=[
            ConsolePanel(
                ft.Column(
                    spacing=10,
                    controls=[
                        _contact_row(
                            ft.Icons.MAIL,
                            "Email",
                            profile.get("email", ""),
                            f"mailto:{profile.get('email', '')}",
                        ),
                        _contact_row(
                            ft.Icons.LINK,
                            "LinkedIn",
                            "linkedin.com/in/mauricioobgo",
                            social_links.get("linkedin", ""),
                        ),
                        _contact_row(
                            ft.Icons.CODE,
                            "GitHub",
                            "github.com/mauricioobgo",
                            profile.get("github_url", ""),
                        ),
                        _contact_row(
                            ft.Icons.PLACE,
                            "Location",
                            profile.get("location", ""),
                        ),
                    ],
                ),
                title="mauricio@cloud:~$ contact",
                padding=ft.Padding.all(24),
                bgcolor="#111827",
            ),
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan(
                        f"(c) {footer_year} Mauricio Obando - built with Flet - ",
                        ft.TextStyle(color=MUTED, size=12, font_family="Mono"),
                    ),
                    ft.TextSpan(
                        "try up up down down left right left right BA",
                        ft.TextStyle(color=WARNING, size=12, font_family="Mono"),
                    ),
                ],
            ),
        ],
    )
