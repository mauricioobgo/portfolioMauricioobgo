import flet as ft

from portfolio.components.cards import LottiePanel


def test_lottie_panel_returns_control_even_if_asset_is_missing() -> None:
    control = LottiePanel(
        "Test panel",
        "lottie/missing_animation.json",
        caption="Fallback should still render a control.",
    )

    assert isinstance(control, ft.Control)
