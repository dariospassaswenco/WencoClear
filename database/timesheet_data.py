import pandas as pd
from sqlalchemy import create_engine, text
from config.app_settings import ENGINE, MIDAS_STORE_NUMBERS, BIGO_STORE_NUMBERS, CLOSED_DAYS
from datetime import datetime


def get_missing_timesheet_dates(start_date, end_date, table_name, store_numbers):
    missing_data_info = {}

    for store_number in store_numbers:
        for date in pd.date_range(start=start_date, end=end_date):
            date_str = date.strftime('%Y-%m-%d')
            if date_str in CLOSED_DAYS or date.weekday() == 6:  # Skip closed days and Sundays
                continue
            query = f"""
                SELECT COUNT(*) FROM {table_name} 
                WHERE "wenco_id" = {store_number}
                AND "date" = '{date_str}'
            """
            with ENGINE.connect() as conn:
                result = pd.read_sql_query(query, conn).iloc[0, 0]

            if result == 0:
                if store_number not in missing_data_info:
                    missing_data_info[store_number] = []
                missing_data_info[store_number].append(date_str)

    return missing_data_info

def get_midas_timesheet_data(start_date, end_date):
    query = text("""
        SELECT wenco_id AS store_id, date, date_entered, first_name, last_name, hours
        FROM midas_timesheet
        WHERE date BETWEEN :start_date AND :end_date
    """)
    with ENGINE.connect() as conn:
        result = conn.execute(query, {'start_date': start_date, 'end_date': end_date})
        data = result.fetchall()
    columns = ['store_id', 'date', 'date_entered', 'first_name', 'last_name', 'hours']
    return pd.DataFrame(data, columns=columns)

def get_bigo_timesheet_data(start_date, end_date):
    query = text("""
        SELECT wenco_id AS store_id, date, date_entered, first_name, last_name, hours
        FROM bigo_timesheet
        WHERE date BETWEEN :start_date AND :end_date
    """)
    with ENGINE.connect() as conn:
        result = conn.execute(query, {'start_date': start_date, 'end_date': end_date})
        data = result.fetchall()
    columns = ['store_id', 'date', 'date_entered', 'first_name', 'last_name', 'hours']
    return pd.DataFrame(data, columns=columns)

def get_oldest_date_entered(start_date, end_date):
    query = text("""
        SELECT wenco_id, last_name, first_name, MIN(date_entered) AS oldest_date_entered
        FROM (
            SELECT wenco_id, last_name, first_name, date_entered FROM midas_timesheet WHERE date BETWEEN :start_date AND :end_date
            UNION ALL
            SELECT wenco_id, last_name, first_name, date_entered FROM bigo_timesheet WHERE date BETWEEN :start_date AND :end_date
        ) AS combined_timesheets
        GROUP BY wenco_id, last_name, first_name
        ORDER BY oldest_date_entered
        LIMIT 1
    """)
    with ENGINE.connect() as conn:
        result = conn.execute(query, {'start_date': start_date, 'end_date': end_date}).fetchone()
    return result if result else None


def test_timesheet_data():
    start_date = '2024-06-01'
    end_date = '2024-06-10'
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    print("Testing get_missing_timesheet_dates for Midas:")
    missing_midas_timesheet = get_missing_timesheet_dates(start_date_dt, end_date_dt, 'midas_timesheet', MIDAS_STORE_NUMBERS)
    print(missing_midas_timesheet)

    print("Testing get_missing_timesheet_dates for Bigo:")
    missing_bigo_timesheet = get_missing_timesheet_dates(start_date_dt, end_date_dt, 'bigo_timesheet', BIGO_STORE_NUMBERS)
    print(missing_bigo_timesheet)

    print("Testing get_midas_timesheet_data:")
    midas_timesheet_data = get_midas_timesheet_data(start_date, end_date)
    print(midas_timesheet_data)

    print("Testing get_bigo_timesheet_data:")
    bigo_timesheet_data = get_bigo_timesheet_data(start_date, end_date)
    print(bigo_timesheet_data)


if __name__ == "__main__":
    test_timesheet_data()