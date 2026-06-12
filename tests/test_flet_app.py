from types import SimpleNamespace

import flet as ft

from portfolio.app import build_portfolio_view
from portfolio.components.ambient import ScrollProgressOverlay
from portfolio.components.assistant import build_assistant_response
from portfolio.components.github_feed import GitHubSummaryCard
from portfolio.components.projects import project_matches
from portfolio_app.services.content import build_portfolio_content


class _FakePage(SimpleNamespace):
    def scroll_to(self, **kwargs) -> None:
        return None

    def launch_url(self, url: str | None) -> None:
        return None


def test_build_portfolio_view_builds_from_generated_content() -> None:
    page = _FakePage(width=1440)
    content = build_portfolio_content()

    view = build_portfolio_view(page, content)

    assert isinstance(view, ft.Control)


def _walk(control: ft.Control):
    yield control
    for attribute in ("content", "leading", "title", "subtitle", "trailing"):
        child = getattr(control, attribute, None)
        if isinstance(child, ft.Control):
            yield from _walk(child)
    controls = getattr(control, "controls", None)
    if isinstance(controls, list):
        for child in controls:
            if isinstance(child, ft.Control):
                yield from _walk(child)


def test_view_exposes_bound_links_and_interactive_controls() -> None:
    page = _FakePage(width=1440)
    content = build_portfolio_content()

    view = build_portfolio_view(page, content)
    controls = list(_walk(view))

    external_links = [
        control.data
        for control in controls
        if isinstance(getattr(control, "data", None), dict)
        and control.data.get("kind") == "external_link"
    ]
    section_links = [
        control.data
        for control in controls
        if isinstance(getattr(control, "data", None), dict)
        and control.data.get("kind") == "section_link"
    ]
    terminal_shells = [
        control.data
        for control in controls
        if isinstance(getattr(control, "data", None), dict)
        and control.data.get("kind") == "terminal_shell"
    ]
    assistant_prompts = [
        control.data
        for control in controls
        if isinstance(getattr(control, "data", None), dict)
        and control.data.get("kind") == "assistant_prompt"
    ]
    scroll_progress = [
        control.data
        for control in controls
        if isinstance(getattr(control, "data", None), dict)
        and control.data.get("kind") == "scroll_progress"
    ]
    hero_console = [
        control.data
        for control in controls
        if isinstance(getattr(control, "data", None), dict)
        and control.data.get("kind") == "hero_console"
    ]
    role_typers = [
        control.data
        for control in controls
        if isinstance(getattr(control, "data", None), dict)
        and control.data.get("kind") == "role_typer"
    ]
    hero_metrics = [
        control.data
        for control in controls
        if isinstance(getattr(control, "data", None), dict)
        and control.data.get("kind") == "hero_metric"
    ]
    certification_cards = [
        control.data
        for control in controls
        if isinstance(getattr(control, "data", None), dict)
        and control.data.get("kind") == "certification_card"
    ]

    required_external_labels = {"GitHub", "LinkedIn", "Download Resume", "Email"}
    found_labels = {item["label"] for item in external_links if item.get("valid")}
    assert required_external_labels <= found_labels
    assert any(item["target"] == "projects" for item in section_links)
    assert any(item["target"] == "terminal" for item in section_links)
    assert any(item["target"] == "ai" for item in section_links)
    assert terminal_shells
    assert assistant_prompts
    assert scroll_progress
    assert hero_console
    assert role_typers
    assert len(hero_metrics) == 4
    assert len(certification_cards) >= 2

    ordered_keys = [
        getattr(control, "key", None) for control in controls if getattr(control, "key", None)
    ]
    assert ordered_keys.index("experience") < ordered_keys.index("terminal")
    assert ordered_keys.index("terminal") < ordered_keys.index("certifications")
    assert ordered_keys.index("github") < ordered_keys.index("ai")
    assert ordered_keys.index("ai") < ordered_keys.index("stack")

    kinds = [
        item.get("kind")
        for item in (getattr(control, "data", None) for control in controls)
        if isinstance(item, dict)
    ]
    assert "arcade_rail" not in kinds
    assert "border_pacman" not in kinds
    assert "hero_arcade_maze" not in kinds
    assert "project_filter" not in kinds


def test_github_summary_card_tolerates_missing_profile_counts() -> None:
    summary = {"repo_count": 12, "top_starred": None, "language_breakdown": []}
    profile = {"followers": None, "html_url": "https://github.com/mauricioobgo"}

    card = GitHubSummaryCard(summary, profile)

    assert isinstance(card, ft.Control)


def test_scroll_progress_overlay_tracks_scroll_fraction() -> None:
    overlay = ScrollProgressOverlay()

    overlay.sync(pixels=0, max_scroll=1000, width=1440, height=900)
    assert overlay.progress == 0

    overlay.sync(pixels=500, max_scroll=1000, width=1440, height=900)
    assert overlay.progress == 0.5

    overlay.sync(pixels=5000, max_scroll=1000, width=1440, height=900)
    assert overlay.progress == 1


def test_project_filter_logic_matches_declared_filters() -> None:
    project = {"filters": ["Backend", "AWS", "FastAPI"]}

    assert project_matches(project, "All")
    assert project_matches(project, "Backend")
    assert not project_matches(project, "LLM")


def test_assistant_cli_uses_predefined_certification_response() -> None:
    content = build_portfolio_content()

    lines = build_assistant_response("Tell me about AWS certifications", content)

    assert any("Solutions Architect - Professional" in line for line in lines)
    assert any("Machine Learning - Specialty" in line for line in lines)
