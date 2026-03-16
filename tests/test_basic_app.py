import pytest
from shiny.playwright import controller
from playwright.sync_api import Page
from shiny.run import ShinyAppProc


def test_basic_app(page: Page, local_app: ShinyAppProc) -> None:
    page.goto(local_app.url)

    total_bookings = controller.OutputText(page, "total_bookings")
    selectize = controller.InputSelectize(page, "vehicle_type")
    reset_btn = controller.InputActionButton(page, "action_button")

    # initial state
    selectize.expect_selected([])

    # select vehicle
    selectize.set(["Auto", "Bike"])
    selectize.expect_selected(["Auto", "Bike"])

    page.wait_for_timeout(30000)  # wait for reactive update

    # total bookings for Auto and Bike should be 37K
    total_bookings.expect_value("37K")

    # reset filters
    reset_btn.click()
    page.wait_for_load_state("networkidle")

    # expect cleared
    selectize.expect_selected([])
