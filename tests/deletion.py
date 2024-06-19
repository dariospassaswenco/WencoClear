from sqlalchemy import create_engine, text
from config.app_settings import ENGINE, MIDAS_SS_TABLE, MIDAS_TIMESHEET_TABLE, MIDAS_TECH_TABLE, BIGO_SS_TABLE, BIGO_TIMESHEET_TABLE, BIGO_TECH_TABLE
import pandas as pd
from datetime import datetime

# Define test data for Midas Sales Summary as DataFrame
midas_ss_test_data = pd.DataFrame([
    {
        'wenco_id': 2,
        'date': '2024-06-14'
    }
])

# Define test data for Midas Timesheet as DataFrame
midas_ts_test_data = pd.DataFrame([
    {
        'wenco_id': 2,
        'date': '2024-06-14',
        'date_entered': '2024-06-13',
        'last_name': 'Doe'
    }
])

# Define test data for Midas Tech Summary as DataFrame
midas_tech_test_data = pd.DataFrame([
    {
        'wenco_id': 2,
        'date': '2024-06-14',
        'last_name': 'Doe'
    }
])

# Define test data for Bigo Sales Summary as DataFrame
bigo_ss_test_data = pd.DataFrame([
    {
        'wenco_id': 14,
        'date': '2024-06-14'
    }
])

# Define test data for Bigo Timesheet as DataFrame
bigo_ts_test_data = pd.DataFrame([
    {
        'wenco_id': 14,
        'date': '2024-06-14',
        'date_entered': '2024-06-13',
        'last_name': 'Smith'
    }
])

# Define test data for Bigo Tech Summary as DataFrame
bigo_tech_test_data = pd.DataFrame([
    {
        'date': '2024-06-14',
        'last_name': 'Smith'
    }
])

# Function to delete existing records for Midas Sales Summary
def delete_existing_records_ss_midas(df):
    with ENGINE.begin() as conn:
        for _, row in df.iterrows():
            query = text(f"DELETE FROM {MIDAS_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date")
            result = conn.execute(query, {'wenco_id': row['wenco_id'], 'date': row['date']})
            print(f"Query executed: DELETE FROM {MIDAS_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date with params wenco_id={row['wenco_id']} and date={row['date']}")
            print(f"Number of rows deleted: {result.rowcount}")

# Function to delete existing records for Midas Timesheet
def delete_existing_records_ts_midas(df):
    with ENGINE.begin() as conn:
        for _, row in df.iterrows():
            query = text(f"SELECT date_entered FROM {MIDAS_TIMESHEET_TABLE} WHERE wenco_id = :wenco_id AND last_name = :last_name AND date = :date")
            result = conn.execute(query, {'wenco_id': row['wenco_id'], 'last_name': row['last_name'], 'date': row['date']}).fetchone()
            print(f"Query executed: {query} with params wenco_id={row['wenco_id']}, last_name={row['last_name']}, date={row['date']}")
            if result:
                existing_date_entered = datetime.strptime(result[0], '%Y-%m-%d')
                new_date_entered = datetime.strptime('2024-06-15', '%Y-%m-%d')
                if new_date_entered > existing_date_entered:
                    delete_query = text(f"DELETE FROM {MIDAS_TIMESHEET_TABLE} WHERE wenco_id = :wenco_id AND last_name = :last_name AND date = :date")
                    delete_result = conn.execute(delete_query, {'wenco_id': row['wenco_id'], 'last_name': row['last_name'], 'date': row['date']})
                    print(f"Deleted existing record for wenco_id {row['wenco_id']}, last_name {row['last_name']} and date {row['date']}")
                    print(f"Number of rows deleted: {delete_result.rowcount}")
                else:
                    print(f"No deletion needed: new_date_entered ({new_date_entered}) is not greater than existing_date_entered ({existing_date_entered})")
            else:
                print(f"No matching record found for wenco_id={row['wenco_id']}, last_name={row['last_name']}, date={row['date']}")

# Function to delete existing records for Midas Tech Summary
def delete_existing_records_tech_midas(df):
    with ENGINE.begin() as conn:
        for _, row in df.iterrows():
            query = text(f"DELETE FROM {MIDAS_TECH_TABLE} WHERE wenco_id = :wenco_id AND date = :date AND last_name = :last_name")
            result = conn.execute(query, {'wenco_id': row['wenco_id'], 'date': row['date'], 'last_name': row['last_name']})
            print(f"Query executed: DELETE FROM {MIDAS_TECH_TABLE} WHERE wenco_id = :wenco_id AND date = :date AND last_name = :last_name with params wenco_id={row['wenco_id']}, date={row['date']}, last_name={row['last_name']}")
            print(f"Number of rows deleted: {result.rowcount}")

# Function to delete existing records for Bigo Sales Summary
def delete_existing_records_ss_bigo(df):
    with ENGINE.begin() as conn:
        for _, row in df.iterrows():
            query = text(f"DELETE FROM {BIGO_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date")
            result = conn.execute(query, {'wenco_id': row['wenco_id'], 'date': row['date']})
            print(f"Query executed: DELETE FROM {BIGO_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date with params wenco_id={row['wenco_id']} and date={row['date']}")
            print(f"Number of rows deleted: {result.rowcount}")

# Function to delete existing records for Bigo Timesheet
def delete_existing_records_ts_bigo(df):
    with ENGINE.begin() as conn:
        for _, row in df.iterrows():
            query = text(f"SELECT date_entered FROM {BIGO_TIMESHEET_TABLE} WHERE wenco_id = :wenco_id AND last_name = :last_name AND date = :date")
            result = conn.execute(query, {'wenco_id': row['wenco_id'], 'last_name': row['last_name'], 'date': row['date']}).fetchone()
            print(f"Query executed: {query} with params wenco_id={row['wenco_id']}, last_name={row['last_name']}, date={row['date']}")
            if result:
                existing_date_entered = datetime.strptime(result[0], '%Y-%m-%d')
                new_date_entered = datetime.strptime('2024-06-15', '%Y-%m-%d')
                if new_date_entered > existing_date_entered:
                    delete_query = text(f"DELETE FROM {BIGO_TIMESHEET_TABLE} WHERE wenco_id = :wenco_id AND last_name = :last_name AND date = :date")
                    delete_result = conn.execute(delete_query, {'wenco_id': row['wenco_id'], 'last_name': row['last_name'], 'date': row['date']})
                    print(f"Deleted existing record for wenco_id {row['wenco_id']}, last_name {row['last_name']} and date {row['date']}")
                    print(f"Number of rows deleted: {delete_result.rowcount}")
                else:
                    print(f"No deletion needed: new_date_entered ({new_date_entered}) is not greater than existing_date_entered ({existing_date_entered})")
            else:
                print(f"No matching record found for wenco_id={row['wenco_id']}, last_name={row['last_name']}, date={row['date']}")

# Function to delete existing records for Bigo Tech Summary
def delete_existing_records_tech_bigo(df):
    with ENGINE.begin() as conn:
        for _, row in df.iterrows():
            query = text(f"DELETE FROM {BIGO_TECH_TABLE} WHERE date = :date AND last_name = :last_name")
            result = conn.execute(query, {'date': row['date'], 'last_name': row['last_name']})
            print(f"Query executed: DELETE FROM {BIGO_TECH_TABLE} WHERE date = :date AND last_name = :last_name with params date={row['date']} and last_name={row['last_name']}")
            print(f"Number of rows deleted: {result.rowcount}")

# Delete existing records
delete_existing_records_ss_midas(midas_ss_test_data)
delete_existing_records_ts_midas(midas_ts_test_data)
delete_existing_records_tech_midas(midas_tech_test_data)
delete_existing_records_ss_bigo(bigo_ss_test_data)
delete_existing_records_ts_bigo(bigo_ts_test_data)
delete_existing_records_tech_bigo(bigo_tech_test_data)
