from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import flet as ft


LinkData = dict[str, Any]


def normalize_external_url(url: str | None) -> str | None:
    candidate = (url or "").strip()
    if not candidate:
        return None

    parsed = urlparse(candidate)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return candidate
    if parsed.scheme == "mailto" and parsed.path:
        return candidate
    return None


def external_link_data(label: str, url: str | None) -> LinkData:
    normalized = normalize_external_url(url)
    return {
        "kind": "external_link",
        "label": label,
        "target": normalized,
        "raw_target": url or "",
        "valid": bool(normalized),
    }


def section_link_data(label: str, section_key: str) -> LinkData:
    return {
        "kind": "section_link",
        "label": label,
        "target": section_key,
        "valid": True,
    }


def scroll_to(page: ft.Page, section_key: str, *, duration: int = 700) -> None:
    if hasattr(page, "scroll_to"):
        page.scroll_to(scroll_key=section_key, duration=duration)


def attach_hover_lift(
    control: ft.Control,
    *,
    scale: float = 1.02,
    y_offset: float = -0.012,
) -> ft.Control:
    control.animate_scale = ft.Animation(180, ft.AnimationCurve.EASE_OUT)
    control.animate_offset = ft.Animation(180, ft.AnimationCurve.EASE_OUT)
    control.scale = 1
    control.offset = ft.Offset(0, 0)

    def _handle_hover(event: ft.ControlEvent) -> None:
        hovered = event.data == "true"
        control.scale = scale if hovered else 1
        control.offset = ft.Offset(0, y_offset if hovered else 0)
        control.update()

    control.on_hover = _handle_hover
    return control
