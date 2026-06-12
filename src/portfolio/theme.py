from __future__ import annotations

import flet as ft

from portfolio.responsive import content_gutter, content_width


BACKGROUND = "#04070F"
PANEL = "#0A1322"
CARD = "#0D1830"
BORDER = "#1E3A5F"
PRIMARY = "#22D3EE"
SECONDARY = "#34D399"
PURPLE = "#A78BFA"
WARNING = "#FBBF24"
ROSE = "#FB7185"
TEXT = "#F1F5F9"
MUTED = "#8FA3BF"
TERMINAL = "#22C55E"
ERROR = ROSE

SECTION_WIDTH = 1240
CARD_RADIUS = 20
CARD_SHADOW = [
    ft.BoxShadow(
        spread_radius=0,
        blur_radius=18,
        color="#0009",
        offset=ft.Offset(0, 10),
    )
]


def alpha(color: str, opacity: float) -> str:
    return ft.Colors.with_opacity(opacity, color)


def apply_theme(page: ft.Page) -> None:
    page.title = "Mauricio Obando | Backend, Data, Cloud & AI Engineer"
    page.bgcolor = BACKGROUND
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ALWAYS
    page.fonts = {
        "Body": "fonts/Poppins-Regular.ttf",
        "Display": "fonts/Poppins-SemiBold.ttf",
        "DisplayBold": "fonts/Poppins-Bold.ttf",
        "Mono": "fonts/IBMPlexMono-Medium.ttf",
    }
    page.theme = ft.Theme(font_family="Body")


def app_shell(
    content: ft.Control,
    *,
    overlays: list[ft.Control] | None = None,
    page_width: float | int | None = None,
    layout_ref: ft.Ref[ft.Container] | None = None,
    content_ref: ft.Ref[ft.Container] | None = None,
    top_padding: int = 120,
) -> ft.Control:
    chrome = overlays or []
    gutter = content_gutter(page_width)
    width = content_width(page_width)
    return ft.Container(
        expand=True,
        content=ft.Stack(
            expand=True,
            controls=[
                background_glow(),
                *chrome,
                ft.Container(
                    ref=layout_ref,
                    alignment=ft.Alignment(0, -1),
                    padding=ft.Padding(
                        left=gutter,
                        right=gutter,
                        top=top_padding,
                        bottom=44,
                    ),
                    content=ft.Container(ref=content_ref, width=width, content=content),
                ),
            ],
        ),
    )


def panel(
    content: ft.Control,
    *,
    padding: ft.PaddingValue | None = None,
    bgcolor: str = CARD,
    gradient: ft.Gradient | None = None,
) -> ft.Container:
    return ft.Container(
        content=content,
        padding=padding or ft.Padding.all(24),
        bgcolor=bgcolor,
        gradient=gradient,
        border=ft.Border.all(1, alpha(BORDER, 0.55)),
        border_radius=CARD_RADIUS,
        shadow=CARD_SHADOW,
    )


def gradient_text(value: str, *, size: int, colors: list[str] | None = None) -> ft.Control:
    return ft.ShaderMask(
        blend_mode=ft.BlendMode.SRC_IN,
        shader=ft.LinearGradient(
            begin=ft.Alignment(-1, 0),
            end=ft.Alignment(1, 0),
            colors=colors or [PRIMARY, PURPLE],
        ),
        content=ft.Text(
            value,
            size=size,
            color=TEXT,
            font_family="DisplayBold",
            weight=ft.FontWeight.W_700,
        ),
    )


def accent_rule(accent: str = PRIMARY, *, width: int = 64) -> ft.Control:
    return ft.Container(
        width=width,
        height=3,
        border_radius=999,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, 0),
            end=ft.Alignment(1, 0),
            colors=[accent, alpha(accent, 0.0)],
        ),
    )


def background_glow() -> ft.Control:
    return ft.Stack(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(-1, -1),
                    end=ft.Alignment(1, 1),
                    colors=[BACKGROUND, "#071226", "#070A1C"],
                ),
            ),
            ft.Container(
                left=-160,
                top=-120,
                width=560,
                height=560,
                border_radius=999,
                gradient=ft.RadialGradient(
                    colors=[alpha(PRIMARY, 0.10), alpha(PRIMARY, 0.0)],
                ),
            ),
            ft.Container(
                right=-200,
                top=240,
                width=640,
                height=640,
                border_radius=999,
                gradient=ft.RadialGradient(
                    colors=[alpha(PURPLE, 0.08), alpha(PURPLE, 0.0)],
                ),
            ),
            ft.Container(
                left=120,
                bottom=-260,
                width=620,
                height=620,
                border_radius=999,
                gradient=ft.RadialGradient(
                    colors=[alpha(SECONDARY, 0.05), alpha(SECONDARY, 0.0)],
                ),
            ),
            ft.Container(
                expand=True,
                image=ft.DecorationImage(
                    src=_grid_svg(),
                    repeat=ft.ImageRepeat.REPEAT,
                    opacity=0.5,
                ),
            ),
        ],
    )


def _grid_svg() -> str:
    return (
        "data:image/svg+xml;utf8,"
        "<svg xmlns='http://www.w3.org/2000/svg' width='72' height='72' viewBox='0 0 72 72'>"
        "<path d='M72 0H0V72' fill='none' stroke='%2322D3EE' stroke-opacity='0.05' "
        "stroke-width='1'/>"
        "<circle cx='0' cy='0' r='1' fill='%2322D3EE' fill-opacity='0.10'/>"
        "</svg>"
    )
