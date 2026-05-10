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
                    "Validated credentials",
                    "Featured AWS credentials stay prominent and link back to the LinkedIn certifications page through managed data.",
                ),
                CertificationGrid(page, content.get("certifications", [])),
            ],
        ),
    )
