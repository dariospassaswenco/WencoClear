import sqlite3
from datetime import datetime, timedelta
from database.db_helpers import get_db_connection

def create_week_ranges_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS week_ranges (
            week_start DATE,
            week_end DATE
        )
    ''')

    conn.commit()
    conn.close()

def populate_week_ranges_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    start_date = datetime.strptime("2020-01-01", "%Y-%m-%d")
    end_date = datetime.strptime("2030-12-31", "%Y-%m-%d")
    current_date = start_date

    week_ranges = []

    while current_date <= end_date:
        # Find the next Sunday
        next_sunday = current_date + timedelta(days=(6 - current_date.weekday()) % 7)
        week_start = next_sunday.strftime("%Y-%m-%d")
        week_end = (next_sunday + timedelta(days=7)).strftime("%Y-%m-%d")

        week_ranges.append((week_start, week_end))
        current_date = next_sunday + timedelta(days=7)

    cursor.executemany('''
        INSERT INTO week_ranges (week_start, week_end)
        VALUES (?, ?)
    ''', week_ranges)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_week_ranges_table()
    populate_week_ranges_table()
