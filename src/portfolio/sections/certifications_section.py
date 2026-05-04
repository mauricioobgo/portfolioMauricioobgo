from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import SectionHeader
from portfolio.components.certifications import CertificationGrid


def CertificationsSection(page: ft.Page, content: dict[str, Any]) -> ft.Control:
    return ft.Container(
        key="certifications",
        content=ft.Column(
            spacing=18,
            controls=[
                SectionHeader(
                    page,
                    "CERTIFICATIONS",
                    "Prominent AWS credentials and linked proof points.",
                    "Featured AWS professional credentials stay near the top and always link back to the LinkedIn "
                    "certifications section instead of relying on scraping.",
                ),
                CertificationGrid(page, content.get("certifications", [])),
            ],
        ),
    )
