from __future__ import annotations

import flet as ft

from portfolio.theme import CARD, MUTED, PRIMARY, TERMINAL, TEXT, alpha, panel


def TerminalBlock(lines: list[str], *, title: str = "console://mauricio") -> ft.Control:
    controls: list[ft.Control] = [
        ft.Row(
            spacing=8,
            controls=[
                ft.Container(width=10, height=10, bgcolor="#FB7185", border_radius=999),
                ft.Container(width=10, height=10, bgcolor="#F59E0B", border_radius=999),
                ft.Container(width=10, height=10, bgcolor=TERMINAL, border_radius=999),
                ft.Text(title, color=PRIMARY, size=12, font_family="Mono"),
            ],
        )
    ]

    for line in lines:
        if line:
            controls.append(
                ft.Text(
                    line, color=TEXT if line.startswith("$") else MUTED, size=13, font_family="Mono"
                )
            )
        else:
            controls.append(ft.Text("", size=8))

    return panel(
        ft.Column(spacing=10, controls=controls),
        bgcolor=alpha(CARD, 0.98),
        padding=ft.Padding.all(18),
    )
