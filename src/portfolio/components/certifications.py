from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import BentoGrid, ConsolePanel, SkillPill
from portfolio.interaction import attach_hover_lift, external_link_data, normalize_external_url
from portfolio.theme import MUTED, PRIMARY, PURPLE, TEXT, WARNING


def CertificationCard(page: ft.Page, certification: dict[str, Any]) -> ft.Control:
    accent = WARNING if certification.get("featured") else PRIMARY
    level = certification.get("level") or "Credential"
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
                            SkillPill(level, accent),
                            SkillPill(certification.get("status", "Active"), PURPLE),
                        ],
                    ),
                    ft.Text(
                        certification.get("title", ""),
                        color=TEXT,
                        size=22,
                        font_family="DisplayBold",
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(certification.get("issuer", ""), color=PRIMARY, size=16),
                    ft.Text(certification.get("category", ""), color=MUTED, size=14),
                    ft.Text(
                        certification.get("issued", "Listed on LinkedIn"), color=MUTED, size=13
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=10,
                        run_spacing=10,
                        controls=[
                            SkillPill(skill, accent) for skill in certification.get("skills", [])
                        ],
                    ),
                    ft.FilledButton(
                        content=certification.get("credential_label", "View on LinkedIn"),
                        style=ft.ButtonStyle(
                            bgcolor=accent,
                            color="#020617",
                            shape=ft.RoundedRectangleBorder(radius=16),
                        ),
                        url=normalize_external_url(certification.get("credential_url")),
                        data=external_link_data(
                            certification.get("title", "Certification"),
                            certification.get("credential_url"),
                        ),
                    ),
                ],
            ),
            title=f"{certification.get('issuer', '').lower()} - {level.lower()}",
            glow=bool(certification.get("featured")),
            bgcolor="#111827",
        ),
        scale=1.02,
    )


def CertificationGrid(page: ft.Page, certifications: list[dict[str, Any]]) -> ft.Control:
    ordered = sorted(
        certifications, key=lambda item: (not item.get("featured", False), item.get("title", ""))
    )
    return BentoGrid(
        [
            ft.Container(col={"xs": 12, "md": 6, "xl": 4}, content=CertificationCard(page, item))
            for item in ordered
        ]
    )
