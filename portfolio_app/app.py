import reflex as rx
from .pages.home import home_page

app = rx.App()
app.add_page(home_page, route="/")
