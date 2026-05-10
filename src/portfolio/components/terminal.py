from __future__ import annotations

import flet as ft

from portfolio.components.cards import ConsolePanel
from portfolio.components.mascots import ConsoleSweep
from portfolio.theme import MUTED, TEXT


def TerminalBlock(lines: list[str], *, title: str = "console://mauricio") -> ft.Control:
    controls: list[ft.Control] = []

    for line in lines:
        if line:
            controls.append(
                ft.Text(
                    line, color=TEXT if line.startswith("$") else MUTED, size=13, font_family="Mono"
                )
            )
        else:
            controls.append(ft.Text("", size=8))

    return ConsolePanel(
        ft.Column(
            spacing=10,
            controls=[
                ConsoleSweep(),
                *controls,
            ],
        ),
        title=title,
        padding=ft.Padding.all(18),
        bgcolor="#0B1120",
    )
