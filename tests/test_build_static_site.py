from __future__ import annotations

from pathlib import Path

from portfolio_app.scripts import build_static_site
from portfolio_app.services.content import write_frontend_content


def _ensure_content() -> None:
    if not build_static_site.CONTENT_PATH.exists():
        write_frontend_content()


def test_build_static_site_emits_self_contained_html(tmp_path: Path) -> None:
    _ensure_content()
    out = build_static_site.build_static_site(tmp_path / "site")

    index = out / "index.html"
    assert index.is_file()
    html = index.read_text(encoding="utf-8")

    # Server-side rendered content is present without needing JavaScript.
    assert "Mauricio" in html
    assert "<style>" in html and "</style>" in html
    for section in ("focus", "projects", "certifications", "contact"):
        assert f'id="{section}"' in html

    # Fonts and the no-Jekyll marker are emitted for reliable Pages hosting.
    assert (out / ".nojekyll").is_file()
    assert (out / "fonts").is_dir()


def test_static_site_includes_featured_certification_and_links(tmp_path: Path) -> None:
    _ensure_content()
    out = build_static_site.build_static_site(tmp_path / "site")
    html = (out / "index.html").read_text(encoding="utf-8")

    assert "Solutions Architect" in html
    assert "linkedin.com/in/mauricioobgo" in html
    assert "mailto:" in html


def test_safe_url_rejects_unsafe_schemes() -> None:
    assert build_static_site._safe_url("https://example.com") == "https://example.com"
    assert build_static_site._safe_url("mailto:a@b.com") == "mailto:a@b.com"
    assert build_static_site._safe_url("javascript:alert(1)") is None
    assert build_static_site._safe_url("") is None
    assert build_static_site._safe_url(None) is None
