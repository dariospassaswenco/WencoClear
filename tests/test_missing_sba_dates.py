from datetime import datetime, timedelta
from config.app_settings import MIDAS_SBA_TABLE
from database.sales_by_category_data import get_missing_sales_by_category_dates


def test_get_missing_sales_by_category_dates():
    # Define parameters for the test
    end_date = datetime.now().strftime('%Y-%m-%d')  # Use current date as end date
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')  # 7 days ago as start date
    table_name = MIDAS_SBA_TABLE

    # Use the Midas store numbers
    midas_store_numbers = [2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 22, 23, 24]

    # Get missing sales by category dates for Midas
    print("Testing get_missing_sales_by_category_dates for Midas...")
    missing_dates = get_missing_sales_by_category_dates(start_date, end_date, midas_store_numbers, table_name)

    if missing_dates:
        print("Midas stores with missing sales by category data:")
        for store, dates in missing_dates.items():
            print(f"Store {store}: {', '.join(dates)}")
    else:
        print("No Midas stores found with missing sales by category data.")


# Call the test function
if __name__ == '__main__':
    test_get_missing_sales_by_category_dates()