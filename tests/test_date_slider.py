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
    selectize = controller.InputSelectize(page, "vehicle_type")
    slider.expect_value(("2024-01-01", "2024-12-30"))

    selectize.set("Go Mini")
    slider.set(("2024-01-04", "2024-12-30"))
    selectize.expect_selected(["Go Mini"])
    slider.expect_value(("2024-01-04", "2024-12-30"))
    total_revenue.expect_value("10M", timeout=60000)
