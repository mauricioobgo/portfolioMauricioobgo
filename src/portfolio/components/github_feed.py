from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import BentoGrid, SkillPill
from portfolio.theme import MUTED, PRIMARY, SECONDARY, TEXT, WARNING, panel


def GitHubRepoCard(page: ft.Page, repo: dict[str, Any]) -> ft.Control:
    topics = repo.get("topics", [])[:3]
    return panel(
        ft.Column(
            spacing=12,
            controls=[
                ft.TextButton(
                    content=ft.Text(
                        repo.get("name", ""),
                        color=TEXT,
                        size=21,
                        font_family="DisplayBold",
                        weight=ft.FontWeight.W_700,
                    ),
                    on_click=lambda _: page.launch_url(repo.get("html_url")),
                ),
                ft.Text(
                    repo.get("description") or "Repository activity synced from GitHub.",
                    color=MUTED,
                    size=14,
                ),
                ft.Row(
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                    controls=[
                        SkillPill(repo.get("language", "Code"), PRIMARY),
                        SkillPill(f"Stars {repo.get('stargazers_count', 0)}", WARNING),
                        SkillPill(f"Forks {repo.get('forks_count', 0)}", SECONDARY),
                    ],
                ),
                ft.Row(
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                    controls=[SkillPill(topic, "#A855F7") for topic in topics],
                ),
            ],
        )
    )


def GitHubSummaryCard(summary: dict[str, Any], profile: dict[str, Any]) -> ft.Control:
    language_breakdown = summary.get("language_breakdown", [])[:5]
    return panel(
        ft.Column(
            spacing=14,
            controls=[
                ft.Text(
                    "GitHub signal",
                    color=TEXT,
                    size=22,
                    font_family="DisplayBold",
                    weight=ft.FontWeight.W_700,
                ),
                ft.Row(
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                    controls=[
                        SkillPill(f"Repos {summary.get('repo_count', 0)}", PRIMARY),
                        SkillPill(f"Followers {profile.get('followers', 0)}", SECONDARY),
                        SkillPill(f"Top stars {summary.get('top_starred', 0)}", WARNING),
                    ],
                ),
                ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text(
                            f"{item['name']}: {item['count']} repos",
                            color=MUTED,
                            size=14,
                            font_family="Mono",
                        )
                        for item in language_breakdown
                    ],
                ),
            ],
        )
    )


def GitHubGrid(page: ft.Page, github: dict[str, Any]) -> ft.Control:
    repositories = github.get("repositories", [])[:6]
    summary = github.get("summary", {})
    profile = github.get("profile", {})
    return BentoGrid(
        [
            ft.Container(
                col={"xs": 12, "md": 6, "xl": 4},
                content=GitHubSummaryCard(summary, profile),
            ),
            *[
                ft.Container(
                    col={"xs": 12, "md": 6, "xl": 4},
                    content=GitHubRepoCard(page, repo),
                )
                for repo in repositories
            ],
        ]
    )
