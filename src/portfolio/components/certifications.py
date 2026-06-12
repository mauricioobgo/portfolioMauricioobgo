from __future__ import annotations

from typing import Any

import flet as ft

from portfolio.components.cards import ConsolePanel, SkillPill
from portfolio.interaction import attach_hover_lift, external_link_data, normalize_external_url
from portfolio.theme import (
    CARD,
    MUTED,
    PRIMARY,
    SECONDARY,
    TEXT,
    WARNING,
    alpha,
)


def _issuer_monogram(issuer: str, accent: str) -> ft.Control:
    initials = "".join(word[0] for word in issuer.split()[:2]).upper() or "C"
    return ft.Container(
        width=52,
        height=52,
        border_radius=14,
        alignment=ft.Alignment(0, 0),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[alpha(accent, 0.28), alpha(accent, 0.06)],
        ),
        border=ft.Border.all(1, alpha(accent, 0.45)),
        content=ft.Text(
            initials,
            color=accent,
            size=18,
            font_family="DisplayBold",
            weight=ft.FontWeight.W_700,
        ),
    )


def _verify_button(certification: dict[str, Any], accent: str, *, filled: bool) -> ft.Control:
    label = certification.get("credential_label", "View on LinkedIn")
    url = certification.get("credential_url")
    content = ft.Row(
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Icon(ft.Icons.VERIFIED, size=16, color="#04070F" if filled else accent),
            ft.Text(
                label,
                font_family="Mono",
                size=12,
                weight=ft.FontWeight.W_700,
                color="#04070F" if filled else accent,
            ),
        ],
    )
    if filled:
        return ft.FilledButton(
            content=content,
            style=ft.ButtonStyle(
                bgcolor=accent,
                color="#04070F",
                padding=ft.Padding.symmetric(horizontal=18, vertical=14),
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            url=normalize_external_url(url),
            data=external_link_data(certification.get("title", "Certification"), url),
        )
    return ft.OutlinedButton(
        content=content,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1, alpha(accent, 0.4)),
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        url=normalize_external_url(url),
        data=external_link_data(certification.get("title", "Certification"), url),
    )


def FeaturedCertificationCard(certification: dict[str, Any]) -> ft.Control:
    accent = WARNING
    level = certification.get("level") or "Credential"
    return attach_hover_lift(
        ft.Container(
            data={"kind": "certification_card", "featured": True},
            border_radius=20,
            padding=ft.Padding.all(1.5),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[alpha(accent, 0.65), alpha(PRIMARY, 0.35), alpha(accent, 0.15)],
            ),
            content=ft.Container(
                border_radius=19,
                bgcolor=CARD,
                padding=ft.Padding.all(24),
                content=ft.Column(
                    spacing=16,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                _issuer_monogram(certification.get("issuer", ""), accent),
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        SkillPill(level.upper(), accent),
                                        SkillPill(
                                            certification.get("status", "Active").upper(),
                                            SECONDARY,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.Text(
                            certification.get("title", ""),
                            color=TEXT,
                            size=21,
                            font_family="DisplayBold",
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            f"{certification.get('issuer', '')} · "
                            f"{certification.get('category', '')}",
                            color=PRIMARY,
                            size=14,
                        ),
                        ft.Row(
                            wrap=True,
                            spacing=8,
                            run_spacing=8,
                            controls=[
                                SkillPill(skill, MUTED)
                                for skill in certification.get("skills", [])[:5]
                            ],
                        ),
                        _verify_button(certification, accent, filled=True),
                    ],
                ),
            ),
        ),
        scale=1.02,
    )


def CertificationCard(page: ft.Page, certification: dict[str, Any]) -> ft.Control:
    del page
    if certification.get("featured"):
        return FeaturedCertificationCard(certification)

    accent = PRIMARY
    level = certification.get("level") or "Credential"
    issued = certification.get("issued") or "Listed on LinkedIn"
    return attach_hover_lift(
        ConsolePanel(
            ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            _issuer_monogram(certification.get("issuer", ""), accent),
                            ft.Column(
                                spacing=2,
                                expand=True,
                                controls=[
                                    ft.Text(
                                        certification.get("title", ""),
                                        color=TEXT,
                                        size=16,
                                        font_family="DisplayBold",
                                        weight=ft.FontWeight.W_700,
                                        max_lines=2,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                    ft.Text(
                                        f"{certification.get('issuer', '')} · {issued}",
                                        color=MUTED,
                                        size=12,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=8,
                        run_spacing=8,
                        controls=[
                            SkillPill(level, accent),
                            *[
                                SkillPill(skill, MUTED)
                                for skill in certification.get("skills", [])[:3]
                            ],
                        ],
                    ),
                    _verify_button(certification, accent, filled=False),
                ],
            ),
            padding=ft.Padding.all(20),
        ),
        scale=1.02,
    )


def CertificationShowcase(page: ft.Page, certifications: list[dict[str, Any]]) -> ft.Control:
    featured = [item for item in certifications if item.get("featured")]
    others = sorted(
        (item for item in certifications if not item.get("featured")),
        key=lambda item: item.get("title", ""),
    )
    rows: list[ft.Control] = []
    if featured:
        rows.append(
            ft.ResponsiveRow(
                columns=12,
                spacing=18,
                run_spacing=18,
                controls=[
                    ft.Container(col={"xs": 12, "md": 6}, content=FeaturedCertificationCard(item))
                    for item in featured
                ],
            )
        )
    if others:
        rows.append(
            ft.ResponsiveRow(
                columns=12,
                spacing=16,
                run_spacing=16,
                controls=[
                    ft.Container(
                        col={"xs": 12, "md": 6, "xl": 4},
                        content=CertificationCard(page, item),
                    )
                    for item in others
                ],
            )
        )
    return ft.Column(spacing=18, controls=rows)


def CertificationGrid(page: ft.Page, certifications: list[dict[str, Any]]) -> ft.Control:
    return CertificationShowcase(page, certifications)
