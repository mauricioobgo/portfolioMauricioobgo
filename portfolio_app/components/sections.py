import reflex as rx


def section(
    title: str,
    *children: rx.Component,
    eyebrow: str | None = None,
    subtitle: str | None = None,
    action_label: str | None = None,
    action_url: str | None = None,
) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.vstack(
                *([rx.text(eyebrow, class_name="section-eyebrow")] if eyebrow else []),
                rx.heading(title, size="6", class_name="section-title"),
                *([rx.text(subtitle, class_name="section-subtitle")] if subtitle else []),
                spacing="1",
                align="start",
            ),
            *(
                [
                    rx.link(
                        action_label,
                        href=action_url,
                        is_external=True,
                        class_name="section-action",
                    )
                ]
                if action_label and action_url
                else []
            ),
            width="100%",
            justify="between",
            align="start",
            gap="1rem",
            wrap="wrap",
        ),
        rx.vstack(
            *children,
            spacing="4",
            align="stretch",
            width="100%",
        ),
        width="100%",
        padding="1.5rem",
        class_name="section-shell",
    )
