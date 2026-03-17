import os
import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.data_wrangling import data_wrangling

@pytest.fixture
def data():
    BASE_DIR = Path(__file__).parent
    parquet_path = BASE_DIR.parent / "data" / "processed" / "ncr_ride_bookings.parquet"
    data = pd.read_parquet(parquet_path)
    return data


def test_data_wrangling(data):
    """Test that check for consistency in 'Issue_Reason' with their source
    columns for corresponding 'Booking_Status'. This is data validation necessary to generated
    the sunburst chart correctly.
    """
    data_wrangling(data)
    null_error = "There are still null values in the Issue_Reason column."
    assert data["Issue_Reason"].isna().sum() == 0, null_error
    verify_booking_status(data, "Incomplete", "Incomplete_Rides_Reason")
    verify_booking_status(data, "Cancelled by Driver", "Driver_Cancellation_Reason")
    verify_booking_status(data, "Cancelled by Customer", "Reason_for_cancelling_by_Customer")


def verify_booking_status(data, booking_status, original_column):
    incomplete = data.query(f"Booking_Status == '{booking_status}'")
    count_of_non_match = (incomplete[original_column] != incomplete['Issue_Reason']).sum()
    error_msg = f"'{original_column}' not match Issue Reason for {booking_status} booking status."
    assert count_of_non_match == 0, error_msg