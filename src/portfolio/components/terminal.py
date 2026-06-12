from __future__ import annotations

import asyncio

import flet as ft

from portfolio.components.ambient import ConsoleSweep
from portfolio.components.cards import ConsolePanel
from portfolio.theme import MUTED, PANEL, SECONDARY, TEXT, alpha


class TerminalBlock(ft.Container):
    def __init__(self, lines: list[str], *, title: str = "console://mauricio") -> None:
        self._source_lines = lines
        self._body_ref = ft.Ref[ft.Column]()
        self._caret_ref = ft.Ref[ft.Container]()
        self._running = False
        super().__init__(content=self._build(title))

    def _build(self, title: str) -> ft.Control:
        return ConsolePanel(
            ft.Column(
                spacing=12,
                controls=[
                    ConsoleSweep(),
                    ft.Column(ref=self._body_ref, spacing=8, controls=[]),
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Text(
                                "boot sequence active",
                                color=SECONDARY,
                                size=12,
                                font_family="Mono",
                            ),
                            ft.Container(
                                ref=self._caret_ref,
                                width=10,
                                height=16,
                                bgcolor=SECONDARY,
                                border_radius=2,
                            ),
                        ],
                    ),
                ],
            ),
            title=title,
            padding=ft.Padding.all(18),
            bgcolor=alpha(PANEL, 0.95),
        )

    def did_mount(self) -> None:
        self._running = True
        if self.page:
            self.page.run_task(self._reveal)

    def will_unmount(self) -> None:
        self._running = False

    async def _reveal(self) -> None:
        if not self._body_ref.current:
            return
        column = self._body_ref.current
        for line in self._source_lines:
            if not self._running or not self._body_ref.current:
                return
            column.controls.append(self._render_line(line))
            column.update()
            await asyncio.sleep(0.18 if line else 0.08)

        while self._running and self._caret_ref.current:
            self._caret_ref.current.opacity = 0
            self._caret_ref.current.update()
            await asyncio.sleep(0.5)
            self._caret_ref.current.opacity = 1
            self._caret_ref.current.update()
            await asyncio.sleep(0.5)

    def _render_line(self, line: str) -> ft.Control:
        if not line:
            return ft.Text("", size=8)
        return ft.Text(
            line,
            color=TEXT if line.startswith("$") else MUTED,
            size=13,
            font_family="Mono",
        )
