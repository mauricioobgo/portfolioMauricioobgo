from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import SectionHeader
from portfolio.components.certifications import CertificationShowcase
from portfolio.interaction import external_link_data, normalize_external_url
from portfolio.theme import MUTED, WARNING, alpha


def _linkedin_banner(content: dict[str, Any]) -> ft.Control:
    profile = content.get("profile", {})
    url = profile.get("linkedin_certifications_url") or profile.get("social_links", {}).get(
        "linkedin"
    )
    certifications = content.get("certifications", [])
    featured_count = sum(1 for item in certifications if item.get("featured"))
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=18, vertical=14),
        border_radius=16,
        bgcolor=alpha(WARNING, 0.06),
        border=ft.Border.all(1, alpha(WARNING, 0.22)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            wrap=True,
            run_spacing=10,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Icon(ft.Icons.VERIFIED_USER, color=WARNING, size=18),
                        ft.Text(
                            f"{len(certifications)} credentials · "
                            f"{featured_count} featured AWS certifications",
                            color=MUTED,
                            size=13,
                            font_family="Mono",
                        ),
                    ],
                ),
                ft.TextButton(
                    content=ft.Row(
                        spacing=6,
                        controls=[
                            ft.Text(
                                "verify all on LinkedIn",
                                color=WARNING,
                                size=13,
                                font_family="Mono",
                                weight=ft.FontWeight.W_700,
                            ),
                            ft.Icon(ft.Icons.OPEN_IN_NEW, color=WARNING, size=14),
                        ],
                    ),
                    url=normalize_external_url(url),
                    data=external_link_data("LinkedIn Certifications", url),
                ),
            ],
        ),
    )


def CertificationsSection(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return ft.Container(
        key="certifications",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "CERTIFICATIONS",
                    "Validated credentials",
                    "AWS Professional and Specialty certifications, verifiable on LinkedIn.",
                    accent=WARNING,
                ),
                _linkedin_banner(content),
                CertificationShowcase(page, content.get("certifications", [])),
            ],
        ),
    )
