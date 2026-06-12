from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel
from portfolio.interaction import attach_hover_lift, external_link_data, normalize_external_url
from portfolio.theme import MUTED, PRIMARY, TEXT, alpha


def _channel_button(
    icon: ft.IconData,
    label: str,
    value: str,
    url: str | None,
    *,
    filled: bool = False,
) -> ft.Control:
    normalized = normalize_external_url(url) if url else None
    foreground = "#04070F" if filled else TEXT
    button_content = ft.Row(
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Icon(icon, size=16, color=foreground if filled else PRIMARY),
            ft.Text(
                value,
                color=foreground,
                size=13,
                font_family="Mono",
                weight=ft.FontWeight.W_700 if filled else ft.FontWeight.W_400,
            ),
        ],
    )
    if filled:
        return attach_hover_lift(
            ft.FilledButton(
                content=button_content,
                style=ft.ButtonStyle(
                    bgcolor=PRIMARY,
                    color="#04070F",
                    padding=ft.Padding.symmetric(horizontal=20, vertical=16),
                    shape=ft.RoundedRectangleBorder(radius=14),
                ),
                url=normalized,
                disabled=normalized is None,
                data=external_link_data(label, url),
            )
        )
    return attach_hover_lift(
        ft.OutlinedButton(
            content=button_content,
            style=ft.ButtonStyle(
                side=ft.BorderSide(1, alpha(PRIMARY, 0.35)),
                padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=14),
            ),
            url=normalized,
            disabled=normalized is None,
            data=external_link_data(label, url),
        )
    )


def ContactGrid(_page: ft.Page, content: dict[str, Any]) -> ft.Control:
    profile = content["profile"]
    social_links = profile.get("social_links", {})
    email = profile.get("email", "")
    footer_year = str(content.get("metadata", {}).get("generated_at", ""))[:4] or "2026"
    return ft.Column(
        spacing=18,
        controls=[
            ConsolePanel(
                ft.Column(
                    spacing=18,
                    controls=[
                        ft.Text(
                            "Hiring for backend, data, cloud, or AI?",
                            color=TEXT,
                            size=26,
                            font_family="DisplayBold",
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "One email away. I usually reply within a day.",
                            color=MUTED,
                            size=15,
                        ),
                        ft.Row(
                            wrap=True,
                            spacing=12,
                            run_spacing=12,
                            controls=[
                                _channel_button(
                                    ft.Icons.MAIL,
                                    "Email",
                                    email,
                                    f"mailto:{email}",
                                    filled=True,
                                ),
                                _channel_button(
                                    ft.Icons.WORK_OUTLINE,
                                    "LinkedIn",
                                    "linkedin.com/in/mauricioobgo",
                                    social_links.get("linkedin", ""),
                                ),
                                _channel_button(
                                    ft.Icons.CODE,
                                    "GitHub",
                                    "github.com/mauricioobgo",
                                    profile.get("github_url", ""),
                                ),
                                _channel_button(
                                    ft.Icons.DOWNLOAD,
                                    "Resume",
                                    "resume.pdf",
                                    profile.get("resume_link", ""),
                                ),
                            ],
                        ),
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.PLACE, color=MUTED, size=14),
                                ft.Text(
                                    f"{profile.get('location', '')} · remote-friendly",
                                    color=MUTED,
                                    size=13,
                                    font_family="Mono",
                                ),
                            ],
                        ),
                    ],
                ),
                title="mauricio@cloud:~$ contact",
                padding=ft.Padding.all(28),
                glow=True,
            ),
            ft.Text(
                f"© {footer_year} Mauricio Obando · 100% Python · built with Flet · "
                "deployed on GitHub Pages",
                color=MUTED,
                size=12,
                font_family="Mono",
                text_align=ft.TextAlign.CENTER,
            ),
        ],
    )
