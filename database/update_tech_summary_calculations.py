import sqlite3
from datetime import datetime, timedelta
from contextlib import closing
from database.db_helpers import get_db_connection

def get_week_start_end(date_str):
    end_date = datetime.strptime(date_str, "%Y-%m-%d")
    start_date = end_date - timedelta(days=end_date.weekday() + 1)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def fetch_and_update_kpi_data(week_start, week_end):
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()

        # GS Hours Worked and Overtime
        cursor.execute('''
            SELECT 
                t.wenco_id, 
                SUM(t.total_hours) as gs_hours_worked,
                SUM(t.overtime_hours) as gs_overtime
            FROM 
                wenco_timesheet t
            JOIN 
                employees e ON t.first_name = e.first_name AND t.last_name = e.last_name
            JOIN 
                positions p ON e.position_id = p.position_id
            WHERE 
                p.title = 'GS'
                AND t.week_start = ?
                AND t.week_end = ?
            GROUP BY 
                t.wenco_id
        ''', (week_start, week_end))
        gs_hours = cursor.fetchall()
        print("GS Hours: ", gs_hours)

        # Tech Hours Worked and Overtime
        cursor.execute('''
            SELECT 
                t.wenco_id, 
                SUM(t.total_hours) as tech_hours_worked,
                SUM(t.overtime_hours) as tech_overtime
            FROM 
                wenco_timesheet t
            JOIN 
                employees e ON t.first_name = e.first_name AND t.last_name = e.last_name
            JOIN 
                positions p ON e.position_id = p.position_id
            WHERE 
                p.title = 'Tech'
                AND t.week_start = ?
                AND t.week_end = ?
            GROUP BY 
                t.wenco_id
        ''', (week_start, week_end))
        tech_hours = cursor.fetchall()
        print("Tech Hours: ", tech_hours)

        # Tech Hours Flagged
        cursor.execute('''
            SELECT 
                e.store_id as wenco_id,
                SUM(t.tech_hours_flagged) as tech_hours_flagged
            FROM 
                bigo_tech_summary t
            JOIN 
                employees e ON t.first_name = e.first_name AND t.last_name = e.last_name
            WHERE 
                t.start_date = ? AND t.end_date = ?
            GROUP BY 
                e.store_id
        ''', (week_start, week_end))
        bigo_tech_flagged = cursor.fetchall()
        print("Bigo Tech Flagged: ", bigo_tech_flagged)

        cursor.execute('''
            SELECT 
                wenco_id,
                SUM(tech_hours_flagged) as tech_hours_flagged
            FROM 
                midas_tech_summary
            WHERE 
                start_date = ? AND end_date = ?
            GROUP BY 
                wenco_id
        ''', (week_start, week_end))
        midas_tech_flagged = cursor.fetchall()
        print("Midas Tech Flagged: ", midas_tech_flagged)

        all_tech_flagged = bigo_tech_flagged + midas_tech_flagged
        print("All Tech Flagged: ", all_tech_flagged)

        # Update KPI table with new data and print changes
        for store_number, gs_hours_worked, gs_overtime in gs_hours:
            cursor.execute('''
                SELECT gs_hours_worked, gs_overtime
                FROM kpi_weekly_summary
                WHERE wenco_id = ? AND week_start = ? AND week_end = ?
            ''', (store_number, week_start, week_end))
            existing_record = cursor.fetchone()

            if existing_record:
                print(f"Updating GS hours for store {store_number}: gs_hours_worked={gs_hours_worked}, gs_overtime={gs_overtime}")
                cursor.execute('''
                    UPDATE kpi_weekly_summary
                    SET gs_hours_worked = ?,
                        gs_overtime = ?
                    WHERE wenco_id = ? AND week_start = ? AND week_end = ?
                ''', (gs_hours_worked, gs_overtime, store_number, week_start, week_end))

        for store_number, tech_hours_worked, tech_overtime in tech_hours:
            cursor.execute('''
                SELECT tech_hours_worked, tech_overtime
                FROM kpi_weekly_summary
                WHERE wenco_id = ? AND week_start = ? AND week_end = ?
            ''', (store_number, week_start, week_end))
            existing_record = cursor.fetchone()

            if existing_record:
                print(f"Updating Tech hours for store {store_number}: tech_hours_worked={tech_hours_worked}, tech_overtime={tech_overtime}")
                cursor.execute('''
                    UPDATE kpi_weekly_summary
                    SET tech_hours_worked = ?,
                        tech_overtime = ?
                    WHERE wenco_id = ? AND week_start = ? AND week_end = ?
                ''', (tech_hours_worked, tech_overtime, store_number, week_start, week_end))

        for store_number, tech_hours_flagged in all_tech_flagged:
            cursor.execute('''
                SELECT tech_hours_flagged
                FROM kpi_weekly_summary
                WHERE wenco_id = ? AND week_start = ? AND week_end = ?
            ''', (store_number, week_start, week_end))
            existing_record = cursor.fetchone()

            if existing_record:
                print(f"Updating Tech flagged hours for store {store_number}: tech_hours_flagged={tech_hours_flagged}")
                cursor.execute('''
                    UPDATE kpi_weekly_summary
                    SET tech_hours_flagged = ?
                    WHERE wenco_id = ? AND week_start = ? AND week_end = ?
                ''', (tech_hours_flagged, store_number, week_start, week_end))

        conn.commit()

if __name__ == "__main__":
    week_end_date = input("Enter the week end date (YYYY-MM-DD): ")
    week_start_date, week_end_date = get_week_start_end(week_end_date)
    fetch_and_update_kpi_data(week_start_date, week_end_date)
