import reflex as rx

from portfolio_app.components.sections import section
from portfolio_app.services.content import load_portfolio_content


CONTENT = load_portfolio_content()


def _hero(profile: dict, generated_profile: dict, refresh_log: dict) -> rx.Component:
    social_links = profile["social_links"]
    refresh_copy = ""
    if refresh_log:
        refresh_copy = (
            f"Last refresh: {refresh_log['scope']} cadence at {refresh_log['executed_at']}"
        )

    avatar_url = generated_profile.get("avatar_url")
    location = generated_profile.get("location")

    return rx.box(
        rx.flex(
            rx.vstack(
                rx.text(
                    "Python-first portfolio",
                    text_transform="uppercase",
                    letter_spacing="0.24em",
                    color="#c06a15",
                    font_weight="700",
                    font_size="0.8rem",
                ),
                rx.heading(
                    profile["name"],
                    size="9",
                    color="#102033",
                    line_height="1.05",
                ),
                rx.heading(
                    profile["title"],
                    size="7",
                    color="#334155",
                    line_height="1.1",
                ),
                rx.text(
                    profile["subtitle"],
                    color="#475569",
                    font_size="1.1rem",
                    max_width="42rem",
                ),
                rx.hstack(
                    *[
                        rx.box(
                            skill,
                            padding="0.5rem 0.8rem",
                            border_radius="999px",
                            background="rgba(255, 255, 255, 0.72)",
                            border="1px solid rgba(16, 32, 51, 0.08)",
                            color="#102033",
                            font_weight="600",
                        )
                        for skill in profile["skills"]
                    ],
                    wrap="wrap",
                    spacing="3",
                ),
                rx.hstack(
                    rx.link(
                        "View resume",
                        href=profile["resume_link"],
                        is_external=True,
                        padding="0.85rem 1.2rem",
                        border_radius="999px",
                        background="#102033",
                        color="white",
                        font_weight="700",
                        text_decoration="none",
                    ),
                    rx.link(
                        "Send email",
                        href=f"mailto:{profile['email']}",
                        padding="0.85rem 1.2rem",
                        border_radius="999px",
                        border="1px solid rgba(16, 32, 51, 0.14)",
                        color="#102033",
                        font_weight="700",
                        text_decoration="none",
                    ),
                    spacing="3",
                    wrap="wrap",
                ),
                rx.hstack(
                    rx.link("GitHub", href=social_links["github"], is_external=True, color="#102033"),
                    rx.text("•", color="#94a3b8"),
                    rx.link(
                        "LinkedIn",
                        href=social_links["linkedin"],
                        is_external=True,
                        color="#102033",
                    ),
                    *((
                        rx.text("•", color="#94a3b8"),
                        rx.text(location, color="#475569"),
                    ) if location else ()),
                    spacing="3",
                    wrap="wrap",
                ),
                *((
                    rx.text(
                        refresh_copy,
                        color="#64748b",
                        font_size="0.92rem",
                    ),
                ) if refresh_copy else ()),
                align="start",
                spacing="5",
                width="100%",
                max_width="42rem",
            ),
            *((
                rx.box(
                    rx.image(
                        src=avatar_url,
                        alt=f"{profile['name']} GitHub avatar",
                        width="100%",
                        height="100%",
                        object_fit="cover",
                    ),
                    width="220px",
                    height="220px",
                    border_radius="28px",
                    overflow="hidden",
                    box_shadow="0 28px 60px rgba(16, 32, 51, 0.16)",
                    border="1px solid rgba(255, 255, 255, 0.5)",
                    flex_shrink="0",
                ),
            ) if avatar_url else ()),
            width="100%",
            justify="between",
            align="center",
            gap="2rem",
            wrap="wrap",
        ),
        width="100%",
        padding="2rem",
        border_radius="32px",
        background=(
            "linear-gradient(135deg, rgba(245, 158, 11, 0.18), rgba(255, 255, 255, 0.88))"
        ),
        border="1px solid rgba(255, 255, 255, 0.54)",
        box_shadow="0 32px 80px rgba(16, 32, 51, 0.12)",
    )


def _experience_section(experience: list[dict]) -> rx.Component:
    return section(
        "Experience",
        *[
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.heading(item["role"], size="5", color="#102033"),
                        rx.text(item["company"], color="#c06a15", font_weight="700"),
                        rx.text(item["description"], color="#475569"),
                        align="start",
                        spacing="2",
                    ),
                    rx.text(
                        item["date"],
                        color="#64748b",
                        white_space="nowrap",
                    ),
                    width="100%",
                    justify="between",
                    align="start",
                    gap="1rem",
                    wrap="wrap",
                ),
                padding_bottom="1.2rem",
                border_bottom="1px solid rgba(16, 32, 51, 0.08)",
            )
            for item in experience
        ],
    )


def _project_grid(title: str, items: list[dict], empty_state: str) -> rx.Component:
    body: list[rx.Component]
    if items:
        body = [
            rx.flex(
                *[
                    rx.box(
                        rx.heading(item["name"], size="5", color="#102033"),
                        rx.text(item["summary"], color="#475569"),
                        *([
                            rx.link(
                                "Open repository",
                                href=item["html_url"],
                                is_external=True,
                                color="#c06a15",
                                font_weight="700",
                            )
                        ] if item.get("html_url") else []),
                        padding="1.25rem",
                        border_radius="20px",
                        background="rgba(255, 255, 255, 0.82)",
                        border="1px solid rgba(16, 32, 51, 0.08)",
                        box_shadow="0 18px 40px rgba(16, 32, 51, 0.06)",
                        flex="1 1 280px",
                    )
                    for item in items
                ],
                wrap="wrap",
                gap="1rem",
                width="100%",
            )
        ]
    else:
        body = [rx.text(empty_state, color="#64748b")]

    return section(title, *body)


def _certifications_section(certifications: list[dict]) -> rx.Component:
    return section(
        "Certifications",
        *[
            rx.box(
                rx.heading(item["title"], size="5", color="#102033"),
                rx.text(item["issuer"], color="#475569"),
                rx.link(
                    "View credential",
                    href=item["credential_url"],
                    is_external=True,
                    color="#c06a15",
                    font_weight="700",
                ),
                padding="1.25rem",
                border_radius="20px",
                background="rgba(255, 255, 255, 0.82)",
                border="1px solid rgba(16, 32, 51, 0.08)",
            )
            for item in certifications
        ],
    )


def home_page() -> rx.Component:
    profile = CONTENT["profile"]
    generated_profile = CONTENT["generated_profile"]
    refresh_log = CONTENT["refresh_log"]
    generated_repos = CONTENT["generated_repos"]

    latest_repos = [
        {
            "name": repo["name"],
            "summary": repo.get("description") or "Recently updated GitHub repository.",
            "html_url": repo["html_url"],
        }
        for repo in generated_repos[:6]
    ]

    return rx.box(
        rx.container(
            rx.vstack(
                _hero(profile, generated_profile, refresh_log),
                _experience_section(CONTENT["experience"]),
                _project_grid(
                    "Featured Work",
                    CONTENT["projects"],
                    "Curated project highlights will appear here.",
                ),
                _project_grid(
                    "Latest GitHub Repositories",
                    latest_repos,
                    "Run the weekly sync to publish fresh repository activity.",
                ),
                _certifications_section(CONTENT["certifications"]),
                width="100%",
                spacing="7",
                align="stretch",
            ),
            max_width="1200px",
            width="100%",
            padding_x=["1.2rem", "1.5rem", "2rem"],
            padding_y="2.5rem",
        ),
        min_height="100vh",
        width="100%",
    )
