from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel, SkillPill
from portfolio.components.mascots import ConsoleSweep
from portfolio.interaction import attach_hover_lift
from portfolio.theme import MUTED, PRIMARY, PURPLE, SECONDARY, TEXT, WARNING, alpha


def _greeting_lines(content: dict[str, Any]) -> list[str]:
    profile = content.get("profile", {})
    prompts = profile.get("assistant_prompts", [])
    starter = (
        prompts[0] if prompts else "Ask how Mauricio builds backend, data, AI, and cloud systems."
    )
    return [
        "MauricioOS booting...",
        "Welcome to the command center. Glad you are here.",
        "This browser shell is static-safe and runs on predefined portfolio context.",
        f"Try: {starter}",
        "Press Enter to submit. Each command also boosts the arcade rail.",
    ]


def _latest_role_lines(content: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for entry in content.get("experience", [])[:3]:
        role = entry.get("role", "Role")
        company = entry.get("company", "Company")
        date = entry.get("date", "Timeline unavailable")
        lines.append(f"{date} | {role} @ {company}")
    return lines


def build_assistant_response(question: str, content: dict[str, Any]) -> list[str]:
    prompt = question.lower()
    profile = content.get("profile", {})
    projects = content.get("featured_projects", [])
    certifications = [
        cert.get("title", "Certification")
        for cert in content.get("certifications", [])
        if cert.get("featured")
    ]
    experience_lines = _latest_role_lines(content)
    repo_count = content.get("github", {}).get("summary", {}).get("repo_count", 0)
    email = profile.get("email", "mauricioobgo@gmail.com")
    resume_link = profile.get("resume_link", "")

    if any(token in prompt for token in ("hello", "hi", "hey", "greetings")):
        return [
            "Great to meet you.",
            "Mauricio focuses on backend, data, cloud, and AI delivery with a Python-first stack.",
            "Ask about FastAPI systems, AWS architecture, Redshift analytics, certifications, or recent roles.",
        ]

    if any(token in prompt for token in ("backend", "fastapi", "api", "python")):
        return [
            "Backend engineering signal: Python 3.14, FastAPI, async services, testing, and clean architecture.",
            "The portfolio highlights production-minded APIs, platform templates, and systems that stay maintainable under delivery pressure.",
            "A good follow-up is: how does Mauricio combine backend work with data and AI pipelines?",
        ]

    if any(token in prompt for token in ("data", "redshift", "dbt", "pipeline", "athena", "glue")):
        return [
            "Data engineering signal: Redshift, dbt, Spark, Glue, Athena, orchestration, and warehouse delivery.",
            "Mauricio's case studies lean toward analytics reliability, cost visibility, and production pipeline clarity.",
            "This is especially visible in the Redshift analyzer and AI DataOps portfolio entries.",
        ]

    if any(token in prompt for token in ("ai", "llm", "rag", "agent", "openai")):
        return [
            "AI engineering signal: RAG workflows, structured outputs, evaluation loops, tool calling, and LLM-assisted delivery.",
            "The portfolio positions AI work as applied systems engineering rather than isolated prompt experiments.",
            "The full OpenAI-powered version stays in the local CLI flow so GitHub Pages remains static-safe.",
        ]

    if any(
        token in prompt for token in ("cert", "certificate", "certification", "machine learning")
    ):
        joined = (
            ", ".join(certifications[:3])
            if certifications
            else "AWS certifications are configured from YAML."
        )
        return [
            f"Featured certifications: {joined}.",
            "Each certification card links to the LinkedIn certifications page without scraping LinkedIn.",
            "The highest-signal certifications here are Solutions Architect - Professional and Machine Learning - Specialty.",
        ]

    if any(token in prompt for token in ("aws", "cloud", "devops", "finops", "docker")):
        return [
            "Cloud signal: AWS architecture, Redshift operations, observability, CI/CD, Docker, and FinOps awareness.",
            "The site emphasizes production-grade delivery across cloud platforms, backend services, and analytics systems.",
            "If you want a concise pitch, ask for a recruiter summary next.",
        ]

    if any(token in prompt for token in ("experience", "role", "job", "career", "work history")):
        return [
            "Latest experience snapshot:",
            *experience_lines,
            "That timeline is driven from repository content so it stays aligned with the monthly refresh process.",
        ]

    if any(token in prompt for token in ("project", "portfolio", "github", "repo")):
        featured = ", ".join(project.get("name", "Project") for project in projects[:3])
        return [
            f"Featured project slice: {featured}.",
            f"GitHub snapshot currently exposes {repo_count} public repositories for the portfolio feed.",
            "Project cards expand inline so architecture, problem framing, and impact can stay visible without leaving the page.",
        ]

    if any(token in prompt for token in ("resume", "cv", "contact", "email", "linkedin", "hire")):
        lines = [
            f"Best direct contact: {email}.",
            "LinkedIn and GitHub links stay active in the contact and hero sections.",
        ]
        if resume_link:
            lines.append(f"Resume source: {resume_link}")
        return lines

    if "matrix" in prompt:
        return [
            "Wake up, recruiter...",
            "This shell can highlight backend, data, AI, AWS, certifications, and current experience without leaving the page.",
            "Ask a real portfolio question next and I will route the answer.",
        ]

    return [
        "I can answer predefined questions about Mauricio's backend, data, cloud, AI, projects, certifications, and recent roles.",
        "Try one of these topics: backend summary, AWS certifications, Redshift/data engineering, AI/LLM work, or recent experience.",
        "This browser console stays static-safe; the full OpenAI-powered assistant remains available through the local CLI flow.",
    ]


def _terminal_line(text: str, role: str) -> ft.Control:
    prefixes = {"system": "#", "assistant": ">", "user": "$"}
    colors = {"system": SECONDARY, "assistant": TEXT, "user": PRIMARY}
    return ft.Text(
        f"{prefixes.get(role, '>')} {text}",
        color=colors.get(role, TEXT),
        size=13,
        font_family="Mono",
    )


class AssistantTerminalShell(ft.Container):
    def __init__(
        self,
        content: dict[str, Any],
        cli_command: str,
        *,
        on_enter_pacman: Callable[[str], None] | None = None,
    ) -> None:
        self._content = content
        self._cli_command = cli_command
        self._on_enter_pacman = on_enter_pacman
        self._history: list[tuple[str, str]] = [
            ("system", line) for line in _greeting_lines(content)
        ]
        self._log_ref = ft.Ref[ft.ListView]()
        self._input_ref = ft.Ref[ft.TextField]()
        self._status_ref = ft.Ref[ft.Text]()
        self._thinking_ref = ft.Ref[ft.Row]()
        self._busy = False
        self._sweep = ConsoleSweep(auto_start=False, accent=WARNING)
        super().__init__(
            data={"kind": "assistant_terminal", "mode": "browser_cli"}, content=self._build()
        )

    def _build(self) -> ft.Control:
        prompts = self._content.get("profile", {}).get("assistant_prompts", [])[:4]
        resume_keywords = self._content.get("resume", {}).get("keywords", [])[:6]
        return ConsolePanel(
            ft.Column(
                spacing=16,
                controls=[
                    ft.Row(
                        wrap=True,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=6,
                                controls=[
                                    ft.Text(
                                        "mauricio@cloud:~$",
                                        color=PRIMARY,
                                        size=28,
                                        font_family="DisplayBold",
                                        weight=ft.FontWeight.W_700,
                                    ),
                                    ft.Text(
                                        "Recruiter-friendly browser CLI with predefined answers, portfolio context, and arcade feedback on Enter.",
                                        color=MUTED,
                                        size=14,
                                    ),
                                ],
                            ),
                            ft.Row(
                                wrap=True,
                                spacing=8,
                                run_spacing=8,
                                controls=[
                                    SkillPill("BROWSER CLI", PRIMARY),
                                    SkillPill("STATIC SAFE", SECONDARY),
                                    SkillPill("PACMAN BOOST", PURPLE),
                                ],
                            ),
                        ],
                    ),
                    self._sweep,
                    ft.Row(
                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                        controls=[self._prefill_chip(prompt) for prompt in prompts],
                    ),
                    ft.Container(
                        border_radius=20,
                        border=ft.Border.all(1, alpha(PRIMARY, 0.18)),
                        bgcolor=alpha("#08111E", 0.88),
                        padding=ft.Padding.all(18),
                        content=ft.Column(
                            spacing=14,
                            controls=[
                                ft.ListView(
                                    ref=self._log_ref,
                                    height=360,
                                    auto_scroll=True,
                                    spacing=8,
                                    controls=[
                                        _terminal_line(text, role) for role, text in self._history
                                    ],
                                ),
                                ft.Row(
                                    ref=self._thinking_ref,
                                    visible=False,
                                    spacing=4,
                                    controls=[
                                        ft.Text(
                                            "working", color=PRIMARY, size=13, font_family="Mono"
                                        ),
                                        ft.Text(".", color=PRIMARY, size=13, font_family="Mono"),
                                        ft.Text(".", color=PRIMARY, size=13, font_family="Mono"),
                                        ft.Text(".", color=PRIMARY, size=13, font_family="Mono"),
                                    ],
                                ),
                                ft.Row(
                                    spacing=10,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            "mauricio@cloud",
                                            color=SECONDARY,
                                            size=13,
                                            font_family="Mono",
                                        ),
                                        ft.Text(":", color=MUTED, size=13, font_family="Mono"),
                                        ft.Text("~", color=PRIMARY, size=13, font_family="Mono"),
                                        ft.Text("$", color=TEXT, size=13, font_family="Mono"),
                                        ft.TextField(
                                            ref=self._input_ref,
                                            expand=True,
                                            hint_text="Ask about backend, AWS, data engineering, AI, certifications, projects, or experience",
                                            filled=False,
                                            border=ft.InputBorder.NONE,
                                            color=TEXT,
                                            cursor_color=PRIMARY,
                                            hint_style=ft.TextStyle(color=MUTED, size=13),
                                            text_style=ft.TextStyle(
                                                color=TEXT, size=14, font_family="Mono"
                                            ),
                                            on_submit=self._handle_submit,
                                            autofocus=True,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        wrap=True,
                        controls=[
                            ft.Column(
                                spacing=4,
                                controls=[
                                    ft.Text(
                                        "Prompt helpers feed the CLI, but the terminal remains the primary interaction surface.",
                                        ref=self._status_ref,
                                        color=MUTED,
                                        size=12,
                                    ),
                                    ft.Row(
                                        wrap=True,
                                        spacing=8,
                                        run_spacing=8,
                                        controls=[
                                            SkillPill(keyword, WARNING)
                                            for keyword in resume_keywords
                                        ],
                                    ),
                                ],
                            ),
                            ft.Text(
                                self._cli_command,
                                color=PRIMARY,
                                size=12,
                                font_family="Mono",
                            ),
                        ],
                    ),
                ],
            ),
            title="MauricioOS /dev/tty1",
            bgcolor=alpha("#0B1120", 0.95),
            glow=True,
        )

    def _prefill_chip(self, prompt: str) -> ft.Control:
        return attach_hover_lift(
            ft.Container(
                data={"kind": "assistant_prompt", "prompt": prompt},
                ink=True,
                border_radius=999,
                on_click=lambda _, value=prompt: self._prefill(value),
                content=ft.Container(
                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    border_radius=999,
                    bgcolor=alpha(PURPLE, 0.12),
                    border=ft.Border.all(1, alpha(PURPLE, 0.3)),
                    content=ft.Text(prompt, color=TEXT, size=12, font_family="Mono"),
                ),
            ),
            scale=1.02,
        )

    def _prefill(self, value: str) -> None:
        if self._input_ref.current:
            self._input_ref.current.value = value
            self._input_ref.current.update()
            if self._status_ref.current:
                self._status_ref.current.value = "Prompt injected into the browser terminal."
                self._status_ref.current.update()

    def _append_line(self, role: str, text: str) -> None:
        self._history.append((role, text))
        if self._log_ref.current:
            self._log_ref.current.controls.append(_terminal_line(text, role))
            self._log_ref.current.update()

    def _handle_submit(self, event: ft.ControlEvent) -> None:
        question = (event.control.value or "").strip()
        if not question or self._busy:
            return

        event.control.value = ""
        event.control.update()
        if self.page:
            self.page.run_task(self._emit_response, question)

    async def _emit_response(self, question: str) -> None:
        self._busy = True
        self._append_line("user", question)
        if self._thinking_ref.current:
            self._thinking_ref.current.visible = True
            self._thinking_ref.current.update()
        if self._status_ref.current:
            self._status_ref.current.value = "Working through predefined portfolio context..."
            self._status_ref.current.update()
        self._sweep.trigger()
        if self._on_enter_pacman:
            self._on_enter_pacman("assistant-enter")

        await asyncio.sleep(0.4)
        if self._thinking_ref.current:
            self._thinking_ref.current.visible = False
            self._thinking_ref.current.update()
        for line in build_assistant_response(question, self._content):
            self._append_line("assistant", line)
            await asyncio.sleep(0.05)

        if self._status_ref.current:
            self._status_ref.current.value = "Response emitted from local portfolio context."
            self._status_ref.current.update()
        self._busy = False


def AssistantExperienceGrid(
    content: dict[str, Any],
    *,
    on_enter_pacman: Callable[[str], None] | None = None,
) -> ft.Control:
    assistant = content.get("assistant", {})
    cli_command = assistant.get("cli_command", "uv run python -m portfolio_app.scripts.chat_cv")
    return AssistantTerminalShell(content, cli_command, on_enter_pacman=on_enter_pacman)
