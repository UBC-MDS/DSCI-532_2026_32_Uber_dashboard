from shiny.pytest import create_app_fixture
from shiny.playwright import controller
from playwright.sync_api import Page
from shiny.run import ShinyAppProc

app = create_app_fixture("../src/app.py")

def test_reset_button(page: Page, app: ShinyAppProc) -> None:
    """Checks that the reset button will set the date range slider and vehicle
    type select element to their initial states, and the dashboard displays 
    the correct number for 'Cancelled Bookings'.
    """
    page.goto(app.url)
    page.wait_for_load_state("networkidle")

    canceled_bookings = controller.OutputText(page, "canceled_bookings")
    slider = controller.InputSliderRange(page, "slider")
    selectize = controller.InputSelectize(page, "vehicle_type")
    reset_button = controller.InputActionButton(page, "action_button")

    selectize.set("Bike")
    slider.set(("2024-01-01", "2024-12-26"))
    selectize.expect_selected(["Bike"])
    slider.expect_value(("2024-01-01", "2024-12-26"))
    canceled_bookings.expect_value("6K", timeout=20000)

    reset_button.click()
    page.wait_for_selector("html:not(.shiny-busy)")
    selectize.expect_selected([], timeout=40000)
    slider.expect_value(("2024-01-01", "2024-12-30"), timeout=40000)
    canceled_bookings.expect_value("38K", timeout=40000)
