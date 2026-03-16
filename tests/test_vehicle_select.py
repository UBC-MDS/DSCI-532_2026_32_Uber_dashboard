from shiny.pytest import create_app_fixture
from shiny.playwright import controller
from playwright.sync_api import Page
from shiny.run import ShinyAppProc

app = create_app_fixture("../src/app.py")

def test_basic_app(page: Page, app: ShinyAppProc) -> None:
    page.goto(app.url)

    total_bookings = controller.OutputText(page, "total_bookings")
    selectize = controller.InputSelectize(page, "vehicle_type")

    # initial state
    selectize.expect_selected([])

    # select vehicle
    selectize.set("Auto")
    selectize.expect_selected(["Auto"])

    # total bookings for Auto and Bike should be 37K
    total_bookings.expect_value("37K", timeout=20000)
