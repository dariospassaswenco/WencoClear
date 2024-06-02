import sqlite3
from datetime import datetime, timedelta
from database.db_helpers import get_db_connection
from contextlib import closing

def get_week_start_end(date_obj):
    start = date_obj - timedelta(days=date_obj.weekday() + 1)
    end = start + timedelta(days=6)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

def create_wenco_timesheet_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wenco_timesheet (
            wenco_id INTEGER,
            week_start DATE,
            week_end DATE,
            first_name TEXT,
            last_name TEXT,
            total_hours FLOAT,
            overtime_hours FLOAT
        )
    ''')

    conn.commit()
    conn.close()

def fetch_week_ranges():
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT week_start, week_end FROM week_ranges ORDER BY week_start')
        weeks = cursor.fetchall()
    return weeks

def fetch_and_insert_timesheet_data(week_start, week_end):
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()

        # Fetch Midas timesheet data
        cursor.execute('''
            SELECT 
                wenco_id,
                first_name,
                last_name,
                SUM(hours) as total_hours
            FROM 
                midas_timesheet
            WHERE 
                date BETWEEN ? AND ?
            GROUP BY 
                wenco_id, first_name, last_name
        ''', (week_start, week_end))
        midas_timesheet = cursor.fetchall()

        # Fetch Big O timesheet data
        cursor.execute('''
            SELECT 
                wenco_id,
                first_name,
                last_name,
                SUM(hours) as total_hours
            FROM 
                bigo_timesheet
            WHERE 
                date BETWEEN ? AND ?
            GROUP BY 
                wenco_id, first_name, last_name
        ''', (week_start, week_end))
        bigo_timesheet = cursor.fetchall()

        all_timesheet = midas_timesheet + bigo_timesheet

        # Insert data into wenco_timesheet table
        for wenco_id, first_name, last_name, total_hours in all_timesheet:
            total_hours = total_hours if total_hours is not None else 0
            overtime_hours = max(0, total_hours - 40)
            cursor.execute('''
                INSERT INTO wenco_timesheet (wenco_id, week_start, week_end, first_name, last_name, total_hours, overtime_hours)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (wenco_id, week_start, week_end, first_name, last_name, total_hours, overtime_hours))

        conn.commit()

if __name__ == "__main__":
    create_wenco_timesheet_table()

    # Fetch all unique week start and end dates
    weeks = fetch_week_ranges()

    # Iterate through each week range and populate timesheet data
    for week_start, week_end in weeks:
        fetch_and_insert_timesheet_data(week_start, week_end)
