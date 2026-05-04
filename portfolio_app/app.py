import reflex as rx
from reflex.config import get_config

from .pages.home import home_page


def _asset_url(path: str) -> str:
    return get_config().prepend_frontend_path(path)


app = rx.App(
    enable_state=False,
    theme=rx.theme(
        accent_color="amber",
        gray_color="sand",
        radius="large",
        scaling="105%",
    ),
    stylesheets=["/site.css"],
    head_components=[
        rx.el.Meta.create(name="theme-color", content="#102033"),
        rx.el.Link.create(rel="manifest", href=_asset_url("/manifest.json")),
        rx.el.Link.create(
            rel="apple-touch-icon",
            sizes="180x180",
            href=_asset_url("/apple-touch-icon.png"),
        ),
        rx.el.Link.create(
            rel="icon",
            type="image/png",
            sizes="32x32",
            href=_asset_url("/favicon-32x32.png"),
        ),
        rx.el.Link.create(
            rel="icon",
            type="image/png",
            sizes="16x16",
            href=_asset_url("/favicon-16x16.png"),
        ),
        rx.el.Link.create(
            rel="mask-icon",
            href=_asset_url("/safari-pinned-tab.svg"),
            color="#102033",
        ),
    ],
)
app.add_page(
    home_page,
    route="/",
    title="Mauricio Obando | Data Engineering Portfolio",
    description=(
        "Data engineering, analytics, and cloud delivery portfolio for "
        "Mauricio Obando."
    ),
    image="android-chrome-384x384.png",
    meta=[
        {"name": "twitter:card", "content": "summary_large_image"},
        {"name": "twitter:title", "content": "Mauricio Obando | Data Engineering Portfolio"},
        {
            "name": "twitter:description",
            "content": "Data engineering, analytics, and cloud delivery portfolio for Mauricio Obando.",
        },
    ],
)
