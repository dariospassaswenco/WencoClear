import pandas as pd
from sqlalchemy import create_engine
from config.app_settings import ENGINE, MIDAS_STORE_NUMBERS, BIGO_STORE_NUMBERS
import traceback

""" These functions are mostly for the UI for datacheckup view. I dont think they really have any other use because they are so specific for it """

def create_empty_dataframe(start_date, end_date, stores):
    date_range = pd.date_range(start=start_date, end=end_date)
    columns = [date.strftime('%Y-%m-%d') for date in date_range]
    df = pd.DataFrame(index=stores, columns=columns).fillna('')
    return df

def query_sales_summary_data(start_date, end_date, store_type):
    try:
        if store_type == "Midas":
            stores = [f"Midas {store}" for store in MIDAS_STORE_NUMBERS]
            query = f"""
            SELECT wenco_id, date, total_revenue_w_supplies AS revenue
            FROM midas_sales_summary
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            """
        elif store_type == "Bigo":
            stores = [f"Bigo {store}" for store in BIGO_STORE_NUMBERS]
            query = f"""
            SELECT wenco_id, date, total_revenue_w_supplies AS revenue
            FROM bigo_sales_summary
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            """
        else:
            raise ValueError("Invalid store type")

        print(f"Executing query for sales summary data: {query}")  # Debug statement
        result_df = pd.read_sql(query, ENGINE)

        # Create an empty dataframe
        empty_df = create_empty_dataframe(start_date, end_date, stores)

        # Populate the dataframe with query results
        for _, row in result_df.iterrows():
            store = f"{store_type} {row['wenco_id']}"
            date = row['date']
            value = row['revenue']
            if store in empty_df.index and date in empty_df.columns:
                empty_df.at[store, date] = value

        print(f"Query result (formatted): {empty_df.shape}\n{empty_df.head()}")  # Debug statement
        return empty_df
    except Exception as e:
        print(f"Error querying sales summary data: {e}")
        traceback.print_exc()
        return create_empty_dataframe(start_date, end_date, [])

def query_tech_data(start_date, end_date, store_type):
    try:
        if store_type == "Midas":
            stores = [f"Midas {store}" for store in MIDAS_STORE_NUMBERS]
            query = f"""
            SELECT wenco_id, date, last_name
            FROM midas_tech_summary
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            """
        elif store_type == "Bigo":
            stores = [f"Bigo {store}" for store in BIGO_STORE_NUMBERS]
            query = f"""
            SELECT date, last_name
            FROM bigo_tech_summary
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            """
        else:
            raise ValueError("Invalid store type")

        print(f"Executing query for tech data: {query}")  # Debug statement
        result_df = pd.read_sql(query, ENGINE)

        # Create an empty dataframe
        empty_df = create_empty_dataframe(start_date, end_date, stores)

        if store_type == "Midas":
            # Populate the dataframe with query results for Midas
            for _, row in result_df.iterrows():
                store = f"{store_type} {row['wenco_id']}"
                date = row['date']
                value = row['last_name']
                if store in empty_df.index and date in empty_df.columns:
                    empty_df.at[store, date] = value
        elif store_type == "Bigo":
            # Populate the dataframe with query results for Bigo
            for _, row in result_df.iterrows():
                date = row['date']
                value = row['last_name']
                for store in stores:
                    if date in empty_df.columns:
                        empty_df.at[store, date] = value

        print(f"Query result (formatted): {empty_df.shape}\n{empty_df.head()}")  # Debug statement
        return empty_df
    except Exception as e:
        print(f"Error querying tech data: {e}")
        traceback.print_exc()
        return create_empty_dataframe(start_date, end_date, [])


def query_timesheet_data(start_date, end_date, store_type):
    try:
        if store_type == "Midas":
            stores = [f"Midas {store}" for store in MIDAS_STORE_NUMBERS]
            query = f"""
            SELECT wenco_id, date, last_name
            FROM midas_timesheet
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            """
        elif store_type == "Bigo":
            stores = [f"Bigo {store}" for store in BIGO_STORE_NUMBERS]
            query = f"""
            SELECT wenco_id, date, last_name
            FROM bigo_timesheet
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            """
        else:
            raise ValueError("Invalid store type")

        print(f"Executing query for timesheet data: {query}")  # Debug statement
        result_df = pd.read_sql(query, ENGINE)

        # Create an empty dataframe
        empty_df = create_empty_dataframe(start_date, end_date, stores)

        # Populate the dataframe with query results
        for _, row in result_df.iterrows():
            store = f"{store_type} {row['wenco_id']}"
            date = row['date']
            value = row['last_name']
            if store in empty_df.index and date in empty_df.columns:
                empty_df.at[store, date] = value

        print(f"Query result (formatted): {empty_df.shape}\n{empty_df.head()}")  # Debug statement
        return empty_df
    except Exception as e:
        print(f"Error querying timesheet data: {e}")
        traceback.print_exc()
        return create_empty_dataframe(start_date, end_date, [])


def query_sales_by_category_data(start_date, end_date, store_type):
    try:
        if store_type == "Midas":
            stores = [f"Midas {store}" for store in MIDAS_STORE_NUMBERS]
            query = f"""
            SELECT wenco_id, date, category
            FROM midas_sales_by_category
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            """
            column_name = 'category'
        elif store_type == "Bigo":
            stores = [f"Bigo {store}" for store in BIGO_STORE_NUMBERS]
            query = f"""
            SELECT wenco_id, date, sales_category
            FROM bigo_sales_by_category
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            """
            column_name = 'sales_category'
        else:
            raise ValueError("Invalid store type for Sales By Category")

        print(f"Executing query for {store_type} sales by category data: {query}")  # Debug statement
        result_df = pd.read_sql(query, ENGINE)

        # Create an empty dataframe
        empty_df = create_empty_dataframe(start_date, end_date, stores)

        # Populate the dataframe with query results
        for _, row in result_df.iterrows():
            store = f"{store_type} {row['wenco_id']}"
            date = row['date']
            value = row[column_name]
            if store in empty_df.index and date in empty_df.columns:
                if empty_df.at[store, date] == '':
                    empty_df.at[store, date] = value
                else:
                    empty_df.at[store, date] += f", {value}"

        print(f"Query result (formatted): {empty_df.shape}\n{empty_df.head()}")  # Debug statement
        return empty_df
    except Exception as e:
        print(f"Error querying sales by category data: {e}")
        traceback.print_exc()
        return create_empty_dataframe(start_date, end_date, [])

# Test functions for each query
def test_query_sales_summary():
    print("Testing Sales Summary Query...")
    start_date = '2024-06-01'
    end_date = '2024-06-08'
    store_type = 'Midas'  # Change to 'Bigo' for Bigo test
    result_df = query_sales_summary_data(start_date, end_date, store_type)
    print(f"Test Sales Summary Result: {result_df}")

def test_query_tech_data():
    print("Testing Tech Data Query...")
    start_date = '2024-06-01'
    end_date = '2024-06-08'
    store_type = 'Midas'  # Change to 'Bigo' for Bigo test
    result_df = query_tech_data(start_date, end_date, store_type)
    print(f"Test Tech Data Result: {result_df}")

def test_query_timesheet_data():
    print("Testing Timesheet Data Query...")
    start_date = '2024-06-01'
    end_date = '2024-06-08'
    store_type = 'Midas'  # Change to 'Bigo' for Bigo test
    result_df = query_timesheet_data(start_date, end_date, store_type)
    print(f"Test Timesheet Data Result: {result_df}")

def test_query_sales_by_category_data():
    print("Testing Sales By Category Data Query...")
    start_date = '2024-07-08'
    end_date = '2024-07-13'
    store_type = 'Midas'
    result_df = query_sales_by_category_data(start_date, end_date, store_type)
    print(f"Test Sales By Category Data Result:\n{result_df}")

if __name__ == "__main__":
    test_query_sales_summary()
    test_query_tech_data()
    test_query_timesheet_data()
    test_query_sales_by_category_data()
