from __future__ import annotations

import flet as ft

from portfolio.responsive import content_gutter, content_width


BACKGROUND = "#050712"
PANEL = "#07162E"
CARD = "#081B3D"
BORDER = "#163B8F"
PRIMARY = "#00E5FF"
SECONDARY = "#35FF7A"
PURPLE = "#FF4FD8"
WARNING = "#FFD21F"
ROSE = "#FF4D6D"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
TERMINAL = "#22C55E"
ERROR = ROSE

SECTION_WIDTH = 1240
CARD_RADIUS = 22
CARD_SHADOW = [
    ft.BoxShadow(
        spread_radius=0,
        blur_radius=14,
        color="#000000",
        offset=ft.Offset(0, 8),
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
                    colors=[BACKGROUND, "#06172F", "#090B22"],
                ),
            ),
            ft.Container(
                expand=True,
                image=ft.DecorationImage(
                    src=_maze_grid_svg(),
                    repeat=ft.ImageRepeat.REPEAT,
                    opacity=0.22,
                ),
            ),
            ft.Container(
                expand=True,
                image=ft.DecorationImage(
                    src=_pellet_grid_svg(),
                    repeat=ft.ImageRepeat.REPEAT,
                    opacity=0.26,
                ),
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
            bgcolor=alpha(PRIMARY, 0.06 if column % 2 == 0 else 0.025),
        )
        for column in range(13)
    ]
    horizontals = [
        ft.Container(
            left=0,
            right=0,
            top=40 + row * 92,
            height=1,
            bgcolor=alpha(BORDER, 0.11 if row % 2 == 0 else 0.045),
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
            bgcolor=alpha(PRIMARY, 0.018),
        )
        for stripe in range(120)
    ]


def _maze_grid_svg() -> str:
    return (
        "data:image/svg+xml;utf8,"
        "<svg xmlns='http://www.w3.org/2000/svg' width='96' height='96' viewBox='0 0 96 96'>"
        "<path d='M8 8H88V24H24V40H88V56H8V72H72V88H8Z' "
        "fill='none' stroke='%2300E5FF' stroke-width='2' stroke-opacity='0.24' "
        "stroke-linejoin='round'/>"
        "</svg>"
    )


def _pellet_grid_svg() -> str:
    return (
        "data:image/svg+xml;utf8,"
        "<svg xmlns='http://www.w3.org/2000/svg' width='48' height='48' viewBox='0 0 48 48'>"
        "<circle cx='6' cy='6' r='2.2' fill='%23FFD21F' fill-opacity='0.44' />"
        "</svg>"
    )
