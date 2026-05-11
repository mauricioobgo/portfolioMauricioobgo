from __future__ import annotations

import flet as ft

from portfolio.interaction import scroll_to, section_link_data
from portfolio.theme import PANEL, PRIMARY, SECTION_WIDTH, TEXT, alpha


class ConsoleTopbar(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        self._page = page
        self._active = "focus"
        self._button_refs: dict[str, ft.Ref[ft.Container]] = {}
        self._items = [
            ("Focus", "focus"),
            ("Projects", "projects"),
            ("Experience", "experience"),
            ("Terminal", "assistant"),
            ("Certifications", "certifications"),
            ("GitHub", "github"),
            ("Stack", "stack"),
            ("Contact", "contact"),
        ]
        super().__init__(data={"kind": "topbar"}, content=self._build())

    def _build(self) -> ft.Control:
        return ft.Container(
            width=SECTION_WIDTH,
            padding=ft.Padding.symmetric(horizontal=18, vertical=14),
            border_radius=24,
            bgcolor=alpha(PANEL, 0.74),
            border=ft.Border.all(1, alpha(PRIMARY, 0.22)),
            shadow=[
                ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=18,
                    color=alpha("#000000", 0.72),
                    offset=ft.Offset(0, 8),
                )
            ],
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                wrap=True,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(
                                "MAURICIO CLOUD CONSOLE",
                                color=PRIMARY,
                                size=10,
                                font_family="Mono",
                                weight=ft.FontWeight.W_700,
                            ),
                            ft.Text(
                                "Mauricio Obando",
                                color=TEXT,
                                size=20,
                                font_family="DisplayBold",
                                weight=ft.FontWeight.W_700,
                            ),
                        ],
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=8,
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
            padding=ft.Padding.symmetric(horizontal=15, vertical=10),
            border_radius=999,
            bgcolor=alpha(PRIMARY, 0.12) if active else alpha("#09111E", 0.72),
            border=ft.Border.all(1, alpha(PRIMARY, 0.32) if active else alpha(TEXT, 0.1)),
            shadow=(
                [
                    ft.BoxShadow(
                        blur_radius=18,
                        color=alpha(PRIMARY, 0.18),
                        offset=ft.Offset(0, 0),
                    )
                ]
                if active
                else None
            ),
            content=ft.Text(
                label,
                color=TEXT if active else alpha(TEXT, 0.72),
                size=12,
                font_family="Mono",
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


def NavigationBar(page: ft.Page) -> ConsoleTopbar:
    return ConsoleTopbar(page)
