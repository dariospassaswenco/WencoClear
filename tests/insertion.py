from datetime import datetime, timedelta
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float, text
import pandas as pd

# Assuming ENGINE is already defined in your config.app_settings
from config.app_settings import ENGINE, MIDAS_SS_TABLE, MIDAS_TIMESHEET_TABLE, MIDAS_TECH_TABLE, BIGO_SS_TABLE, BIGO_TIMESHEET_TABLE, BIGO_TECH_TABLE

# Define test data for Midas Sales Summary as DataFrame
midas_ss_test_data = pd.DataFrame([
    {
        'wenco_id': 2,
        'date': '2024-06-14',
        'car_count': 10,
        'parts_revenue': 1000.0,
        'labor_revenue': 2000.0,
        'tire_revenue': 500.0,
        'supplies_revenue': 100.0,
        'parts_cost': 500.0,
        'labor_cost': 1000.0,
        'tire_cost': 250.0,
        'total_revenue_w_supplies': 3600.0,
        'parts_gp': 500.0,
        'labor_gp': 1000.0,
        'tire_gp': 250.0,
        'gp_w_supplies': 1850.0
    }
])

# Define test data for Midas Timesheet as DataFrame
midas_ts_test_data = pd.DataFrame([
    {
        'wenco_id': 2,
        'date': '2024-06-14',
        'date_entered': '2024-06-13',
        'first_name': 'John',
        'last_name': 'Doe',
        'hours': 8.0
    }
])

# Define test data for Midas Tech Summary as DataFrame
midas_tech_test_data = pd.DataFrame([
    {
        'wenco_id': 2,
        'first_name': 'John',
        'last_name': 'Doe',
        'date': '2024-06-14',
        'tech_hours_flagged': 8.0,
        'labor_revenue': 2000.0,
        'part_revenue': 1000.0,
        'car_count': 10,
        'total_revenue': 3000.0
    }
])

# Define test data for Bigo Sales Summary as DataFrame
bigo_ss_test_data = pd.DataFrame([
    {
        'wenco_id': 14,
        'date': '2024-06-14',
        'car_count': 10,
        'tire_count': 5,
        'alignment_count': 2,
        'nitrogen_count': 1,
        'parts_revenue': 1000.0,
        'labor_quantity': 8.0,
        'labor_revenue': 2000.0,
        'supplies_revenue': 100.0,
        'total_revenue_w_supplies': 3100.0,
        'gross_profit_no_supplies': 1800.0,
        'gross_profit_w_supplies': 1900.0
    }
])

# Define test data for Bigo Timesheet as DataFrame
bigo_ts_test_data = pd.DataFrame([
    {
        'wenco_id': 14,
        'date': '2024-06-14',
        'date_entered': '2024-06-13',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'hours': 8.0
    }
])

# Define test data for Bigo Tech Summary as DataFrame
bigo_tech_test_data = pd.DataFrame([
    {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'date': '2024-06-14',
        'car_count': 10,
        'tire_count': 5,
        'alignment_count': 2,
        'nitrogen_count': 1,
        'parts_revenue': 1000.0,
        'tech_hours_flagged': 8.0,
        'labor_revenue': 2000.0,
        'total_revenue': 3000.0,
        'gross_profit': 1800.0
    }
])

# Function to insert test data as DataFrame
def insert_test_data(df, table_name):
    df.to_sql(table_name, ENGINE, if_exists='append', index=False)
    print(f"Inserted test data into {table_name}")

# Insert test data
insert_test_data(midas_ss_test_data, MIDAS_SS_TABLE)
insert_test_data(midas_ts_test_data, MIDAS_TIMESHEET_TABLE)
insert_test_data(midas_tech_test_data, MIDAS_TECH_TABLE)
insert_test_data(bigo_ss_test_data, BIGO_SS_TABLE)
insert_test_data(bigo_ts_test_data, BIGO_TIMESHEET_TABLE)
insert_test_data(bigo_tech_test_data, BIGO_TECH_TABLE)
