import reflex as rx


def home_page() -> rx.Component:
    return rx.container(
        rx.heading("Mauricio Obando", size="8"),
        rx.text("Data Engineer | Data Scientist | Cloud"),
        rx.text("Refactored portfolio powered by Reflex and YAML data."),
        padding="2rem",
    )
