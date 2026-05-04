import reflex as rx


def section(title: str, *children: rx.Component) -> rx.Component:
    return rx.box(
        rx.heading(title, size="6", color="#102033"),
        rx.vstack(
            *children,
            spacing="4",
            align="stretch",
            width="100%",
        ),
        width="100%",
        padding="1.5rem",
        border="1px solid rgba(16, 32, 51, 0.08)",
        border_radius="24px",
        background="rgba(255, 255, 255, 0.76)",
        box_shadow="0 24px 60px rgba(16, 32, 51, 0.08)",
        backdrop_filter="blur(18px)",
    )
