from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import BentoGrid, LottiePanel, SkillPill, panel
from portfolio.interaction import attach_hover_lift
from portfolio.theme import MUTED, PRIMARY, PURPLE, SECONDARY, TEXT, alpha


class AssistantPromptBoard(ft.Container):
    def __init__(self, prompts: list[str], cli_command: str) -> None:
        self.prompts = prompts
        self.cli_command = cli_command
        self._preview_ref = ft.Ref[ft.Text]()
        self._chip_refs = [ft.Ref[ft.TextButton]() for _ in prompts]
        self._active_index = 0
        super().__init__(content=self._build())

    def _build_chip(self, index: int, prompt: str) -> ft.Control:
        active = index == self._active_index
        return ft.TextButton(
            ref=self._chip_refs[index],
            content=ft.Text(prompt, color=PRIMARY if active else TEXT, size=13),
            style=ft.ButtonStyle(
                bgcolor=alpha(PRIMARY, 0.16) if active else alpha("#0F172A", 0.88),
                side=ft.Border.all(1, alpha(PRIMARY if active else MUTED, 0.28)),
                padding=ft.Padding.symmetric(horizontal=16, vertical=14),
                shape=ft.RoundedRectangleBorder(radius=18),
            ),
            data={"kind": "assistant_prompt", "index": index, "prompt": prompt},
            on_click=lambda _, idx=index: self._select(idx),
        )

    def _build(self) -> ft.Control:
        return ft.Column(
            spacing=16,
            controls=[
                ft.Row(
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                    controls=[
                        self._build_chip(index, prompt) for index, prompt in enumerate(self.prompts)
                    ],
                ),
                panel(
                    ft.Column(
                        spacing=12,
                        controls=[
                            ft.Row(
                                wrap=True,
                                spacing=10,
                                run_spacing=10,
                                controls=[
                                    SkillPill("CLI MODE", SECONDARY),
                                    SkillPill("STATIC SITE SAFE", PURPLE),
                                ],
                            ),
                            ft.Text(
                                "Selected assistant prompt",
                                color=PRIMARY,
                                size=12,
                                font_family="Mono",
                            ),
                            ft.Text(
                                self.prompts[0]
                                if self.prompts
                                else "Add assistant_prompts to profile.yaml",
                                ref=self._preview_ref,
                                color=TEXT,
                                size=18,
                                font_family="DisplayBold",
                            ),
                            ft.Text(
                                "Public GitHub Pages remains static. The AI assistant runs locally/admin-side with generated context from your resume, portfolio data, and GitHub snapshot.",
                                color=MUTED,
                                size=14,
                            ),
                            ft.Text("Run locally", color=PRIMARY, size=12, font_family="Mono"),
                            ft.Text(
                                self.cli_command,
                                color=TEXT,
                                size=13,
                                font_family="Mono",
                            ),
                        ],
                    ),
                    bgcolor=alpha("#111827", 0.94),
                ),
            ],
        )

    def _select(self, index: int) -> None:
        self._active_index = index
        if self._preview_ref.current:
            self._preview_ref.current.value = self.prompts[index]
            self._preview_ref.current.update()
        for chip_index, ref in enumerate(self._chip_refs):
            button = ref.current
            if not button:
                continue
            active = chip_index == index
            button.style = ft.ButtonStyle(
                bgcolor=alpha(PRIMARY, 0.16) if active else alpha("#0F172A", 0.88),
                side=ft.Border.all(1, alpha(PRIMARY if active else MUTED, 0.28)),
                padding=ft.Padding.symmetric(horizontal=16, vertical=14),
                shape=ft.RoundedRectangleBorder(radius=18),
            )
            button.content = ft.Text(
                self.prompts[chip_index],
                color=PRIMARY if active else TEXT,
                size=13,
            )
            button.update()


def AssistantExperienceGrid(content: dict[str, Any]) -> ft.Control:
    assistant = content.get("assistant", {})
    resume = content.get("resume", {})
    prompts = assistant.get("prompts", [])
    cli_command = assistant.get("cli_command", "uv run python -m portfolio_app.scripts.chat_cv")
    cards = [
        attach_hover_lift(
            panel(
                ft.Column(
                    spacing=14,
                    controls=[
                        SkillPill("ASK MAURICIO AI", PRIMARY),
                        ft.Text(
                            assistant.get("status", "CLI mode"),
                            color=TEXT,
                            size=22,
                            font_family="DisplayBold",
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(assistant.get("description", ""), color=MUTED, size=14),
                        AssistantPromptBoard(prompts, cli_command),
                    ],
                )
            ),
            scale=1.01,
        ),
        attach_hover_lift(
            LottiePanel(
                "AI context pipeline",
                "lottie/developer_terminal.json",
                caption=(
                    "Resume, GitHub, certifications, and curated case studies are packed into generated context files ready for the local CLI assistant."
                ),
                accent=PURPLE,
                icon=ft.Icons.DATA_OBJECT,
            ),
            scale=1.01,
        ),
        attach_hover_lift(
            panel(
                ft.Column(
                    spacing=14,
                    controls=[
                        SkillPill("RESUME SNAPSHOT", SECONDARY),
                        ft.Text(
                            resume.get("synced_at") or "Awaiting monthly sync",
                            color=TEXT,
                            size=20,
                            font_family="DisplayBold",
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "The monthly pipeline downloads the public Drive CV, extracts text, reports drift, and feeds the AI context bundle without scraping LinkedIn.",
                            color=MUTED,
                            size=14,
                        ),
                        ft.Row(
                            wrap=True,
                            spacing=10,
                            run_spacing=10,
                            controls=[
                                SkillPill(keyword, SECONDARY)
                                for keyword in resume.get("keywords", [])[:8]
                            ],
                        ),
                    ],
                )
            ),
            scale=1.01,
        ),
    ]

    return BentoGrid(
        [
            ft.Container(col={"xs": 12, "xl": 6}, content=cards[0]),
            ft.Container(col={"xs": 12, "md": 6, "xl": 3}, content=cards[1]),
            ft.Container(col={"xs": 12, "md": 6, "xl": 3}, content=cards[2]),
        ]
    )
