from __future__ import annotations

import flet as ft


MOBILE = 720
TABLET = 1040


def viewport_width(page: ft.Page) -> float:
    return float(page.width or 1366)


def is_mobile(page: ft.Page) -> bool:
    return viewport_width(page) < MOBILE


def is_tablet(page: ft.Page) -> bool:
    return MOBILE <= viewport_width(page) < TABLET


def hero_title_size(page: ft.Page) -> int:
    if is_mobile(page):
        return 34
    if is_tablet(page):
        return 44
    return 56


def section_title_size(page: ft.Page) -> int:
    return 28 if is_mobile(page) else 34
