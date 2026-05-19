from __future__ import annotations

import flet as ft


MOBILE = 720
TABLET = 1040
SECTION_WIDTH = 1240


def viewport_width(page_or_width: ft.Page | float | int | None) -> float:
    if isinstance(page_or_width, ft.Page):
        return float(page_or_width.width or 1366)
    if hasattr(page_or_width, "width"):
        return float(getattr(page_or_width, "width", 1366) or 1366)
    if page_or_width is None:
        return 1366.0
    width = float(page_or_width or 0)
    return width if width > 0 else 1366.0


def is_mobile(page_or_width: ft.Page | float | int | None) -> bool:
    return viewport_width(page_or_width) < MOBILE


def is_tablet(page_or_width: ft.Page | float | int | None) -> bool:
    width = viewport_width(page_or_width)
    return MOBILE <= width < TABLET


def is_desktop(page_or_width: ft.Page | float | int | None) -> bool:
    return viewport_width(page_or_width) >= TABLET


def content_gutter(page_or_width: ft.Page | float | int | None) -> int:
    width = viewport_width(page_or_width)
    if width < MOBILE:
        return 14
    if width < TABLET:
        return 18
    return 24


def content_width(page_or_width: ft.Page | float | int | None) -> int:
    width = viewport_width(page_or_width)
    gutter = content_gutter(width)
    available = max(width - (gutter * 2), 320)
    return int(min(SECTION_WIDTH, available))


def shell_top_padding(page_or_width: ft.Page | float | int | None, *, desktop_overlay: bool) -> int:
    width = viewport_width(page_or_width)
    if desktop_overlay:
        return 118
    if width < MOBILE:
        return 20
    if width < TABLET:
        return 28
    return 36


def hero_title_size(page: ft.Page) -> int:
    if is_mobile(page):
        return 34
    if is_tablet(page):
        return 44
    return 56


def section_title_size(page: ft.Page) -> int:
    return 28 if is_mobile(page) else 34
