from shiny.pytest import create_app_fixture
from shiny.playwright import controller
from playwright.sync_api import Page
from shiny.run import ShinyAppProc

app = create_app_fixture("../src/app.py")

def test_date_slider(page: Page, app: ShinyAppProc) -> None:
    """Checks that both ends of the date range slider works to filter the data
    and render the corect number of 'Total Revenue'.
    """
    page.goto(app.url)
    page.wait_for_load_state("networkidle")
    total_revenue = controller.OutputText(page, "total_revenue")
    slider = controller.InputSliderRange(page, "slider")

    # initial state
    slider.expect_value(("2024-01-01", "2024-12-30"))

    slider.set(("2024-01-04", "2024-12-26"))
    slider.expect_value(("2024-01-04", "2024-12-26"), timeout=30000)
    total_revenue.expect_value("51M", timeout=60000)
