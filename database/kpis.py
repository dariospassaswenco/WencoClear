import sqlite3
from datetime import datetime, timedelta
from database.db_helpers import get_db_connection
from contextlib import closing


def get_week_start_end(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    start = date_obj - timedelta(days=date_obj.weekday() + 1)
    end = start + timedelta(days=6)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')


def create_kpi_table():
    conn = get_db_connection()
    cursor = conn.cursor()

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
            nitrogen INTEGER
        )
    ''')

    conn.commit()
    conn.close()


def fetch_and_insert_kpi_data(start_date):
    end_date = (datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
    week_start, week_end = get_week_start_end(start_date)

    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()

        # Sales Data
        cursor.execute('''
            SELECT 
                "Store Number", 
                SUM("Total Revenue w/ Supplies") as revenue
            FROM 
                bigo_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number"
        ''', (end_date, start_date))
        bigo_sales = cursor.fetchall()

        cursor.execute('''
            SELECT 
                "Store Number", 
                SUM("Total Revenue w/ Supplies") as revenue
            FROM 
                midas_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number"
        ''', (end_date, start_date))
        midas_sales = cursor.fetchall()

        all_sales = bigo_sales + midas_sales

        # Gross Profit
        cursor.execute('''
            SELECT 
                "Store Number", 
                SUM("Gross Profit w/ Supplies") as gross_profit
            FROM 
                bigo_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number"
        ''', (end_date, start_date))
        bigo_gp = cursor.fetchall()

        cursor.execute('''
            SELECT 
                "Store Number", 
                SUM("GP w/ Supplies") as gross_profit
            FROM 
                midas_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number"
        ''', (end_date, start_date))
        midas_gp = cursor.fetchall()

        all_gp = bigo_gp + midas_gp

        # Labor Revenue
        cursor.execute('''
            SELECT 
                "Store Number", 
                SUM("Billed Labor Revenue") as labor_revenue
            FROM 
                bigo_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number"
        ''', (end_date, start_date))
        bigo_lr = cursor.fetchall()

        cursor.execute('''
            SELECT 
                "Store Number", 
                SUM("Labor Revenue") as labor_revenue
            FROM 
                midas_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number"
        ''', (end_date, start_date))
        midas_lr = cursor.fetchall()

        all_lr = bigo_lr + midas_lr

        # Cars
        cursor.execute('''
            SELECT 
                "Store Number", 
                SUM("Car Count") as cars
            FROM 
                bigo_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number"
        ''', (end_date, start_date))
        bigo_cars = cursor.fetchall()

        cursor.execute('''
            SELECT 
                "Store Number", 
                SUM("Car Count") as cars
            FROM 
                midas_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number"
        ''', (end_date, start_date))
        midas_cars = cursor.fetchall()

        all_cars = bigo_cars + midas_cars

        # Alignments, Tires, Nitrogen for Big O
        cursor.execute('''
            SELECT 
                "Store Number", 
                SUM("Alignment Count") as alignments,
                SUM("Tire Count") as tires,
                SUM("Nitrogen Count") as nitrogen
            FROM 
                bigo_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number"
        ''', (end_date, start_date))
        bigo_details = cursor.fetchall()

        # Insert data into KPI table
        for store_number, revenue in all_sales:
            cursor.execute('SELECT dm_id FROM stores WHERE wenco_id = ?', (store_number,))
            dm_id = cursor.fetchone()[0]

            gross_profit = next((gp for s, gp in all_gp if s == store_number), 0)
            labor_revenue = next((lr for s, lr in all_lr if s == store_number), 0)
            cars = next((c for s, c in all_cars if s == store_number), 0)

            alignments = next((a for s, a, t, n in bigo_details if s == store_number), 0)
            tires = next((t for s, a, t, n in bigo_details if s == store_number), 0)
            nitrogen = next((n for s, a, t, n in bigo_details if s == store_number), 0)

            cursor.execute('''
                INSERT INTO kpi_weekly_summary (wenco_id, dm_id, week_start, week_end, revenue, gross_profit, labor_revenue, cars, alignments, tires, nitrogen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            store_number, dm_id, week_start, week_end, revenue, gross_profit, labor_revenue, cars, alignments, tires,
            nitrogen))

        conn.commit()


if __name__ == "__main__":
    create_kpi_table()
    fetch_and_insert_kpi_data('2024-05-26')
