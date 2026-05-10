from __future__ import annotations

import flet as ft

from portfolio.components.cards import ConsolePanel
from portfolio.interaction import scroll_to, section_link_data
from portfolio.theme import MUTED, PRIMARY, TEXT, alpha


class _ConsoleTopbar(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        self._page = page
        self._active = "focus"
        self._button_refs: dict[str, ft.Ref[ft.TextButton]] = {}
        self._items = [
            ("Focus", "focus"),
            ("Projects", "projects"),
            ("Experience", "experience"),
            ("Certifications", "certifications"),
            ("GitHub", "github"),
            ("AI", "assistant"),
            ("Stack", "stack"),
            ("Contact", "contact"),
        ]
        super().__init__(content=self._build())

    def _build_button(self, label: str, section_key: str) -> ft.Control:
        ref = ft.Ref[ft.TextButton]()
        self._button_refs[section_key] = ref
        active = section_key == self._active
        return ft.TextButton(
            ref=ref,
            content=ft.Text(
                label,
                color=TEXT if active else MUTED,
                size=12,
                font_family="Mono",
            ),
            style=self._button_style(active),
            data=section_link_data(label, section_key),
            on_click=lambda _, key=section_key: self._activate(key),
        )

    def _button_style(self, active: bool) -> ft.ButtonStyle:
        return ft.ButtonStyle(
            bgcolor=alpha(PRIMARY, 0.14) if active else alpha("#0B1120", 0.65),
            side=ft.Border.all(1, alpha(PRIMARY, 0.34) if active else alpha(MUTED, 0.18)),
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            shape=ft.RoundedRectangleBorder(radius=18),
        )

    def _build(self) -> ft.Control:
        return ConsolePanel(
            ft.ResponsiveRow(
                columns=12,
                spacing=14,
                run_spacing=14,
                controls=[
                    ft.Container(
                        col={"xs": 12, "md": 4},
                        content=ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(
                                    "MAURICIO CLOUD CONSOLE",
                                    color=PRIMARY,
                                    size=11,
                                    font_family="Mono",
                                ),
                                ft.Text(
                                    "Mauricio Obando",
                                    color=TEXT,
                                    size=24,
                                    font_family="DisplayBold",
                                    weight=ft.FontWeight.W_700,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        col={"xs": 12, "md": 8},
                        alignment=ft.Alignment(1, 0),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            wrap=True,
                            spacing=8,
                            run_spacing=8,
                            controls=[
                                self._build_button(label, section_key)
                                for label, section_key in self._items
                            ],
                        ),
                    ),
                ],
            ),
            padding=ft.Padding.symmetric(horizontal=20, vertical=16),
            bgcolor=alpha("#0F172A", 0.82),
        )

    def _activate(self, section_key: str) -> None:
        self._active = section_key
        for key, ref in self._button_refs.items():
            button = ref.current
            if not button:
                continue
            active = key == section_key
            label = next(item_label for item_label, item_key in self._items if item_key == key)
            button.style = self._button_style(active)
            button.content = ft.Text(
                label,
                color=TEXT if active else MUTED,
                size=12,
                font_family="Mono",
            )
            button.update()
        scroll_to(self._page, section_key, duration=650)


def NavigationBar(page: ft.Page) -> ft.Control:
    return _ConsoleTopbar(page)
