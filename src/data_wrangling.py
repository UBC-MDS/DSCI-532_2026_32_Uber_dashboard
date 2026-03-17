import pandas as pd


def data_wrangling(uber):
    """
    Perform data wrangling on the Uber ride bookings dataset. This includes:
    - Replacing spaces in column names with underscores.
    - Converting the 'Date' column to datetime format.
    - Creating a new 'Issue_Reason' column with all reasons why a
    ride is not completed. 
    - Converting to object type columns not in these types:
    datetime, integer, unsigned integer, float, boolean.
    Parameters:
        uber (pd.DataFrame): The raw Uber ride bookings dataset.
    Returns:
        None: Modifies the DataFrame in place.
    """
    uber.columns = uber.columns.str.replace(" ", "_", regex=False)
    uber["Date"] = pd.to_datetime(uber["Date"])
    uber['Issue_Reason'] = (
        uber['Reason_for_cancelling_by_Customer']
        .fillna(uber['Driver_Cancellation_Reason'])
        .fillna(uber['Incomplete_Rides_Reason'])
        .fillna('')
    )
    for col in uber.columns:
        if uber[col].dtype.kind not in ('M', 'i', 'u', 'f', 'b'):
            uber[col] = uber[col].astype(object)