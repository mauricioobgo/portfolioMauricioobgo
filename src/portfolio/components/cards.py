from __future__ import annotations

from pathlib import Path

import flet as ft

from portfolio.responsive import section_title_size
from portfolio.theme import (
    CARD,
    MUTED,
    PANEL,
    PRIMARY,
    PURPLE,
    SECONDARY,
    TEXT,
    alpha,
    panel,
)

try:
    import flet_lottie as ftl
except ImportError:  # pragma: no cover - exercised through fallback behavior.
    ftl = None


def SkillPill(label: str, accent: str = PRIMARY) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=14, vertical=9),
        bgcolor=alpha(accent, 0.12),
        border=ft.Border.all(1, alpha(accent, 0.30)),
        border_radius=999,
        content=ft.Text(
            label,
            color=accent,
            size=12,
            font_family="Mono",
            weight=ft.FontWeight.W_600,
        ),
    )


def MetricCard(label: str, value: str, caption: str, accent: str = PRIMARY) -> ft.Control:
    return panel(
        ft.Column(
            spacing=10,
            controls=[
                ft.Text(label.upper(), color=accent, size=11, font_family="Mono"),
                ft.Text(
                    value,
                    color=TEXT,
                    size=26,
                    font_family="DisplayBold",
                    weight=ft.FontWeight.W_700,
                ),
                ft.Text(caption, color=MUTED, size=13),
            ],
        ),
        bgcolor=alpha(CARD, 0.96),
        padding=ft.Padding.all(18),
    )


def SectionHeader(page: ft.Page, eyebrow: str, title: str, description: str) -> ft.Control:
    return ft.Column(
        spacing=12,
        controls=[
            SkillPill(eyebrow, SECONDARY),
            ft.Text(
                title,
                size=section_title_size(page),
                color=TEXT,
                font_family="DisplayBold",
                weight=ft.FontWeight.W_700,
            ),
            ft.Container(
                width=820,
                content=ft.Text(description, color=MUTED, size=16),
            ),
        ],
    )


def BentoGrid(controls: list[ft.Control]) -> ft.Control:
    return ft.ResponsiveRow(columns=12, spacing=18, run_spacing=18, controls=controls)


def _lottie_fallback(title: str, caption: str, accent: str, icon: ft.IconData) -> ft.Control:
    return panel(
        ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Icon(icon, color=accent, size=42),
                ft.Text(title, color=TEXT, size=20, font_family="DisplayBold"),
                ft.Text(caption, color=MUTED, size=14, text_align=ft.TextAlign.CENTER),
            ],
        ),
        padding=ft.Padding.all(24),
        bgcolor=alpha(PANEL, 0.90),
    )


def LottiePanel(
    title: str,
    asset_path: str,
    *,
    caption: str,
    accent: str = PRIMARY,
    icon: ft.IconData = ft.Icons.AUTO_AWESOME,
) -> ft.Control:
    if ftl is None:
        return _lottie_fallback(title, caption, accent, icon)

    error_content = _lottie_fallback(title, caption, accent, icon)
    return panel(
        ft.Column(
            spacing=16,
            controls=[
                ft.Row(
                    spacing=8,
                    controls=[
                        SkillPill("LOTTIE", accent),
                        SkillPill("STATIC WEB", PURPLE),
                    ],
                ),
                ft.Container(
                    height=240,
                    alignment=ft.Alignment(0, 0),
                    content=ftl.Lottie(
                        src=asset_path,
                        animate=True,
                        repeat=True,
                        fit=ft.BoxFit.CONTAIN,
                        error_content=error_content,
                    ),
                ),
                ft.Text(title, color=TEXT, size=20, font_family="DisplayBold"),
                ft.Text(caption, color=MUTED, size=14),
            ],
        ),
        padding=ft.Padding.all(22),
        bgcolor=alpha(PANEL, 0.90),
    )


def ConsoleFooter(metadata: dict) -> ft.Control:
    runtime = metadata.get("runtime", "static_web")
    return panel(
        ft.Column(
            spacing=8,
            controls=[
                ft.Text("> deploy_status: online", color=SECONDARY, size=12, font_family="Mono"),
                ft.Text(f"> runtime: {runtime}", color=MUTED, size=12, font_family="Mono"),
                ft.Text("> python: 3.14", color=MUTED, size=12, font_family="Mono"),
                ft.Text(
                    "> source: python_generated_content", color=MUTED, size=12, font_family="Mono"
                ),
            ],
        ),
        padding=ft.Padding.all(18),
    )


def link_button(label: str, url: str, page: ft.Page, *, accent: str = PRIMARY) -> ft.Control:
    return ft.TextButton(
        content=ft.Text(label, color=accent, size=13, font_family="Mono"),
        on_click=(lambda _: page.launch_url(url)) if url else None,
    )


def asset_exists(asset_path: str) -> bool:
    return (Path(__file__).resolve().parents[2] / "assets" / asset_path).exists()
