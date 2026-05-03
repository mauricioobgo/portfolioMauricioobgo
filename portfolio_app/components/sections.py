import reflex as rx


def section(title: str, body: rx.Component) -> rx.Component:
    return rx.box(
        rx.heading(title, size="5"),
        body,
        margin_bottom="2rem",
    )
