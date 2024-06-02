import sqlite3
from datetime import datetime, timedelta
from contextlib import closing
from database.db_helpers import get_db_connection

def get_week_start_end(date_obj):
    start = date_obj - timedelta(days=date_obj.weekday() + 1)
    end = start + timedelta(day = 6)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create wenco_timesheet table
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

    # Create kpi_weekly_summary table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kpi_weekly_summary (
            wenco_id INTEGER,
            dm_id INTEGER,
            week_start DATE,
            week_end DATE,
            revenue FLOAT,
            gross_profit FLOAT,
            labor_revenue FLOAT,
            cars INTEGER,
            alignments INTEGER,
            tires INTEGER,
            nitrogen INTEGER,
            gs_hours_worked FLOAT,
            tech_hours_worked FLOAT,
            tech_hours_flagged FLOAT,
            gs_overtime FLOAT,
            tech_overtime FLOAT,
            PRIMARY KEY (wenco_id, week_start, week_end)
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

def fetch_and_update_kpi_data(week_start, week_end):
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()

        # Sales Data
        cursor.execute('''
            SELECT 
                wenco_id, 
                SUM(total_revenue_w_supplies) as revenue
            FROM 
                bigo_sales_summary
            WHERE 
                date BETWEEN ? AND ?
            GROUP BY 
                wenco_id
        ''', (week_start, week_end))
        bigo_sales = cursor.fetchall()

        cursor.execute('''
            SELECT 
                wenco_id, 
                SUM(total_revenue_w_supplies) as revenue
            FROM 
                midas_sales_summary
            WHERE 
                date BETWEEN ? AND ?
            GROUP BY 
                wenco_id
        ''', (week_start, week_end))
        midas_sales = cursor.fetchall()

        all_sales = bigo_sales + midas_sales

        # Gross Profit
        cursor.execute('''
            SELECT 
                wenco_id, 
                SUM(gross_profit_w_supplies) as gross_profit
            FROM 
                bigo_sales_summary
            WHERE 
                date BETWEEN ? AND ?
            GROUP BY 
                wenco_id
        ''', (week_start, week_end))
        bigo_gp = cursor.fetchall()

        cursor.execute('''
            SELECT 
                wenco_id, 
                SUM(gp_w_supplies) as gross_profit
            FROM 
                midas_sales_summary
            WHERE 
                date BETWEEN ? AND ?
            GROUP BY 
                wenco_id
        ''', (week_start, week_end))
        midas_gp = cursor.fetchall()

        all_gp = bigo_gp + midas_gp

        # Labor Revenue
        cursor.execute('''
            SELECT 
                wenco_id, 
                SUM(labor_revenue) as labor_revenue
            FROM 
                bigo_sales_summary
            WHERE 
                date BETWEEN ? AND ?
            GROUP BY 
                wenco_id
        ''', (week_start, week_end))
        bigo_lr = cursor.fetchall()

        cursor.execute('''
            SELECT 
                wenco_id, 
                SUM(labor_revenue) as labor_revenue
            FROM 
                midas_sales_summary
            WHERE 
                date BETWEEN ? AND ?
            GROUP BY 
                wenco_id
        ''', (week_start, week_end))
        midas_lr = cursor.fetchall()

        all_lr = bigo_lr + midas_lr

        # Cars
        cursor.execute('''
            SELECT 
                wenco_id, 
                SUM(car_count) as cars
            FROM 
                bigo_sales_summary
            WHERE 
                date BETWEEN ? AND ?
            GROUP BY 
                wenco_id
        ''', (week_start, week_end))
        bigo_cars = cursor.fetchall()

        cursor.execute('''
            SELECT 
                wenco_id, 
                SUM(car_count) as cars
            FROM 
                midas_sales_summary
            WHERE 
                date BETWEEN ? AND ?
            GROUP BY 
                wenco_id
        ''', (week_start, week_end))
        midas_cars = cursor.fetchall()

        all_cars = bigo_cars + midas_cars

        # Alignments, Tires, Nitrogen for Big O
        cursor.execute('''
            SELECT 
                wenco_id, 
                SUM(alignment_count) as alignments,
                SUM(tire_count) as tires,
                SUM(nitrogen_count) as nitrogen
            FROM 
                bigo_sales_summary
            WHERE 
                date BETWEEN ? AND ?
            GROUP BY 
                wenco_id
        ''', (week_start, week_end))
        bigo_details = cursor.fetchall()

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

        # Insert or update data into KPI table
        for store_number, revenue in all_sales:
            cursor.execute('SELECT dm_id FROM stores WHERE wenco_id = ?', (store_number,))
            dm_id = cursor.fetchone()[0]

            gross_profit = next((gp for s, gp in all_gp if s == store_number), 0)
            labor_revenue = next((lr for s, lr in all_lr if s == store_number), 0)
            cars = next((c for s, c in all_cars if s == store_number), 0)

            alignments = next((a for s, a, t, n in bigo_details if s == store_number), 0)
            tires = next((t for s, a, t, n in bigo_details if s == store_number), 0)
            nitrogen = next((n for s, a, t, n in bigo_details if s == store_number), 0)

            gs_hours_worked = next((gh for s, gh, go in gs_hours if s == store_number), 0)
            gs_overtime = next((go for s, gh, go in gs_hours if s == store_number), 0)
            tech_hours_worked = next((th for s, th, to in tech_hours if s == store_number), 0)
            tech_overtime = next((to for s, th, to in tech_hours if s == store_number), 0)
            tech_hours_flagged = next((tf for s, tf in all_tech_flagged if s == store_number), 0)

            cursor.execute('''
                INSERT INTO kpi_weekly_summary (wenco_id, dm_id, week_start, week_end, revenue, gross_profit, labor_revenue, cars, alignments, tires, nitrogen, gs_hours_worked, tech_hours_worked, tech_hours_flagged, gs_overtime, tech_overtime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(wenco_id, week_start, week_end) DO UPDATE SET
                revenue=excluded.revenue,
                gross_profit=excluded.gross_profit,
                labor_revenue=excluded.labor_revenue,
                cars=excluded.cars,
                alignments=excluded.alignments,
                tires=excluded.tires,
                nitrogen=excluded.nitrogen,
                gs_hours_worked=excluded.gs_hours_worked,
                tech_hours_worked=excluded.tech_hours_worked,
                tech_hours_flagged=excluded.tech_hours_flagged,
                gs_overtime=excluded.gs_overtime,
                tech_overtime=excluded.tech_overtime
            ''', (
                store_number, dm_id, week_start, week_end, revenue, gross_profit, labor_revenue, cars, alignments, tires,
                nitrogen, gs_hours_worked, tech_hours_worked, tech_hours_flagged, gs_overtime, tech_overtime))

        conn.commit()

if __name__ == "__main__":
    create_tables()

    # Fetch all unique week start and end dates
    weeks = fetch_week_ranges()

    # Iterate through each week range and update timesheet data
    for week_start, week_end in weeks:
        fetch_and_insert_timesheet_data(week_start, week_end)
        fetch_and_update_kpi_data(week_start, week_end)