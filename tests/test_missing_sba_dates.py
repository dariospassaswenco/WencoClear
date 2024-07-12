from datetime import datetime, timedelta
from config.app_settings import MIDAS_SBA_TABLE, BIGO_SBA_TABLE, MIDAS_STORE_NUMBERS, BIGO_STORE_NUMBERS
from database.sales_by_category_data import get_missing_sales_by_category_dates

def test_get_missing_sales_by_category_dates():
    # Define parameters for the test
    end_date = datetime.now().strftime('%Y-%m-%d')  # Use current date as end date
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')  # 7 days ago as start date

    # Test for Midas
    print("Testing get_missing_sales_by_category_dates for Midas...")
    midas_missing_dates = get_missing_sales_by_category_dates(
        start_date,
        end_date,
        MIDAS_STORE_NUMBERS,
        MIDAS_SBA_TABLE,
    )

    if midas_missing_dates:
        print("Midas stores with missing sales by category data:")
        for store, dates in midas_missing_dates.items():
            print(f"Store {store}: {', '.join(dates)}")
    else:
        print("No Midas stores found with missing sales by category data.")

    print("\n" + "="*50 + "\n")

    # Test for Bigo
    print("Testing get_missing_sales_by_category_dates for Bigo...")
    bigo_missing_dates = get_missing_sales_by_category_dates(
        start_date,
        end_date,
        BIGO_STORE_NUMBERS,
        BIGO_SBA_TABLE,
    )

    if bigo_missing_dates:
        print("Bigo stores with missing sales by category data:")
        for store, dates in bigo_missing_dates.items():
            print(f"Store {store}: {', '.join(dates)}")
    else:
        print("No Bigo stores found with missing sales by category data.")

# Call the test function
if __name__ == '__main__':
    test_get_missing_sales_by_category_dates()