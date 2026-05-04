from reflex.plugins import SitemapPlugin

from portfolio_app.app import app
from portfolio_app.services.content import load_portfolio_content
from rxconfig import config


def test_reflex_config_targets_gh_pages() -> None:
    assert config.app_name == "portfolio_app"
    assert config.frontend_path == "/portfolioMauricioobgo"
    assert config.api_url
    assert any(isinstance(plugin, SitemapPlugin) for plugin in config.plugins)


def test_app_is_static() -> None:
    assert app.enable_state is False
    assert app._state is None


def test_portfolio_content_loads_yaml_baseline() -> None:
    content = load_portfolio_content()

    assert content["profile"]["name"] == "Mauricio Obando"
    assert content["projects"]
    assert content["experience"]
    assert content["certifications"]
