from __future__ import annotations

import flet as ft

from portfolio.interaction import scroll_to, section_link_data
from portfolio.responsive import content_width
from portfolio.theme import BORDER, MUTED, PANEL, PRIMARY, TEXT, alpha


class ConsoleTopbar(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        self._page = page
        self._active = "focus"
        self._shell_ref = ft.Ref[ft.Container]()
        self._button_refs: dict[str, ft.Ref[ft.Container]] = {}
        self._items = [
            ("Focus", "focus"),
            ("Projects", "projects"),
            ("Experience", "experience"),
            ("Terminal", "terminal"),
            ("Certifications", "certifications"),
            ("GitHub", "github"),
            ("AI", "ai"),
            ("Stack", "stack"),
            ("Contact", "contact"),
        ]
        super().__init__(data={"kind": "topbar"}, content=self._build())

    def _build(self) -> ft.Control:
        return ft.Container(
            ref=self._shell_ref,
            width=content_width(self._page),
            padding=ft.Padding.symmetric(horizontal=20, vertical=12),
            border_radius=18,
            bgcolor=alpha(PANEL, 0.92),
            border=ft.Border.all(1, alpha(BORDER, 0.6)),
            shadow=[
                ft.BoxShadow(
                    blur_radius=24,
                    color="#0008",
                    offset=ft.Offset(0, 8),
                )
            ],
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                wrap=True,
                spacing=16,
                run_spacing=12,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(
                                "BACKEND · DATA · CLOUD · AI",
                                color=PRIMARY,
                                size=10,
                                font_family="Mono",
                                weight=ft.FontWeight.W_700,
                            ),
                            ft.Text(
                                "Mauricio Obando",
                                color=TEXT,
                                size=18,
                                font_family="DisplayBold",
                                weight=ft.FontWeight.W_700,
                            ),
                        ],
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=6,
                        run_spacing=8,
                        controls=[self._build_button(label, key) for label, key in self._items],
                    ),
                ],
            ),
        )

    def _build_button(self, label: str, section_key: str) -> ft.Control:
        ref = ft.Ref[ft.Container]()
        self._button_refs[section_key] = ref
        return ft.Container(
            ref=ref,
            data=section_link_data(label, section_key),
            ink=True,
            border_radius=999,
            animate=ft.Animation(220, ft.AnimationCurve.EASE_OUT),
            on_click=lambda _, key=section_key: self._activate(key),
            content=self._button_content(label, section_key == self._active),
        )

    def _button_content(self, label: str, active: bool) -> ft.Control:
        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
            border_radius=999,
            bgcolor=alpha(PRIMARY, 0.12) if active else None,
            border=ft.Border.all(1, alpha(PRIMARY, 0.45)) if active else None,
            shadow=(
                [
                    ft.BoxShadow(
                        blur_radius=16,
                        color=alpha(PRIMARY, 0.2),
                        offset=ft.Offset(0, 0),
                    )
                ]
                if active
                else None
            ),
            content=ft.Text(
                label,
                color=PRIMARY if active else MUTED,
                size=12,
                font_family="Mono",
                weight=ft.FontWeight.W_700 if active else ft.FontWeight.W_400,
            ),
        )

    def _activate(self, section_key: str) -> None:
        self.set_active(section_key)
        scroll_to(self._page, section_key, duration=680)

    def set_active(self, section_key: str) -> None:
        self._active = section_key
        for label, key in self._items:
            container = self._button_refs[key].current
            if container:
                container.content = self._button_content(label, key == section_key)
                container.update()

    def sync_width(self, page_width: float | int | None) -> None:
        if self._shell_ref.current:
            self._shell_ref.current.width = content_width(page_width)
            self._shell_ref.current.update()


def NavigationBar(page: ft.Page) -> ConsoleTopbar:
    return ConsoleTopbar(page)
