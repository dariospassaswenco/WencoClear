from database.db_helpers import get_db_connection
from contextlib import closing

def query_sales_summaries(store: str, start_date: str, end_date: str):
    if store.lower() == "bigo":
        query = """
            SELECT 
                "Store Number", 
                SUM("Total Revenue w/ Supplies") as Total_Revenue_with_Supplies
            FROM 
                bigo_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number";
        """
    elif store.lower() == "midas":
        query = """
            SELECT 
                "Store Number", 
                SUM("Total Revenue w/ Supplies") as Total_Revenue_with_Supplies
            FROM 
                midas_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number";
        """
    else:
        raise ValueError("Invalid store type. Only 'bigo' and 'midas' are supported.")

    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

    return results

def query_cars_summaries(store: str, start_date: str, end_date: str):
    if store.lower() == "bigo":
        query = """
            SELECT 
                "Store Number", 
                SUM("Car Count") as Total_Car_Count
            FROM 
                bigo_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number";
        """
    elif store.lower() == "midas":
        query = """
            SELECT 
                "Store Number", 
                SUM("Car Count") as Total_Car_Count
            FROM 
                midas_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number";
        """
    else:
        raise ValueError("Invalid store type. Only 'bigo' and 'midas' are supported.")

    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

    return results

def query_gp_summaries(store: str, start_date: str, end_date: str):
    if store.lower() == "bigo":
        query = """
            SELECT 
                "Store Number", 
                SUM("Gross Profit w/ Supplies") as Total_GP
            FROM 
                bigo_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number";
        """
    elif store.lower() == "midas":
        query = """
            SELECT 
                "Store Number", 
                SUM("GP w/ Supplies") as Total_GP
            FROM 
                midas_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number";
        """
    else:
        raise ValueError("Invalid store type. Only 'bigo' and 'midas' are supported.")

    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

    return results

def query_labor_revenue_summaries(store: str, start_date: str, end_date: str):
    if store.lower() == "bigo":
        query = """
            SELECT 
                "Store Number", 
                SUM("Billed Labor Revenue") as Total_Labor_Revenue
            FROM 
                bigo_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number";
        """
    elif store.lower() == "midas":
        query = """
            SELECT 
                "Store Number", 
                SUM("Labor Revenue") as Total_Labor_Revenue
            FROM 
                midas_sales_summary
            WHERE 
                Date BETWEEN ? AND ?
            GROUP BY 
                "Store Number";
        """
    else:
        raise ValueError("Invalid store type. Only 'bigo' and 'midas' are supported.")

    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

    return results

def query_gs_hours(store: str, start_date: str, end_date: str):
    if store.lower() == "bigo":
        query = """
            SELECT 
                t.Store, 
                SUM(t.Hours) as Total_GS_Hours
            FROM 
                bigo_timesheet t
            JOIN 
                employees e ON t.first_name = e.first_name AND t.last_name = e.last_name
            JOIN 
                positions p ON e.position_id = p.position_id
            WHERE 
                p.title = 'GS'
                AND t.Date BETWEEN ? AND ?
            GROUP BY 
                t.Store;
        """
    elif store.lower() == "midas":
        query = """
            SELECT 
                t.Store, 
                SUM(t.hours) as Total_GS_Hours
            FROM 
                midas_timesheet t
            JOIN 
                employees e ON t.first_name = e.first_name AND t.last_name = e.last_name
            JOIN 
                positions p ON e.position_id = p.position_id
            WHERE 
                p.title = 'GS'
                AND t.Date BETWEEN ? AND ?
            GROUP BY 
                t.Store;
        """
    else:
        raise ValueError("Invalid store type. Only 'bigo' and 'midas' are supported.")

    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

    return results

def query_tech_hours(store: str, start_date: str, end_date: str):
    if store.lower() == "bigo":
        query = """
            SELECT 
                t.Store, 
                SUM(t.Hours) as Total_Tech_Hours
            FROM 
                bigo_timesheet t
            JOIN 
                employees e ON t.first_name = e.first_name AND t.last_name = e.last_name
            JOIN 
                positions p ON e.position_id = p.position_id
            WHERE 
                p.title = 'Tech'
                AND t.Date BETWEEN ? AND ?
            GROUP BY 
                t.Store;
        """
    elif store.lower() == "midas":
        query = """
            SELECT 
                t.Store, 
                SUM(t.hours) as Total_Tech_Hours
            FROM 
                midas_timesheet t
            JOIN 
                employees e ON t.first_name = e.first_name AND t.last_name = e.last_name
            JOIN 
                positions p ON e.position_id = p.position_id
            WHERE 
                p.title = 'Tech'
                AND t.Date BETWEEN ? AND ?
            GROUP BY 
                t.Store;
        """
    else:
        raise ValueError("Invalid store type. Only 'bigo' and 'midas' are supported.")

    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

    return results

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

def query_tech_flagged_hours(store: str, start_date: str, end_date: str):
    if store.lower() == "bigo":
        query = """
                SELECT 
                    e.store_id as Store,
                    SUM(t."Billed Labor Quantity") as Total_Tech_Hours
                FROM 
                    bigo_tech_summary t
                JOIN 
                    employees e ON t."First Name" = e.first_name AND t."Last Name" = e.last_name
                WHERE 
                    t."Start Date" = ? AND t."End Date" = ?
                GROUP BY 
                    e.store_id;
            """
    elif store.lower() == "midas":
        query = """
            SELECT 
                "Store #",
                SUM(Time) as Total_Tech_Hours
            FROM 
                midas_tech_summary
            WHERE 
                "Start Date" = ? AND "End Date" = ?
            GROUP BY 
                "Store #";
        """
    else:
        raise ValueError("Invalid store type. Only 'bigo' and 'midas' are supported.")

    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

    return results


def query_bigo_sales_details(start_date: str, end_date: str):
    query = """
        SELECT 
            "Store Number", 
            SUM("Alignment Count") as Total_Alignments,
            SUM("Tire Count") as Total_Tires,
            SUM("Nitrogen Count") as Total_Nitrogens
        FROM 
            bigo_sales_summary
        WHERE 
            Date BETWEEN ? AND ?
        GROUP BY 
            "Store Number";
    """

    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

    return results

