from types import SimpleNamespace

import flet as ft

from portfolio.app import build_portfolio_view
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
