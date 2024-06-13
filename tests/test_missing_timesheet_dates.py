from database.timesheet_data import get_missing_timesheet_dates
from datetime import datetime, timedelta

def test_get_missing_timesheet_dates():
    # Define parameters for the test
    lookback_parameter = 14  # Look back for 2 weeks
    input_date = datetime.now().strftime('%Y-%m-%d')  # Use current date
    midas_table_name = "midas_timesheet"
    bigo_table_name = "bigo_timesheet"

    # Use the store numbers from your config (or define them directly if not using config)
    midas_store_numbers = [2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 22, 23, 24]
    bigo_store_numbers = [14, 15, 16, 17, 18, 19, 20, 21]

    # Get missing timesheet dates for Midas
    print("Testing get_missing_timesheet_dates for Midas...")
    midas_missing_dates = get_missing_timesheet_dates(lookback_parameter, input_date, midas_table_name,
                                                      midas_store_numbers)
    print("Midas missing dates:")
    for store, dates in midas_missing_dates.items():
        print(f"Store {store}: {', '.join(dates)}")

    # Get missing timesheet dates for Bigo
    print("\nTesting get_missing_timesheet_dates for Bigo...")
    bigo_missing_dates = get_missing_timesheet_dates(lookback_parameter, input_date, bigo_table_name,
                                                     bigo_store_numbers)
    print("Bigo missing dates:")
    for store, dates in bigo_missing_dates.items():
        print(f"Store {store}: {', '.join(dates)}")


# Call the test function
if __name__ == '__main__':
    test_get_missing_timesheet_dates()
