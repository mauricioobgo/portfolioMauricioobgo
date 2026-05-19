from __future__ import annotations

import flet as ft

from portfolio.components.assistant import PortfolioTerminalShell
from portfolio.components.cards import SectionHeader


def TerminalSection(
    page: ft.Page,
    terminal_shell: PortfolioTerminalShell,
) -> ft.Control:
    return ft.Container(
        key="terminal",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "TERMINAL",
                    "mauricio@cloud:~$",
                    "A real Linux-style shell. Try whoami, ls, cat about.md, projects, or matrix.",
                ),
                terminal_shell,
            ],
        ),
    )
