from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel, SkillPill, link_button
from portfolio.interaction import attach_hover_lift, external_link_data, normalize_external_url
from portfolio.theme import MUTED, PRIMARY, SECONDARY, TEXT, WARNING, alpha


def _activity_cells(seed: int) -> list[int]:
    cells: list[int] = []
    value = max(seed, 1)
    for index in range(7 * 26):
        value = (value * 9301 + 49297 + index * 17) % 233280
        ratio = value / 233280
        if ratio < 0.28:
            cells.append(0)
        elif ratio < 0.52:
            cells.append(1)
        elif ratio < 0.76:
            cells.append(2)
        elif ratio < 0.92:
            cells.append(3)
        else:
            cells.append(4)
    return cells


def _activity_color(level: int) -> str:
    if level == 0:
        return alpha("#0F172A", 0.0)
    if level == 1:
        return alpha(SECONDARY, 0.22)
    if level == 2:
        return alpha(SECONDARY, 0.42)
    if level == 3:
        return alpha(SECONDARY, 0.64)
    return alpha(SECONDARY, 0.9)


def GitHubRepoCard(_page: ft.Page, repo: dict[str, Any]) -> ft.Control:
    topics = repo.get("topics", [])[:3]
    links = [link_button("Repository", repo.get("html_url", ""))]
    if repo.get("homepage"):
        links.append(link_button("Homepage", repo.get("homepage", ""), accent=SECONDARY))

    return attach_hover_lift(
        ConsolePanel(
            ft.Column(
                spacing=12,
                controls=[
                    ft.TextButton(
                        content=ft.Text(
                            repo.get("name", ""),
                            color=TEXT,
                            size=20,
                            font_family="DisplayBold",
                            weight=ft.FontWeight.W_700,
                        ),
                        url=normalize_external_url(repo.get("html_url")),
                        data=external_link_data(
                            repo.get("name", "Repository"), repo.get("html_url")
                        ),
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
                    ft.Row(wrap=True, spacing=10, run_spacing=10, controls=links),
                ],
            ),
            title=repo.get("full_name", repo.get("name", "github://repo")),
            bgcolor="#111827",
        ),
        scale=1.02,
    )


def GitHubSummaryCard(summary: dict[str, Any], profile: dict[str, Any]) -> ft.Control:
    language_breakdown = summary.get("language_breakdown", [])[:5]
    cells = _activity_cells(summary.get("repo_count", 0) + profile.get("followers", 0))
    heatmap = [
        ft.Container(
            width=11,
            height=11,
            border_radius=3,
            border=ft.Border.all(1, alpha("#1E293B", 0.85)),
            bgcolor=_activity_color(level),
        )
        for level in cells
    ]
    return attach_hover_lift(
        ConsolePanel(
            ft.Column(
                spacing=14,
                controls=[
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
                    ft.ResponsiveRow(
                        columns=26,
                        spacing=4,
                        run_spacing=4,
                        controls=[ft.Container(col=1, content=cell) for cell in heatmap],
                    ),
                    ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                f"{item['name']}: {item['count']} repos",
                                color=MUTED,
                                size=13,
                                font_family="Mono",
                            )
                            for item in language_breakdown
                        ],
                    ),
                    link_button("Open GitHub profile", profile.get("html_url", ""), accent=PRIMARY),
                ],
            ),
            title="contributions @ mauricioobgo",
            glow=True,
            bgcolor="#0F172A",
        ),
        scale=1.02,
    )


def GitHubGrid(page: ft.Page, github: dict[str, Any]) -> ft.Control:
    repositories = github.get("repositories", [])[:3]
    summary = github.get("summary", {})
    profile = github.get("profile", {})
    return ft.ResponsiveRow(
        columns=12,
        spacing=18,
        run_spacing=18,
        controls=[
            ft.Container(
                col={"xs": 12, "xl": 7},
                content=GitHubSummaryCard(summary, profile),
            ),
            ft.Container(
                col={"xs": 12, "xl": 5},
                content=ft.Column(
                    spacing=12,
                    controls=[GitHubRepoCard(page, repo) for repo in repositories],
                ),
            ),
        ],
    )
