import pandas as pd
import sqlite3
from sqlalchemy import create_engine, text
from config.app_settings import ENGINE, CLEAR_DATABASE_PATH
from contextlib import closing
from datetime import datetime


def insert_employees(df):
    """
    Inserts employee data from a dataframe into the database.

    :param df: DataFrame containing employee data
    """
    try:
        conn = sqlite3.connect(CLEAR_DATABASE_PATH)
        cursor = conn.cursor()

        # Clear existing data
        cursor.execute("DELETE FROM employees")

        # Fetch position_id and type_id mappings from the database
        position_map = {row[0]: row[1] for row in cursor.execute("SELECT title, position_id FROM positions")}
        type_map = {row[0]: row[1] for row in cursor.execute("SELECT type_name, type_id FROM store_types")}

        print("Position Map:", position_map)
        print("Type Map:", type_map)

        # Iterate over the dataframe and insert each row into the database
        for _, row in df.iterrows():
            position_id = position_map.get(row['position_id'])
            type_id = type_map.get(row['type_id'])
            wenco_id = row['wenco_id'] if not pd.isna(row['wenco_id']) else None

            if position_id is None:
                print(f"Warning: Position '{row['position_id']}' not found in the database.")
                continue

            if type_id is None:
                print(f"Warning: Store type '{row['type_id']}' not found in the database.")
                continue

            cursor.execute(
                "INSERT INTO employees (first_name, last_name, wenco_id, type_id, position_id) VALUES (?, ?, ?, ?, ?)",
                (row['first_name'], row['last_name'], wenco_id, type_id, position_id)
            )

        conn.commit()
        conn.close()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data into the database: {e}")

def get_all_employees():
    try:
        conn = sqlite3.connect(CLEAR_DATABASE_PATH)
        query = """
            SELECT e.first_name, e.last_name, s.type_name, p.title, e.wenco_id
            FROM employees e
            JOIN store_types s ON e.type_id = s.type_id
            JOIN positions p ON e.position_id = p.position_id
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching employees: {e}")
        return pd.DataFrame()

def get_db_connection():
    return sqlite3.connect(CLEAR_DATABASE_PATH)

def query_timesheet_discrepancies(store: str, start_date: str, end_date: str):
    if store.lower() == "bigo":
        timesheet_query = """
            SELECT first_name, last_name
            FROM bigo_timesheet
            WHERE date BETWEEN ? AND ?;
        """
    elif store.lower() == "midas":
        timesheet_query = """
            SELECT first_name, last_name
            FROM midas_timesheet
            WHERE date BETWEEN ? AND ?;
        """
    else:
        raise ValueError("Invalid store type. Only 'bigo' and 'midas' are supported.")

    employee_query = """
        SELECT first_name, last_name
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

def get_employee_discrepancies(start_date, end_date):
    # Fetch discrepancies for both stores
    bigo_discrepancies = query_timesheet_discrepancies('bigo', start_date, end_date)
    midas_discrepancies = query_timesheet_discrepancies('midas', start_date, end_date)

    # Combine the discrepancies
    discrepancies = bigo_discrepancies.union(midas_discrepancies)

    # Create a DataFrame with the discrepancy information
    df = pd.DataFrame(discrepancies, columns=['first_name', 'last_name'])
    df['wenco_id'] = pd.NA
    df['type_id'] = pd.NA
    df['position_id'] = pd.NA

    return df


def insert_discrepancy_employees(df):
    """
    Inserts employee data from a dataframe into the database.

    :param df: DataFrame containing employee data in the format
               first_name, last_name, wenco_id, type_name, position_name
    """
    try:
        with closing(sqlite3.connect(CLEAR_DATABASE_PATH)) as conn:
            cursor = conn.cursor()

            # Fetch position_id and type_id mappings from the database
            position_map = {row[0]: row[1] for row in cursor.execute("SELECT title, position_id FROM positions")}
            type_map = {row[0]: row[1] for row in cursor.execute("SELECT type_name, type_id FROM store_types")}

            print("Position Map:", position_map)
            print("Type Map:", type_map)

            for _, row in df.iterrows():
                type_id = type_map.get(row['type_name'])
                position_id = position_map.get(row['position_name'])
                wenco_id = row['wenco_id'] if not pd.isna(row['wenco_id']) else None

                if type_id is None:
                    print(f"Warning: Store type '{row['type_name']}' not found in the database.")
                    continue

                if position_id is None:
                    print(f"Warning: Position '{row['position_name']}' not found in the database.")
                    continue

                if type_id and position_id:
                    cursor.execute(
                        "INSERT INTO employees (first_name, last_name, wenco_id, type_id, position_id) VALUES (?, ?, ?, ?, ?)",
                        (row['first_name'], row['last_name'], wenco_id, type_id, position_id)
                    )

            conn.commit()
            print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data into the database: {e}")

def get_store_types():
    conn = sqlite3.connect(CLEAR_DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT type_name FROM store_types")
    store_types = [row[0] for row in cursor.fetchall()]
    conn.close()
    return store_types

def get_positions():
    conn = sqlite3.connect(CLEAR_DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM positions")
    positions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return positions

def test_employee_discrepancies_insert():
    test_data = {
        'first_name': ['John', 'Jane', 'Doe'],
        'last_name': ['Doe', 'Smith', 'Johnson'],
        'wenco_id': [123, 456, 789],
        'type_name': ['Midas', 'Bigo', 'Midas'],
        'position_name': ['GS', 'Service Advisor', 'Manager']
    }
    df = pd.DataFrame(test_data)
    insert_discrepancy_employees(df)

def test_employee_discrepancies():
    start_date = '2024-06-01'
    end_date = '2024-06-10'
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    print("Testing get_employee_discrepancies:")
    discrepancies = get_employee_discrepancies(start_date, end_date)
    print(discrepancies)


# Test the function
if __name__ == "__main__":
    print(get_all_employees())