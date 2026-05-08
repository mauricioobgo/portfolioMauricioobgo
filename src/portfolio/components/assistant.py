from __future__ import annotations

from collections.abc import Callable
from typing import Any

import flet as ft

from portfolio.components.cards import BentoGrid, LottiePanel, SkillPill, panel
from portfolio.components.mascots import ConsoleSweep
from portfolio.interaction import attach_hover_lift
from portfolio.theme import MUTED, PRIMARY, PURPLE, SECONDARY, TEXT, alpha


def _greeting_lines(content: dict[str, Any]) -> list[str]:
    profile = content.get("profile", {})
    prompts = profile.get("assistant_prompts", [])
    starter = (
        prompts[0] if prompts else "Ask how Mauricio builds backend, data, AI, and cloud systems."
    )
    return [
        "mauricio_ai@cloud-console ready",
        "Welcome. Thanks for dropping into the command center.",
        "This browser terminal is static-safe and runs on predefined portfolio context.",
        f"Try this: {starter}",
        "Tip: press Enter to submit and use the arrow keys to steer pacman across the arcade rail.",
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
            "The local CV assistant prep is designed so a hosted bot can be added later without exposing secrets in GitHub Pages.",
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

    return [
        "I can answer predefined questions about Mauricio's backend, data, cloud, AI, projects, certifications, and recent roles.",
        "Try one of these topics: backend summary, AWS certifications, Redshift/data engineering, AI/LLM work, or recent experience.",
        "This browser console stays static-safe; the full OpenAI-powered assistant remains available through the local CLI flow.",
    ]


def _terminal_line(text: str, role: str) -> ft.Control:
    prefixes = {
        "system": "#",
        "assistant": ">",
        "user": "$",
    }
    colors = {
        "system": SECONDARY,
        "assistant": TEXT,
        "user": PRIMARY,
    }
    prefix = prefixes.get(role, ">")
    color = colors.get(role, TEXT)
    return ft.Text(f"{prefix} {text}", color=color, size=13, font_family="Mono")


class AssistantTerminal(ft.Container):
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
        self._log_ref = ft.Ref[ft.ListView]()
        self._input_ref = ft.Ref[ft.TextField]()
        self._status_ref = ft.Ref[ft.Text]()
        self._sweep = ConsoleSweep(auto_start=False, accent=PURPLE)
        self._history: list[tuple[str, str]] = [
            ("system", line) for line in _greeting_lines(content)
        ]
        super().__init__(
            data={"kind": "assistant_terminal", "mode": "browser_cli"},
            content=self._build(),
        )

    def _build(self) -> ft.Control:
        return panel(
            ft.Column(
                spacing=14,
                controls=[
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Container(width=10, height=10, bgcolor="#FB7185", border_radius=999),
                            ft.Container(width=10, height=10, bgcolor="#F59E0B", border_radius=999),
                            ft.Container(width=10, height=10, bgcolor=SECONDARY, border_radius=999),
                            ft.Text(
                                "mauricio_ai.console", color=PRIMARY, size=12, font_family="Mono"
                            ),
                        ],
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                        controls=[
                            SkillPill("BROWSER CLI", PRIMARY),
                            SkillPill("STATIC SITE SAFE", SECONDARY),
                            SkillPill("ENTER = PACMAN BOOST", PURPLE),
                        ],
                    ),
                    self._sweep,
                    ft.ListView(
                        ref=self._log_ref,
                        height=250,
                        auto_scroll=True,
                        spacing=8,
                        controls=[_terminal_line(text, role) for role, text in self._history],
                    ),
                    ft.TextField(
                        ref=self._input_ref,
                        hint_text="Ask about backend, AWS, data engineering, AI, certifications, projects, or experience",
                        border_radius=18,
                        filled=True,
                        bgcolor=alpha("#0B1120", 0.94),
                        border_color=alpha(PRIMARY, 0.28),
                        color=TEXT,
                        cursor_color=PRIMARY,
                        hint_style=ft.TextStyle(color=MUTED, size=13),
                        text_style=ft.TextStyle(color=TEXT, size=14, font_family="Mono"),
                        on_submit=self._handle_submit,
                        autofocus=True,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        wrap=True,
                        controls=[
                            ft.Text(
                                "Warm greetings are baked in. Responses come from local portfolio context, not live network calls.",
                                ref=self._status_ref,
                                color=MUTED,
                                size=12,
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
            bgcolor=alpha("#111827", 0.94),
        )

    def _append_line(self, role: str, text: str) -> None:
        self._history.append((role, text))
        if self._log_ref.current:
            self._log_ref.current.controls.append(_terminal_line(text, role))
            self._log_ref.current.update()

    def _handle_submit(self, event: ft.ControlEvent) -> None:
        question = (event.control.value or "").strip()
        if not question:
            return

        self._append_line("user", question)
        for line in build_assistant_response(question, self._content):
            self._append_line("assistant", line)

        if self._status_ref.current:
            self._status_ref.current.value = "Response emitted from predefined portfolio context."
            self._status_ref.current.update()

        event.control.value = ""
        event.control.update()
        self._sweep.trigger()
        if self._on_enter_pacman:
            self._on_enter_pacman("assistant-enter")


def AssistantExperienceGrid(
    content: dict[str, Any],
    *,
    on_enter_pacman: Callable[[str], None] | None = None,
) -> ft.Control:
    assistant = content.get("assistant", {})
    resume = content.get("resume", {})
    prompts = content.get("profile", {}).get("assistant_prompts", [])
    cli_command = assistant.get("cli_command", "uv run python -m portfolio_app.scripts.chat_cv")
    cards = [
        attach_hover_lift(
            panel(
                ft.Column(
                    spacing=14,
                    controls=[
                        SkillPill("ASK MAURICIO AI", PRIMARY),
                        ft.Text(
                            "Interactive browser CLI",
                            color=TEXT,
                            size=24,
                            font_family="DisplayBold",
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "The public page now behaves like a terminal console: warm greeting, typed prompts, predefined responses, and pacman feedback on every Enter keypress.",
                            color=MUTED,
                            size=14,
                        ),
                        AssistantTerminal(
                            content,
                            cli_command,
                            on_enter_pacman=on_enter_pacman,
                        ),
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
                        SkillPill("PREDEFINED QUERIES", SECONDARY),
                        ft.Text(
                            resume.get("synced_at") or "Awaiting monthly sync",
                            color=TEXT,
                            size=20,
                            font_family="DisplayBold",
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "Starter topics rendered as terminal hints instead of buttons, so the experience stays CLI-first while still guiding recruiters through the strongest signals.",
                            color=MUTED,
                            size=14,
                        ),
                        ft.Column(
                            spacing=8,
                            controls=[
                                ft.Text(prompt, color=PRIMARY, size=13, font_family="Mono")
                                for prompt in prompts[:4]
                            ],
                        ),
                        ft.Row(
                            wrap=True,
                            spacing=10,
                            run_spacing=10,
                            controls=[
                                SkillPill(keyword, SECONDARY)
                                for keyword in resume.get("keywords", [])[:6]
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
            ft.Container(col={"xs": 12, "xl": 7}, content=cards[0]),
            ft.Container(col={"xs": 12, "md": 6, "xl": 3}, content=cards[1]),
            ft.Container(col={"xs": 12, "md": 6, "xl": 2}, content=cards[2]),
        ]
    )
