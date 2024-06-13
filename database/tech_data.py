import pandas as pd
from datetime import datetime, timedelta
from config.app_settings import ENGINE, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE, BIGO_STORE_NUMBERS, BIGO_SS_TABLE, \
    CLOSED_DAYS


def get_missing_midas_tech_dates(start_date, end_date, store_numbers, table_name):
    try:
        missing_dates_per_store = {store: [] for store in store_numbers}
        date_range = pd.date_range(start=start_date, end=end_date)

        for date in date_range:
            date_str = date.strftime('%Y-%m-%d')
            if date_str in CLOSED_DAYS or date.weekday() == 6:
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


def get_missing_bigo_tech_dates(start_date, end_date, table_name):
    try:
        missing_dates = []
        date_range = pd.date_range(start=start_date, end=end_date)

        for date in date_range:
            date_str = date.strftime('%Y-%m-%d')
            if date_str in CLOSED_DAYS or date.weekday() == 6:
                continue
            query = f"SELECT COUNT(*) FROM {table_name} WHERE date = '{date_str}'"
            result = pd.read_sql_query(query, ENGINE).iloc[0, 0]
            if result == 0:
                missing_dates.append(date_str)

        return missing_dates
    except Exception as e:
        print(f"Error: {e}")
        return []


def display_missing_tech_data(store_missing_dates, store_type):
    if store_missing_dates:
        print(f"----------- {store_type} Stores with missing Tech data: -----------")
        for store, missing_dates in store_missing_dates.items():
            print(f"Store {store}: Missing dates - {', '.join(missing_dates)}")
        print("\n")
    else:
        print(f"No {store_type} stores found with missing data.")
        print("\n")


def display_missing_bigo_tech_data(missing_dates, store_type):
    if missing_dates:
        print(f"----------- {store_type} Missing Tech data for the following dates: ----------")
        print(", ".join(missing_dates))
    else:
        print(f"----------- {store_type} Tech data is up to date. -----------")


# Example usage:
if __name__ == "__main__":
    start_date_str = "2024-06-06"  # example start date
    end_date_str = "2024-06-12"  # example end date
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    midas_with_missing_dates = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS,
                                                            'midas_tech_summary')
    display_missing_tech_data(midas_with_missing_dates, "Midas")

    bigo_with_missing_dates = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
    display_missing_bigo_tech_data(bigo_with_missing_dates, "Bigo")
