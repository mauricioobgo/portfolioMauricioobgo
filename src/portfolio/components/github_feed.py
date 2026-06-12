from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel
from portfolio.interaction import external_link_data, normalize_external_url
from portfolio.theme import MUTED, PRIMARY, SECONDARY, TEXT, alpha


def _activity_cells(seed: int) -> list[int]:
    cells: list[int] = []
    value = max(seed, 1)
    for index in range(7 * 26):
        value = (value * 9301 + 49297 + index * 17) % 233280
        ratio = value / 233280
        if ratio < 0.3:
            cells.append(0)
        elif ratio < 0.55:
            cells.append(1)
        elif ratio < 0.8:
            cells.append(2)
        elif ratio < 0.95:
            cells.append(3)
        else:
            cells.append(4)
    return cells


def _activity_color(level: int) -> str:
    shades = [
        alpha(SECONDARY, 0.04),
        alpha(SECONDARY, 0.2),
        alpha(SECONDARY, 0.45),
        alpha(SECONDARY, 0.7),
        alpha(SECONDARY, 1.0),
    ]
    return shades[level]


def _int_value(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def GitHubSummaryCard(summary: dict[str, Any], profile: dict[str, Any]) -> ft.Control:
    repo_count = _int_value(summary.get("repo_count"))
    followers = _int_value(profile.get("followers"))
    cells = _activity_cells(repo_count + followers)
    return ConsolePanel(
        ft.Column(
            spacing=14,
            controls=[
                ft.ResponsiveRow(
                    columns=26,
                    spacing=4,
                    run_spacing=4,
                    controls=[
                        ft.Container(
                            col=1,
                            content=ft.Container(
                                aspect_ratio=1,
                                border_radius=3,
                                border=ft.Border.all(1, alpha(TEXT, 0.1)),
                                bgcolor=_activity_color(level),
                            ),
                        )
                        for level in cells
                    ],
                ),
                ft.TextButton(
                    content=ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.CODE, color=PRIMARY, size=16),
                            ft.Text(
                                "github.com/mauricioobgo",
                                color=PRIMARY,
                                size=12,
                                font_family="Mono",
                            ),
                        ],
                    ),
                    url=normalize_external_url(profile.get("html_url")),
                    data=external_link_data("GitHub", profile.get("html_url")),
                    style=ft.ButtonStyle(padding=0),
                ),
            ],
        ),
        title="contributions @ mauricioobgo",
        padding=ft.Padding.all(20),
    )


def _repo_link_card(repo: dict[str, Any]) -> ft.Control:
    url = repo.get("github_url") or repo.get("html_url")
    return ConsolePanel(
        ft.TextButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text(
                                repo.get("category", repo.get("language", "")),
                                color=PRIMARY,
                                size=12,
                                font_family="Mono",
                            ),
                            ft.Text(
                                repo.get("name", ""),
                                color=TEXT,
                                size=16,
                                font_family="DisplayBold",
                                weight=ft.FontWeight.W_700,
                            ),
                        ],
                    ),
                    ft.Icon(ft.Icons.OPEN_IN_NEW, color=MUTED, size=16),
                ],
            ),
            url=normalize_external_url(url),
            data=external_link_data(repo.get("name", "Repository"), url),
            style=ft.ButtonStyle(padding=0),
        ),
        padding=ft.Padding.all(16),
    )


def GitHubGrid(_page: ft.Page, github: dict[str, Any]) -> ft.Control:
    summary = github.get("summary", {})
    profile = github.get("profile", {})
    repositories = github.get("repositories", [])[:3]
    return ft.ResponsiveRow(
        columns=12,
        spacing=18,
        run_spacing=18,
        controls=[
            ft.Container(col={"xs": 12, "lg": 7}, content=GitHubSummaryCard(summary, profile)),
            ft.Container(
                col={"xs": 12, "lg": 5},
                content=ft.Column(
                    spacing=12,
                    controls=[
                        _repo_link_card(repo)
                        for repo in repositories
                        if repo.get("html_url") or repo.get("github_url")
                    ],
                ),
            ),
        ],
    )
