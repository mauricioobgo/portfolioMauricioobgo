from __future__ import annotations

import asyncio
import json
from collections.abc import Callable
from datetime import datetime
from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel
from portfolio.components.mascots import ConsoleSweep
from portfolio.interaction import attach_hover_lift
from portfolio.responsive import is_mobile, is_tablet
from portfolio.theme import MUTED, PRIMARY, PURPLE, SECONDARY, TEXT, WARNING, alpha


def _assistant_prompts(content: dict[str, Any]) -> list[str]:
    profile_prompts = content.get("profile", {}).get("assistant_prompts", [])
    configured_prompts = content.get("assistant", {}).get("prompts", [])
    return (profile_prompts or configured_prompts)[:4]


def _greeting_lines(content: dict[str, Any]) -> list[str]:
    return [
        "Booting MauricioOS v3.14 ...",
        "Loading neural cores ............ [ok]",
        "Mounting /home/mauricio ......... [ok]",
        "Opening port 443 ................ [ok]",
        "",
        "Welcome to MauricioOS. Type 'help' to see available commands.",
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
        "This browser terminal stays static-safe; the full OpenAI-powered assistant remains available through the local CLI flow.",
    ]


def _execute_terminal_command(
    command: str,
    content: dict[str, Any],
    command_history: list[str],
) -> tuple[list[str], str | None]:
    normalized = command.strip()
    parts = normalized.split()
    head = parts[0].lower() if parts else ""
    arg = " ".join(parts[1:])
    profile = content.get("profile", {})
    profile_links = profile.get("links", {})
    projects = content.get("featured_projects", [])
    certifications = content.get("certifications", [])
    stack = content.get("technical_stack", [])
    github = content.get("github", {})

    if head == "clear":
        return [], "clear"
    if head == "matrix":
        return ["Wake up, Neo ...", "the matrix has you."], "matrix"
    if head == "help":
        return [
            "available commands:",
            "  help                show this help",
            "  whoami              -> mauricio",
            "  hostname / host     -> mauricio",
            "  uname -a            kernel info",
            "  pwd                 print working directory",
            "  ls                  list home directory",
            "  cat <file>          about.md | skills.json | contact.vcf",
            "  experience          work history",
            "  projects [name]     featured projects",
            "  certifications      validated credentials",
            "  stack               tooling i reach for",
            "  ai                  llm / agent work",
            "  github              github profile + repos",
            "  resume / cv         open the resume link",
            "  open <target>       github | linkedin | resume",
            "  date                current date",
            "  echo <text>         echo arguments",
            "  history             command history",
            "  clear               clear scrollback",
            "  matrix              ENTER THE MATRIX",
        ], None
    if head == "whoami":
        return ["mauricio"], None
    if head in {"hostname", "host"}:
        return ["mauricio"], None
    if normalized.lower() == "uname -a":
        return ["MauricioOS 3.14 #1 SMP cloud-native x86_64 GNU/Engineer"], None
    if head == "pwd":
        return ["/home/mauricio"], None
    if head == "ls":
        return [
            "about.md   experience/   projects/   skills.json   certifications/   contact.vcf   resume.pdf"
        ], None
    if head == "cat" and arg == "about.md":
        return [profile.get("about", profile.get("bio", "Portfolio profile unavailable."))], None
    if head == "cat" and arg == "skills.json":
        return json.dumps({"skills": profile.get("skills", [])}, indent=2).splitlines(), None
    if head == "cat" and arg == "contact.vcf":
        return [
            "BEGIN:VCARD",
            f"FN:{profile.get('name', 'Mauricio Obando')}",
            f"EMAIL:{profile.get('email', 'mauricioobgo@gmail.com')}",
            f"URL:{profile.get('linkedin_url', profile_links.get('linkedin', profile.get('linkedin', '')))}",
            f"URL:{profile.get('github_url', profile_links.get('github', github.get('profile', {}).get('html_url', '')))}",
            "END:VCARD",
        ], None
    if head == "cat":
        return [f"cat: {arg or 'missing operand'}: no such file"], None
    if head == "projects":
        if arg and arg != "--list":
            project = next(
                (item for item in projects if arg.lower() in item.get("name", "").lower()),
                None,
            )
            if project is None:
                return [f"projects: {arg} not found"], None
            lines = [
                project.get("name", "Project"),
                project.get("summary", ""),
                f"stack: {', '.join(project.get('tech_stack', [])[:6])}",
            ]
            if project.get("github_url"):
                lines.append(f"repo: {project.get('github_url')}")
            return lines, None
        return [
            f"- {project.get('name', 'Project')} - {project.get('summary', '')}"
            for project in projects[:5]
        ], None
    if head == "certifications":
        return [
            f"* {cert.get('title', 'Certification')} ({cert.get('issuer', '')})"
            for cert in certifications[:5]
        ], None
    if head == "stack":
        return [
            f"{group.get('name', 'stack')}: {', '.join(group.get('items', [])[:6])}"
            for group in stack[:4]
        ], None
    if head == "ai":
        return [
            "applied LLM systems:",
            "- HL7 healthcare agent - parsing, classification, tool calling",
            "- AI DataOps platform - RAG over governed datasets",
            "- Resume and CV assistant - retrieval over personal context",
        ], None
    if head == "github":
        summary = github.get("summary", {})
        return [
            github.get("profile", {}).get("html_url", "https://github.com/mauricioobgo"),
            f"public repos: {summary.get('repo_count', 0)}",
        ], None
    if head in {"resume", "cv"}:
        resume_link = profile.get("resume_link", "")
        if resume_link:
            return [f"opening resume: {resume_link}"], f"open:{resume_link}"
        return ["Resume link unavailable."], None
    if head == "open":
        targets = {
            "github": profile.get(
                "github_url",
                profile_links.get("github", github.get("profile", {}).get("html_url", "")),
            ),
            "linkedin": profile.get(
                "linkedin_url", profile_links.get("linkedin", profile.get("linkedin", ""))
            ),
            "resume": profile.get("resume_link", ""),
            "cv": profile.get("resume_link", ""),
        }
        target = arg.lower()
        url = targets.get(target, arg if arg.startswith(("https://", "http://")) else "")
        if url:
            return [f"opening {target or 'url'}: {url}"], f"open:{url}"
        return ["open: expected github, linkedin, resume, or https:// URL"], None
    if head == "contact":
        return [
            profile.get("email", "mauricioobgo@gmail.com"),
            profile.get(
                "github_url", profile_links.get("github", "https://github.com/mauricioobgo")
            ),
            profile.get("linkedin_url", profile_links.get("linkedin", profile.get("linkedin", ""))),
        ], None
    if head == "experience":
        return _latest_role_lines(content), None
    if head == "date":
        return [datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")], None
    if head == "echo":
        return [arg], None
    if head == "history":
        return command_history[-8:] or ["No previous commands yet."], None
    if head == "coffee":
        return [
            "      ( (",
            "       ) )",
            "    ........",
            "    |      |]",
            "    \\      /",
            "     `----'",
            "brewing ...",
        ], None
    if head == "sudo":
        return ["permission denied. nice try."], None
    if head == "exit":
        return ["nice try. you live here now."], None

    return build_assistant_response(normalized, content), None


def _terminal_line(text: str, role: str) -> ft.Control:
    if not text:
        return ft.Container(height=6)
    prefixes = {"system": "#", "assistant": ">", "user": "$"}
    colors = {"system": SECONDARY, "assistant": TEXT, "user": PRIMARY}
    accent = colors.get(role, TEXT)
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=10, vertical=6),
        border_radius=10,
        bgcolor=alpha(accent, 0.055 if role != "user" else 0.09),
        content=ft.Row(
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Text(
                    prefixes.get(role, ">"),
                    color=accent,
                    size=13,
                    font_family="Mono",
                    weight=ft.FontWeight.W_700,
                ),
                ft.Text(
                    text,
                    color=colors.get(role, TEXT),
                    size=13,
                    font_family="Mono",
                    selectable=True,
                    expand=True,
                ),
            ],
        ),
    )


def _terminal_chip(label: str, color: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=10, vertical=5),
        border_radius=999,
        bgcolor=alpha(color, 0.11),
        border=ft.Border.all(1, alpha(color, 0.28)),
        content=ft.Text(label, color=color, size=11, font_family="Mono"),
    )


class PortfolioTerminalShell(ft.Container):
    def __init__(self, page: ft.Page, content: dict[str, Any], cli_command: str) -> None:
        self._page = page
        self._content = content
        self._cli_command = cli_command
        self._command_history: list[str] = []
        self._history: list[tuple[str, str]] = [
            ("system", line) for line in _greeting_lines(content)
        ]
        self._log_ref = ft.Ref[ft.ListView]()
        self._input_ref = ft.Ref[ft.TextField]()
        self._status_ref = ft.Ref[ft.Text]()
        self._thinking_ref = ft.Ref[ft.Row]()
        self._matrix_ref = ft.Ref[ft.Container]()
        self._busy = False
        self._sweep = ConsoleSweep(auto_start=False, accent=WARNING)
        super().__init__(
            data={"kind": "terminal_shell", "mode": "browser_cli"}, content=self._build()
        )

    def _log_height(self, page_width: float | int | None = None) -> int:
        target = page_width if page_width is not None else self._page
        if is_mobile(target):
            return 320
        if is_tablet(target):
            return 360
        return 440

    def _build(self) -> ft.Control:
        quick_commands = ["help", "projects", "stack", "github", "resume"]
        input_bar = ft.Container(
            padding=ft.Padding.symmetric(horizontal=12, vertical=4),
            border_radius=14,
            bgcolor=alpha("#020617", 0.78),
            border=ft.Border.all(1, alpha(PRIMARY, 0.22)),
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "mauricio@cloud",
                        color=SECONDARY,
                        size=13,
                        font_family="Mono",
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(":~$", color=PRIMARY, size=13, font_family="Mono"),
                    ft.TextField(
                        ref=self._input_ref,
                        expand=True,
                        hint_text="Try help, projects redshift, open github, matrix...",
                        filled=False,
                        border=ft.InputBorder.NONE,
                        color=TEXT,
                        cursor_color=PRIMARY,
                        hint_style=ft.TextStyle(color=MUTED, size=13),
                        text_style=ft.TextStyle(color=TEXT, size=14, font_family="Mono"),
                        on_submit=self._handle_submit,
                        autofocus=True,
                    ),
                ],
            ),
        )
        terminal_body = ft.Container(
            border_radius=20,
            border=ft.Border.all(1, alpha(PRIMARY, 0.22)),
            bgcolor=alpha("#08111E", 0.92),
            padding=ft.Padding.all(18),
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        wrap=True,
                        controls=[
                            ft.Row(
                                spacing=8,
                                wrap=True,
                                controls=[
                                    _terminal_chip("STATIC-SAFE", SECONDARY),
                                    _terminal_chip("LOCAL CONTEXT", PRIMARY),
                                    _terminal_chip("NO API KEY", WARNING),
                                ],
                            ),
                            ft.Text(
                                "enter runs command • links open in a new tab",
                                color=MUTED,
                                size=12,
                                font_family="Mono",
                            ),
                        ],
                    ),
                    ft.ListView(
                        ref=self._log_ref,
                        height=self._log_height(),
                        auto_scroll=True,
                        spacing=8,
                        controls=[_terminal_line(text, role) for role, text in self._history],
                    ),
                    ft.Row(
                        ref=self._thinking_ref,
                        visible=False,
                        spacing=4,
                        controls=[
                            ft.ProgressRing(width=14, height=14, stroke_width=2, color=PRIMARY),
                            ft.Text("working", color=PRIMARY, size=13, font_family="Mono"),
                        ],
                    ),
                    ft.Row(
                        spacing=8,
                        wrap=True,
                        controls=[
                            ft.TextButton(
                                content=command,
                                icon=ft.Icons.TERMINAL,
                                style=ft.ButtonStyle(color=PRIMARY),
                                on_click=lambda _, value=command: self._submit_command(value),
                            )
                            for command in quick_commands
                        ],
                    ),
                    input_bar,
                ],
            ),
        )
        matrix_overlay = ft.Container(
            ref=self._matrix_ref,
            visible=False,
            border_radius=20,
            bgcolor=alpha("#03140B", 0.88),
            padding=ft.Padding.all(24),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.CODE, color=SECONDARY, size=42),
                    ft.Text(
                        "Wake up, Neo ...",
                        color=SECONDARY,
                        size=28,
                        font_family="Mono",
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(
                        "the matrix has you.",
                        color=SECONDARY,
                        size=14,
                        font_family="Mono",
                    ),
                ],
            ),
        )
        return ConsolePanel(
            ft.Column(
                spacing=16,
                controls=[
                    self._sweep,
                    ft.Stack(controls=[terminal_body, matrix_overlay]),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        wrap=True,
                        controls=[
                            ft.Text(
                                "Terminal ready. Quick commands, AI cards, and shell input share one router.",
                                ref=self._status_ref,
                                color=MUTED,
                                size=12,
                            ),
                            ft.Text(
                                self._cli_command,
                                color=PRIMARY,
                                size=12,
                                font_family="Mono",
                                selectable=True,
                            ),
                        ],
                    ),
                ],
            ),
            title="MauricioOS /dev/tty1",
            bgcolor=alpha("#0B1120", 0.95),
            glow=True,
        )

    def sync_layout(self, page_width: float | int | None) -> None:
        if self._log_ref.current:
            self._log_ref.current.height = self._log_height(page_width)
            self._log_ref.current.update()

    def prefill(self, prompt: str) -> None:
        if self._input_ref.current:
            self._input_ref.current.value = prompt
            self._input_ref.current.update()
        if self._status_ref.current:
            self._status_ref.current.value = "Prompt injected from the AI command deck."
            self._status_ref.current.update()

    def _append_line(self, role: str, text: str) -> None:
        self._history.append((role, text))
        if self._log_ref.current:
            self._log_ref.current.controls.append(_terminal_line(text, role))
            self._log_ref.current.update()

    def _clear_history(self) -> None:
        self._history = []
        if self._log_ref.current:
            self._log_ref.current.controls = []
            self._log_ref.current.update()

    def _submit_command(self, command: str) -> None:
        question = command.strip()
        if not question or self._busy:
            return
        if self._input_ref.current:
            self._input_ref.current.value = ""
            self._input_ref.current.update()
        if self.page:
            self.page.run_task(self._emit_response, question)

    def _handle_submit(self, event: ft.ControlEvent) -> None:
        question = (event.control.value or "").strip()
        if not question or self._busy:
            return

        event.control.value = ""
        event.control.update()
        self._submit_command(question)

    async def _emit_response(self, question: str) -> None:
        self._busy = True
        self._command_history.append(question)
        self._append_line("user", question)
        if self._thinking_ref.current:
            self._thinking_ref.current.visible = True
            self._thinking_ref.current.update()
        if self._status_ref.current:
            self._status_ref.current.value = "Working through predefined portfolio context..."
            self._status_ref.current.update()
        self._sweep.trigger()

        await asyncio.sleep(0.3)
        if self._thinking_ref.current:
            self._thinking_ref.current.visible = False
            self._thinking_ref.current.update()

        lines, action = _execute_terminal_command(question, self._content, self._command_history)
        if action == "clear":
            self._clear_history()
        for line in lines:
            self._append_line("assistant", line)
            await asyncio.sleep(0.05)

        if action == "matrix" and self._matrix_ref.current:
            self._matrix_ref.current.visible = True
            self._matrix_ref.current.update()
            await asyncio.sleep(1.8)
            self._matrix_ref.current.visible = False
            self._matrix_ref.current.update()
        elif action and action.startswith("open:") and self.page:
            self.page.launch_url(action.removeprefix("open:"))

        if self._status_ref.current:
            self._status_ref.current.value = "Response emitted from local portfolio context."
            self._status_ref.current.update()
        self._busy = False


def _ai_prompt_card(prompt: str, on_prompt: Callable[[str], None]) -> ft.Control:
    return attach_hover_lift(
        ft.Container(
            data={"kind": "assistant_prompt", "prompt": prompt},
            ink=True,
            border_radius=20,
            on_click=lambda _, value=prompt: on_prompt(value),
            content=ConsolePanel(
                ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("$ ask", color=PURPLE, size=12, font_family="Mono"),
                        ft.Text(prompt, color=TEXT, size=16),
                    ],
                ),
                padding=ft.Padding.all(18),
                bgcolor=alpha("#0B1120", 0.95),
            ),
        ),
        scale=1.02,
    )


def AICommandDeck(
    _page: ft.Page,
    content: dict[str, Any],
    *,
    on_prompt: Callable[[str], None],
) -> ft.Control:
    prompts = _assistant_prompts(content)
    return ft.ResponsiveRow(
        columns=12,
        spacing=14,
        run_spacing=14,
        controls=[
            ft.Container(
                col={"xs": 12, "md": 6},
                content=_ai_prompt_card(prompt, on_prompt),
            )
            for prompt in prompts
        ],
    )


def build_terminal_shell(page: ft.Page, content: dict[str, Any]) -> PortfolioTerminalShell:
    assistant = content.get("assistant", {})
    cli_command = assistant.get("cli_command", "uv run python -m portfolio_app.scripts.chat_cv")
    return PortfolioTerminalShell(page, content, cli_command)
