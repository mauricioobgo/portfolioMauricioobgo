from __future__ import annotations

from pathlib import Path

import flet as ft

from portfolio.interaction import attach_hover_lift, external_link_data, normalize_external_url
from portfolio.responsive import section_title_size
from portfolio.theme import (
    BORDER,
    CARD,
    MUTED,
    PANEL,
    PRIMARY,
    PURPLE,
    ROSE,
    SECONDARY,
    TEXT,
    WARNING,
    alpha,
    panel,
)

try:
    import flet_lottie as ftl
except ImportError:  # pragma: no cover - exercised through fallback behavior.
    ftl = None


def SkillPill(label: str, accent: str = PRIMARY) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=12, vertical=7),
        bgcolor=alpha(accent, 0.12),
        border=ft.Border.all(1, alpha(accent, 0.26)),
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
            ft.Row(
                spacing=8,
                controls=[
                    ft.Container(width=10, height=10, bgcolor=ROSE, border_radius=999),
                    ft.Container(width=10, height=10, bgcolor=WARNING, border_radius=999),
                    ft.Container(width=10, height=10, bgcolor=SECONDARY, border_radius=999),
                    ft.Text(title, color=PRIMARY, size=12, font_family="Mono"),
                ],
            )
        )
        controls.append(ft.Container(height=1, bgcolor=alpha(BORDER, 0.92)))
    controls.append(content)
    base_panel = panel(
        ft.Column(
            spacing=14 if title else 0,
            controls=controls,
        ),
        padding=padding or ft.Padding.all(22),
        bgcolor=bgcolor or alpha(PANEL, 0.86),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[
                alpha(PANEL, 0.97),
                alpha(CARD, 0.94),
                alpha("#101B2B", 0.94),
            ],
        ),
    )
    if not glow:
        return base_panel
    return ft.Container(
        shadow=[
            ft.BoxShadow(
                spread_radius=1,
                blur_radius=28,
                color=alpha(PRIMARY, 0.20),
                offset=ft.Offset(0, 10),
            )
        ],
        content=base_panel,
    )


def MetricCard(label: str, value: str, caption: str, accent: str = PRIMARY) -> ft.Control:
    return attach_hover_lift(
        ConsolePanel(
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
            padding=ft.Padding.all(18),
            bgcolor=alpha(CARD, 0.92),
        ),
        scale=1.03,
    )


def SectionHeader(page: ft.Page, eyebrow: str, title: str, description: str) -> ft.Control:
    return ft.Column(
        spacing=12,
        controls=[
            ft.Text(
                f"// {eyebrow.lower()}",
                color=PRIMARY,
                size=12,
                font_family="Mono",
                weight=ft.FontWeight.W_600,
            ),
            ft.Text(
                title,
                size=section_title_size(page),
                color=TEXT,
                font_family="DisplayBold",
                weight=ft.FontWeight.W_700,
            ),
            ft.Container(
                width=880,
                content=ft.Text(description, color=MUTED, size=16),
            ),
        ],
    )


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
        bgcolor=alpha(PANEL, 0.90),
        glow=True,
    )


def ConsoleFooter(metadata: dict) -> ft.Control:
    runtime = metadata.get("runtime", "static_web")
    return ConsolePanel(
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
        title="console://runtime",
    )


def link_button(label: str, url: str, *, accent: str = PRIMARY) -> ft.Control:
    valid_url = normalize_external_url(url)
    return ft.TextButton(
        content=ft.Text(label, color=accent, size=13, font_family="Mono"),
        style=ft.ButtonStyle(
            side=ft.Border.all(1, alpha(accent, 0.28)),
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            shape=ft.RoundedRectangleBorder(radius=16),
        ),
        url=valid_url,
        disabled=valid_url is None,
        data=external_link_data(label, url),
    )


def asset_exists(asset_path: str) -> bool:
    return (Path(__file__).resolve().parents[2] / "assets" / asset_path).exists()
