from __future__ import annotations

import re
from datetime import datetime

import reflex as rx

from portfolio_app.components.sections import section
from portfolio_app.services.content import load_portfolio_content


LINKEDIN_PROFILE_URL = "https://www.linkedin.com/in/mauricioobgo/"
LINKEDIN_EXPERIENCE_URL = "https://www.linkedin.com/in/mauricioobgo/details/experience/"
LINKEDIN_CERTIFICATIONS_URL = "https://www.linkedin.com/in/mauricioobgo/details/certifications/"


def _format_refresh(refresh_log: dict) -> str:
    executed_at = refresh_log.get("executed_at")
    scope = refresh_log.get("scope", "manual")
    if not executed_at:
        return "Refresh state unavailable"

    try:
        parsed = datetime.fromisoformat(executed_at.replace("Z", "+00:00"))
        stamp = parsed.strftime("%b %d, %Y")
    except ValueError:
        stamp = executed_at

    return f"{scope.upper()} refresh // {stamp}"


def _format_repo_date(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.strftime("%b %d, %Y")
    except ValueError:
        return value


def _estimate_years(experience: list[dict]) -> str:
    if not experience:
        return "n/a"

    latest_match = re.search(r"(20\d{2})", experience[-1].get("date", ""))
    if not latest_match:
        return "7+ years"

    start_year = int(latest_match.group(1))
    years = max(datetime.now().year - start_year, 1)
    return f"{years}+ years"


def _command_pill(value: str) -> rx.Component:
    return rx.box(value, class_name="command-pill")


def _terminal_button(label: str, href: str, *, primary: bool = False) -> rx.Component:
    return rx.link(
        label,
        href=href,
        is_external=True,
        class_name="action-primary" if primary else "action-secondary",
    )


def _metric_card(label: str, value: str, detail: str) -> rx.Component:
    return rx.box(
        rx.text(label, class_name="metric-label"),
        rx.heading(value, size="6", class_name="metric-value"),
        rx.text(detail, class_name="metric-detail"),
        class_name="metric-card",
    )


def _flow_card(title: str, detail: str) -> rx.Component:
    return rx.box(
        rx.text(title, class_name="flow-title"),
        rx.text(detail, class_name="flow-copy"),
        class_name="flow-card",
    )


def _hero(
    profile: dict,
    generated_profile: dict,
    refresh_log: dict,
    experience: list[dict],
    certifications: list[dict],
    generated_repos: list[dict],
) -> rx.Component:
    social_links = profile["social_links"]
    refresh_copy = _format_refresh(refresh_log)
    avatar_url = generated_profile.get("avatar_url")
    location = generated_profile.get("location", "Bogota, Colombia")
    current_company = experience[0]["company"] if experience else "Available on LinkedIn"

    metrics = [
        (
            "current node",
            current_company,
            experience[0].get("date", "latest profile snapshot")
            if experience
            else "latest profile snapshot",
        ),
        ("career span", _estimate_years(experience), "data and cloud delivery"),
        ("cert signals", str(len(certifications)), "LinkedIn-backed credentials"),
        ("repo feed", str(len(generated_repos[:6])), refresh_copy),
    ]

    return rx.box(
        rx.box(class_name="hero-grid-overlay"),
        rx.flex(
            rx.vstack(
                rx.text("AI PORTFOLIO // LIVE PROFILE", class_name="hero-eyebrow"),
                rx.heading(profile["name"], size="9", class_name="hero-name"),
                rx.text(profile["title"], class_name="hero-title"),
                rx.text(profile["subtitle"], class_name="hero-subtitle"),
                rx.text(profile["about"], class_name="hero-about"),
                rx.flex(
                    *[_command_pill(skill) for skill in profile["skills"]],
                    wrap="wrap",
                    gap="0.7rem",
                    width="100%",
                ),
                rx.flex(
                    _terminal_button("View resume", profile["resume_link"], primary=True),
                    _terminal_button("Open LinkedIn", social_links["linkedin"]),
                    _terminal_button("GitHub", social_links["github"]),
                    wrap="wrap",
                    gap="0.8rem",
                    width="100%",
                ),
                rx.flex(
                    rx.text(f"mail // {profile['email']}", class_name="hero-meta"),
                    rx.text(f"location // {location}", class_name="hero-meta"),
                    rx.text(refresh_copy, class_name="hero-meta"),
                    wrap="wrap",
                    gap="0.8rem",
                    width="100%",
                ),
                align="start",
                spacing="5",
                width="100%",
                class_name="hero-copy",
            ),
            rx.vstack(
                *[_metric_card(label, value, detail) for label, value, detail in metrics],
                *(
                    [
                        rx.box(
                            rx.image(
                                src=avatar_url,
                                alt=f"{profile['name']} avatar",
                                width="100%",
                                height="100%",
                                object_fit="cover",
                            ),
                            class_name="avatar-shell",
                        )
                    ]
                    if avatar_url
                    else []
                ),
                width=["100%", "100%", "360px"],
                spacing="4",
                align="stretch",
            ),
            width="100%",
            justify="between",
            align="start",
            gap="1.2rem",
            wrap="wrap",
        ),
        rx.flex(
            _flow_card(
                "AI mode",
                "Practical LLM workflows, automation, and shipping-focused experimentation.",
            ),
            _flow_card(
                "Data systems",
                "Batch and analytics pipelines shaped for cloud-native scale and reliability.",
            ),
            _flow_card(
                "Flow design",
                "Terminal texture, bento rhythm, and connective lines inspired by current AI dashboard patterns.",
            ),
            wrap="wrap",
            gap="1rem",
            width="100%",
        ),
        class_name="hero-shell",
    )


def _experience_card(item: dict) -> rx.Component:
    links: list[rx.Component] = []
    if item.get("company_url"):
        links.append(_terminal_button("Company", item["company_url"]))
    if item.get("reference_url"):
        links.append(
            _terminal_button(
                item.get("reference_label", "LinkedIn"),
                item["reference_url"],
            )
        )

    return rx.box(
        rx.text(item["date"], class_name="timeline-date"),
        rx.flex(
            rx.vstack(
                rx.heading(item["role"], size="5", class_name="timeline-title"),
                rx.text(item["company"], class_name="timeline-company"),
                *(
                    [rx.text(item["location"], class_name="timeline-location")]
                    if item.get("location")
                    else []
                ),
                align="start",
                spacing="1",
            ),
            width="100%",
            justify="between",
            align="start",
            wrap="wrap",
            gap="0.8rem",
        ),
        rx.text(item["description"], class_name="timeline-copy"),
        rx.vstack(
            *[
                rx.flex(
                    rx.text("> ", class_name="timeline-marker"),
                    rx.text(highlight, class_name="timeline-highlight"),
                    gap="0.2rem",
                    align="start",
                )
                for highlight in item.get("highlights", [])
            ],
            spacing="2",
            align="stretch",
            width="100%",
        ),
        *(
            [
                rx.flex(
                    *links,
                    wrap="wrap",
                    gap="0.8rem",
                    width="100%",
                )
            ]
            if links
            else []
        ),
        class_name="timeline-card",
    )


def _experience_section(experience: list[dict]) -> rx.Component:
    return section(
        "Latest Experience Log",
        *[_experience_card(item) for item in experience],
        eyebrow="career timeline",
        subtitle="Three most recent experience nodes, aligned to the current LinkedIn and resume snapshot.",
        action_label="Open full LinkedIn experience",
        action_url=LINKEDIN_EXPERIENCE_URL,
    )


def _project_card(item: dict) -> rx.Component:
    return rx.box(
        rx.text("featured build", class_name="project-label"),
        rx.heading(item["name"], size="5", class_name="project-title"),
        rx.text(item["summary"], class_name="project-copy"),
        class_name="project-card",
    )


def _project_grid(title: str, items: list[dict], empty_state: str) -> rx.Component:
    body: list[rx.Component]
    if items:
        body = [
            rx.flex(
                *[_project_card(item) for item in items],
                wrap="wrap",
                gap="1rem",
                width="100%",
            )
        ]
    else:
        body = [rx.text(empty_state, class_name="empty-copy")]

    return section(
        title,
        *body,
        eyebrow="selected systems",
        subtitle="Curated delivery highlights with product, analytics, and platform emphasis.",
    )


def _repo_card(repo: dict) -> rx.Component:
    stars = repo.get("stargazers_count", 0)
    updated_at = repo.get("updated_at")

    return rx.box(
        rx.flex(
            rx.text("live repo", class_name="repo-label"),
            rx.text(f"stars // {stars}", class_name="repo-meta"),
            width="100%",
            justify="between",
            align="center",
            wrap="wrap",
            gap="0.6rem",
        ),
        rx.heading(repo["name"], size="5", class_name="repo-title"),
        rx.text(
            repo.get("description") or "Recently updated GitHub repository.",
            class_name="repo-copy",
        ),
        *(
            [rx.text(f"updated // {_format_repo_date(updated_at)}", class_name="repo-meta")]
            if updated_at
            else []
        ),
        _terminal_button("Open repository", repo["html_url"]),
        class_name="repo-card",
    )


def _repo_section(generated_repos: list[dict]) -> rx.Component:
    if generated_repos:
        body = [
            rx.flex(
                *[_repo_card(repo) for repo in generated_repos[:6]],
                wrap="wrap",
                gap="1rem",
                width="100%",
            )
        ]
    else:
        body = [
            rx.text(
                "Run the weekly sync to publish fresh repository activity.", class_name="empty-copy"
            )
        ]

    return section(
        "GitHub Activity Feed",
        *body,
        eyebrow="weekly sync output",
        subtitle="Fresh repository motion rendered straight from the generated GitHub snapshot.",
        action_label="Open GitHub profile",
        action_url="https://github.com/mauricioobgo",
    )


def _certification_card(item: dict) -> rx.Component:
    return rx.box(
        rx.text(item["issuer"], class_name="cert-issuer"),
        rx.heading(item["title"], size="5", class_name="cert-title"),
        *(
            [rx.text(f"issued // {item['issued']}", class_name="cert-meta")]
            if item.get("issued")
            else []
        ),
        *(
            [rx.text(f"credential id // {item['credential_id']}", class_name="cert-meta")]
            if item.get("credential_id")
            else []
        ),
        _terminal_button(
            item.get("credential_label", "View credential"),
            item["credential_url"],
        ),
        class_name="cert-card",
    )


def _certifications_section(certifications: list[dict]) -> rx.Component:
    return section(
        "Certifications and Recognition",
        rx.flex(
            *[_certification_card(item) for item in certifications],
            wrap="wrap",
            gap="1rem",
            width="100%",
        ),
        eyebrow="linkedin credential log",
        subtitle="Publicly visible certifications and recognition currently surfaced on LinkedIn.",
        action_label="Open full LinkedIn certifications",
        action_url=LINKEDIN_CERTIFICATIONS_URL,
    )


def home_page() -> rx.Component:
    content = load_portfolio_content()
    profile = content["profile"]
    generated_profile = content["generated_profile"]
    refresh_log = content["refresh_log"]
    experience = content["experience"]
    certifications = content["certifications"]
    generated_repos = content["generated_repos"]

    return rx.box(
        rx.container(
            rx.vstack(
                _hero(
                    profile,
                    generated_profile,
                    refresh_log,
                    experience,
                    certifications,
                    generated_repos,
                ),
                _experience_section(experience),
                _project_grid(
                    "Selected Delivery Systems",
                    content["projects"],
                    "Curated project highlights will appear here.",
                ),
                _repo_section(generated_repos),
                _certifications_section(certifications),
                width="100%",
                spacing="6",
                align="stretch",
            ),
            max_width="1240px",
            width="100%",
            padding_x=["1rem", "1.3rem", "1.8rem"],
            padding_y="2rem",
        ),
        min_height="100vh",
        width="100%",
        class_name="portfolio-shell",
    )
