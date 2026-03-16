from shiny.pytest import create_app_fixture
from shiny.playwright import controller
from playwright.sync_api import Page
from shiny.run import ShinyAppProc

app = create_app_fixture("../src/app.py")

def test_date_slider(page: Page, app: ShinyAppProc) -> None:
    page.goto(app.url)

    total_revenue = controller.OutputText(page, "total_revenue")
    slider = controller.InputSliderRange(page, "slider")

    # initial state
    slider.expect_value(("2024-01-01", "2024-12-30"))

    slider.set(("2024-01-01", "2024-11-09"))
    slider.expect_value(("2024-01-01", "2024-11-09"))
    total_revenue.expect_value("44M", timeout=40000)
