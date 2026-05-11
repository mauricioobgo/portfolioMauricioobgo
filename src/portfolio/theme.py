from __future__ import annotations

import flet as ft


BACKGROUND = "#020617"
PANEL = "#0F172A"
CARD = "#111827"
BORDER = "#1E293B"
PRIMARY = "#38BDF8"
SECONDARY = "#22C55E"
PURPLE = "#A855F7"
WARNING = "#F59E0B"
ROSE = "#FB7185"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
TERMINAL = "#22C55E"
ERROR = ROSE

SECTION_WIDTH = 1240
CARD_RADIUS = 22
CARD_SHADOW = [
    ft.BoxShadow(
        spread_radius=1,
        blur_radius=22,
        color="#000000",
        offset=ft.Offset(0, 10),
    )
]


def alpha(color: str, opacity: float) -> str:
    return ft.Colors.with_opacity(opacity, color)


def apply_theme(page: ft.Page) -> None:
    page.title = "Mauricio Cloud Console"
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
    top_padding: int = 120,
) -> ft.Control:
    chrome = overlays or []
    return ft.Container(
        expand=True,
        content=ft.Stack(
            expand=True,
            controls=[
                background_glow(),
                *chrome,
                ft.Container(
                    alignment=ft.Alignment(0, -1),
                    padding=ft.Padding(left=18, right=18, top=top_padding, bottom=44),
                    content=ft.Container(width=SECTION_WIDTH, content=content),
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
        border=ft.Border.all(1, alpha(BORDER, 0.96)),
        border_radius=CARD_RADIUS,
        shadow=CARD_SHADOW,
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
                    colors=[BACKGROUND, "#06101B", "#081322"],
                ),
            ),
            ft.Container(
                expand=True,
                image=ft.DecorationImage(
                    src=_dot_grid_svg(),
                    repeat=ft.ImageRepeat.REPEAT,
                    opacity=0.28,
                ),
            ),
            ft.Container(
                left=-180,
                top=-120,
                width=520,
                height=520,
                border_radius=260,
                bgcolor=alpha(PRIMARY, 0.12),
            ),
            ft.Container(
                right=-200,
                top=180,
                width=620,
                height=620,
                border_radius=310,
                bgcolor=alpha(PURPLE, 0.12),
            ),
            ft.Container(
                left=180,
                bottom=-180,
                width=420,
                height=420,
                border_radius=210,
                bgcolor=alpha(WARNING, 0.08),
            ),
            *_grid_overlay(),
            *_scanline_overlay(),
        ],
    )


def _grid_overlay() -> list[ft.Control]:
    verticals = [
        ft.Container(
            left=24 + column * 96,
            top=0,
            bottom=0,
            width=1,
            bgcolor=alpha(PRIMARY, 0.055 if column % 2 == 0 else 0.028),
        )
        for column in range(13)
    ]
    horizontals = [
        ft.Container(
            left=0,
            right=0,
            top=40 + row * 92,
            height=1,
            bgcolor=alpha(PRIMARY, 0.04 if row % 2 == 0 else 0.02),
        )
        for row in range(10)
    ]
    return [*verticals, *horizontals]


def _scanline_overlay() -> list[ft.Control]:
    return [
        ft.Container(
            left=0,
            right=0,
            top=4 + stripe * 8,
            height=1,
            bgcolor=alpha(PRIMARY, 0.022),
        )
        for stripe in range(120)
    ]


def _dot_grid_svg() -> str:
    return (
        "data:image/svg+xml;utf8,"
        "<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 32 32'>"
        "<circle cx='1.5' cy='1.5' r='1.2' fill='%2338BDF8' fill-opacity='0.22' />"
        "</svg>"
    )
