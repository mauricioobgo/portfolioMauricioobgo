from __future__ import annotations

from pathlib import Path

import flet as ft

from portfolio.responsive import section_title_size
from portfolio.theme import (
    BORDER,
    MUTED,
    PANEL,
    PRIMARY,
    PURPLE,
    ROSE,
    SECONDARY,
    TEXT,
    WARNING,
    accent_rule,
    alpha,
    panel,
)

try:
    import flet_lottie as ftl
except ImportError:  # pragma: no cover - exercised through fallback behavior.
    ftl = None


def SkillPill(label: str, accent: str = PRIMARY) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
        bgcolor=alpha(accent, 0.10),
        border=ft.Border.all(1, alpha(accent, 0.24)),
        border_radius=999,
        content=ft.Text(
            label,
            color=accent,
            size=11,
            font_family="Mono",
            weight=ft.FontWeight.W_600,
        ),
    )


def ConsolePanel(
    content: ft.Control,
    *,
    title: str | None = None,
    glow: bool = False,
    padding: ft.PaddingValue | None = None,
    bgcolor: str | None = None,
) -> ft.Control:
    controls: list[ft.Control] = []
    if title:
        controls.append(
            ft.Container(
                padding=ft.Padding.only(bottom=12),
                border=ft.Border(bottom=ft.BorderSide(1, alpha(BORDER, 0.5))),
                content=ft.Row(
                    spacing=8,
                    controls=[
                        ft.Container(
                            width=9, height=9, bgcolor=alpha(ROSE, 0.8), border_radius=999
                        ),
                        ft.Container(
                            width=9, height=9, bgcolor=alpha(WARNING, 0.8), border_radius=999
                        ),
                        ft.Container(
                            width=9, height=9, bgcolor=alpha(SECONDARY, 0.8), border_radius=999
                        ),
                        ft.Container(width=4),
                        ft.Text(title, color=MUTED, size=12, font_family="Mono"),
                    ],
                ),
            )
        )
    controls.append(content)
    base_panel = panel(
        ft.Column(
            spacing=14 if title else 0,
            controls=controls,
        ),
        padding=padding or ft.Padding.all(22),
        bgcolor=bgcolor or alpha(PANEL, 0.88),
    )
    if not glow:
        return base_panel
    return ft.Container(
        shadow=[
            ft.BoxShadow(
                spread_radius=1,
                blur_radius=32,
                color=alpha(PRIMARY, 0.14),
                offset=ft.Offset(0, 10),
            )
        ],
        content=base_panel,
    )


def SectionHeader(
    page: ft.Page,
    eyebrow: str,
    title: str,
    description: str | None = None,
    *,
    accent: str = PRIMARY,
) -> ft.Control:
    controls: list[ft.Control] = [
        ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(width=22, height=2, bgcolor=accent, border_radius=999),
                ft.Text(
                    eyebrow.lower(),
                    color=accent,
                    size=12,
                    font_family="Mono",
                    weight=ft.FontWeight.W_700,
                ),
            ],
        ),
        ft.Text(
            title,
            size=section_title_size(page),
            color=TEXT,
            font_family="DisplayBold",
            weight=ft.FontWeight.W_700,
        ),
        accent_rule(accent),
    ]
    if description:
        controls.append(
            ft.Container(
                width=720,
                content=ft.Text(description, color=MUTED, size=15),
            )
        )
    return ft.Column(spacing=10, controls=controls)


def BentoGrid(controls: list[ft.Control]) -> ft.Control:
    return ft.ResponsiveRow(columns=12, spacing=18, run_spacing=18, controls=controls)


def _lottie_fallback(title: str, caption: str, accent: str, icon: ft.IconData) -> ft.Control:
    return ConsolePanel(
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
        title=title,
    )


def LottiePanel(
    title: str,
    asset_path: str,
    *,
    caption: str,
    accent: str = PRIMARY,
    icon: ft.IconData = ft.Icons.AUTO_AWESOME,
) -> ft.Control:
    if ftl is None or not asset_exists(asset_path):
        return _lottie_fallback(title, caption, accent, icon)

    error_content = _lottie_fallback(title, caption, accent, icon)
    return ConsolePanel(
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
                ft.Text(caption, color=MUTED, size=14),
            ],
        ),
        padding=ft.Padding.all(22),
        title=title,
        glow=True,
    )


def asset_exists(asset_path: str) -> bool:
    return (Path(__file__).resolve().parents[2] / "assets" / asset_path).exists()
