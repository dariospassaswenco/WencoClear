import pandas as pd
from datetime import datetime, timedelta
from config.app_settings import ENGINE, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE, BIGO_STORE_NUMBERS, BIGO_SS_TABLE, \
    CLOSED_DAYS

def get_missing_sales_by_category_dates(start_date, end_date, store_numbers, table_name):
    try:
        missing_dates_per_store = {store: [] for store in store_numbers}
        date_range = pd.date_range(start=start_date, end=end_date)

        for date in date_range:
            date_str = date.strftime('%Y-%m-%d')
            if date_str in CLOSED_DAYS or date.weekday() == 6:  # Skip closed days and Sundays
                continue
            for store_number in store_numbers:
                query = f"SELECT COUNT(*) FROM {table_name} WHERE date = '{date_str}' AND wenco_id = {store_number}"
                result = pd.read_sql_query(query, ENGINE).iloc[0, 0]
                if result == 0:
                    missing_dates_per_store[store_number].append(date_str)

        stores_with_missing_dates = {store: dates for store, dates in missing_dates_per_store.items() if dates}
        return stores_with_missing_dates
    except Exception as e:
        print(f"Error: {e}")
        return {}