from __future__ import annotations

import flet as ft

from portfolio.theme import MUTED, PRIMARY, TEXT, alpha, panel


def _scroll_to(page: ft.Page, section_key: str) -> None:
    page.scroll_to(scroll_key=section_key, duration=650)


def NavigationBar(page: ft.Page) -> ft.Control:
    items = [
        ("Focus", "focus"),
        ("Projects", "projects"),
        ("Experience", "experience"),
        ("Certifications", "certifications"),
        ("GitHub", "github"),
        ("Stack", "stack"),
        ("Contact", "contact"),
    ]
    return panel(
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
                                "MAURICIO CLOUD CONSOLE", color=PRIMARY, size=12, font_family="Mono"
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
                        spacing=10,
                        run_spacing=10,
                        controls=[
                            ft.TextButton(
                                content=ft.Text(label, color=TEXT, size=12, font_family="Mono"),
                                style=ft.ButtonStyle(
                                    side=ft.Border.all(1, alpha(MUTED, 0.35)),
                                    padding=ft.Padding.symmetric(horizontal=16, vertical=14),
                                    shape=ft.RoundedRectangleBorder(radius=18),
                                ),
                                on_click=lambda _, key=section_key: _scroll_to(page, key),
                            )
                            for label, section_key in items
                        ],
                    ),
                ),
            ],
        ),
        bgcolor=alpha("#0F172A", 0.90),
        padding=ft.Padding.all(20),
    )
