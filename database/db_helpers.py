import sqlite3
from contextlib import closing
from typing import List
from config.settings import DATABASE_PATH
from database.models import BigoSalesSummary, BigoTechSummary, BigoTimesheet, MidasSalesSummary, MidasTechSummary, MidasTimesheet

def get_db_connection():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_PATH)

def employee_exists(first_name: str, last_name: str) -> int:
    """Check if an employee exists in the database and return the employee_id if they do."""
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?
            """, (first_name, last_name)
        )
        result = cursor.fetchone()
        return result[0] if result else None

def insert_bigo_sales_summary(summaries: List[BigoSalesSummary]):
    """Insert a list of Bigo sales summaries into the database"""
    with closing(get_db_connection()) as conn:
        with conn:
            conn.executemany(
                """
                INSERT INTO bigo_sales_summary (wenco_id, date, car_count, tire_count, alignment_count, nitrogen_count, parts_revenue, billed_labor_quantity, billed_labor_revenue, supplies, total_revenue_w_supplies, gross_profit_no_supplies, gross_profit_w_supplies)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [(s.wenco_id, s.date, s.car_count, s.tire_count, s.alignment_count, s.nitrogen_count, s.parts_revenue,
                  s.billed_labor_quantity, s.billed_labor_revenue, s.supplies, s.total_revenue_w_supplies,
                  s.gross_profit_no_supplies, s.gross_profit_w_supplies) for s in summaries]
            )

def insert_bigo_tech_summary(summaries: List[BigoTechSummary]):
    """Insert a list of Bigo tech summaries into the database."""
    with closing(get_db_connection()) as conn:
        with conn:
            for summary in summaries:
                employee_id = employee_exists(summary.first_name, summary.last_name)
                if employee_id:
                    conn.execute(
                        """
                        INSERT INTO bigo_tech_summary (employee_id, wenco_id, start_date, end_date, car_count, tire_count, alignment_count, nitrogen_count, parts_revenue, billed_labor_quantity, billed_labor_revenue, total_revenue, gross_profit)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (employee_id, summary.wenco_id, summary.start_date, summary.end_date, summary.car_count, summary.tire_count,
                         summary.alignment_count, summary.nitrogen_count, summary.parts_revenue, summary.billed_labor_quantity,
                         summary.billed_labor_revenue, summary.total_revenue, summary.gross_profit)
                    )
                else:
                    print(f"Error: Employee {summary.first_name} {summary.last_name} does not exist in the database.")

def insert_bigo_timesheets(timesheets: List[BigoTimesheet]):
    """Insert a list of Bigo timesheets into the database."""
    with closing(get_db_connection()) as conn:
        with conn:
            for timesheet in timesheets:
                employee_id = employee_exists(timesheet.first_name, timesheet.last_name)
                if employee_id:
                    conn.execute(
                        """
                        INSERT INTO bigo_timesheet (wenco_id, employee_id, date, hours)
                        VALUES (?, ?, ?, ?)
                        """,
                        (timesheet.wenco_id, employee_id, timesheet.date, timesheet.hours)
                    )
                else:
                    print(f"Error: Employee {timesheet.first_name} {timesheet.last_name} does not exist in the database.")

def insert_midas_sales_summaries(summaries: List[MidasSalesSummary]):
    """Insert a list of Midas sales summaries into the database."""
    with closing(get_db_connection()) as conn:
        with conn:
            conn.executemany(
                """
                INSERT INTO midas_sales_summary (wenco_id, date, car_count, parts_revenue, labor_revenue, tire_revenue, supplies_revenue, parts_cost, labor_cost, tire_cost, total_revenue_w_supplies, parts_gp, labor_gp, tire_gp, gp_w_supplies)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [(s.wenco_id, s.date, s.car_count, s.parts_revenue, s.labor_revenue, s.tire_revenue, s.supplies_revenue, s.parts_cost, s.labor_cost, s.tire_cost, s.total_revenue_w_supplies, s.parts_gp, s.labor_gp, s.tire_gp, s.gp_w_supplies) for s in summaries]
            )

def insert_midas_tech_summaries(summaries: List[MidasTechSummary]):
    """Insert a list of Midas tech summaries into the database."""
    with closing(get_db_connection()) as conn:
        with conn:
            for summary in summaries:
                employee_id = employee_exists(summary.first_name, summary.last_name)
                if employee_id:
                    conn.execute(
                        """
                        INSERT INTO midas_tech_summary (employee_id, wenco_id, start_date, end_date, store_number, time, labor_sales, part_sales, no_of_ros, total_sales)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (employee_id, summary.wenco_id, summary.start_date, summary.end_date, summary.store_number, summary.time,
                         summary.labor_sales, summary.part_sales, summary.no_of_ros, summary.total_sales)
                    )
                else:
                    print(f"Error: Employee {summary.first_name} {summary.last_name} does not exist in the database.")

def insert_midas_timesheets(timesheets: List[MidasTimesheet]):
    """Insert a list of Midas timesheets into the database."""
    with closing(get_db_connection()) as conn:
        with conn:
            for timesheet in timesheets:
                employee_id = employee_exists(timesheet.first_name, timesheet.last_name)
                if employee_id:
                    conn.execute(
                        """
                        INSERT INTO midas_timesheet (wenco_id, employee_id, date, hours)
                        VALUES (?, ?, ?, ?)
                        """,
                        (timesheet.wenco_id, employee_id, timesheet.date, timesheet.hours)
                    )
                else:
                    print(f"Error: Employee {timesheet.first_name} {timesheet.last_name} does not exist in the database.")
