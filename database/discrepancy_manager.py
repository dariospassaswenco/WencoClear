import sqlite3
from datetime import datetime, timedelta
from database.db_helpers import get_db_connection
from contextlib import closing


def get_week_start_end(end_date_str):
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    start_date = end_date - timedelta(days=6)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def create_discrepancy_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timesheet_discrepancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store TEXT,
            first_name TEXT,
            last_name TEXT,
            week_start DATE,
            week_end DATE,
            UNIQUE(store, first_name, last_name, week_start, week_end)
        )
    ''')

    conn.commit()
    conn.close()


def fetch_timesheet_discrepancies(week_end_date):
    # Calculate the start date (7 days prior)
    week_start_date, week_end_date = get_week_start_end(week_end_date)

    try:
        # Ensure the database connection can be established
        conn = get_db_connection()
        conn.close()  # Close the connection immediately after the test

        # Fetch sales summaries for both Big O Tires and Midas
        bigo = query_timesheet_discrepancies("bigo", week_start_date, week_end_date)
        midas = query_timesheet_discrepancies("midas", week_start_date, week_end_date)

        # Combine both results into a single list
        all_discrepancies = {"bigo": bigo, "midas": midas}

        # Insert discrepancies into the table
        insert_discrepancies("bigo", bigo, week_start_date, week_end_date)
        insert_discrepancies("midas", midas, week_start_date, week_end_date)

        return all_discrepancies
    except Exception as e:
        print(f"Exception {e} occurred")
        return []


def query_timesheet_discrepancies(store: str, start_date: str, end_date: str):
    if store.lower() == "bigo":
        timesheet_query = """
            SELECT DISTINCT first_name, last_name
            FROM bigo_timesheet
            WHERE Date BETWEEN ? AND ?;
        """
    elif store.lower() == "midas":
        timesheet_query = """
            SELECT DISTINCT first_name, last_name
            FROM midas_timesheet
            WHERE Date BETWEEN ? AND ?;
        """
    else:
        raise ValueError("Invalid store type. Only 'bigo' and 'midas' are supported.")

    employee_query = """
        SELECT DISTINCT first_name, last_name
        FROM employees;
    """

    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()

        # Query timesheet table for unique names within the specified date range
        cursor.execute(timesheet_query, (start_date, end_date))
        timesheet_employees = set(cursor.fetchall())

        # Query employee table for unique names
        cursor.execute(employee_query)
        employees = set(cursor.fetchall())

    # Find discrepancies
    discrepancies = timesheet_employees - employees

    return discrepancies


def insert_discrepancies(store, discrepancies, week_start, week_end):
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        for first_name, last_name in discrepancies:
            cursor.execute('''
                INSERT OR IGNORE INTO timesheet_discrepancies (store, first_name, last_name, week_start, week_end)
                VALUES (?, ?, ?, ?, ?)
            ''', (store, first_name, last_name, week_start, week_end))

        conn.commit()


def clean_discrepancies():
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()

        # Remove discrepancies that now exist in the employees table
        cursor.execute('''
            DELETE FROM timesheet_discrepancies
            WHERE (first_name, last_name) IN (
                SELECT first_name, last_name
                FROM employees
            )
        ''')

        conn.commit()


if __name__ == "__main__":
    create_discrepancy_table()

    # Manually enter the week end date
    week_end_date = input("Enter the week end date (YYYY-MM-DD): ")

    # Clean up existing discrepancies
    clean_discrepancies()

    # Fetch and update timesheet discrepancies
    discrepancies = fetch_timesheet_discrepancies(week_end_date)
    print("Discrepancies:", discrepancies)
