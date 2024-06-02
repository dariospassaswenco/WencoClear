import configparser
import sqlite3
from config.settings import OLD_DATABASE_PATH, CLEAR_DATABASE_PATH

# Connect to old and new databases
old_conn = sqlite3.connect(OLD_DATABASE_PATH)
new_conn = sqlite3.connect(CLEAR_DATABASE_PATH)

old_cursor = old_conn.cursor()
new_cursor = new_conn.cursor()

# Function to get data from a table
def get_table_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()

# Function to insert data into a table
def insert_data(cursor, table_name, columns, data):
    placeholders = ', '.join(['?'] * len(columns))
    cursor.executemany(
        f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", data
    )

# Define the table mappings between old and new schema
table_mappings = {
    "midas_timesheet": {
        "old": ["Store", "Date", "first_name", "last_name", "hours"],
        "new": ["wenco_id", "date", "first_name", "last_name", "hours"],
        "table": "midas_timesheet"
    },
    "midas_tech_summary": {
        "old": ["First Name", "Last Name", "Start Date", "End Date", "Store #", "Time", "Labor Sales", "Part Sales", "No of ROs", "Total Sales"],
        "new": ["wenco_id", "first_name", "last_name", "start_date", "end_date", "tech_hours_flagged", "labor_revenue", "part_revenue", "car_count", "total_revenue"],
        "table": "midas_tech_summary"
    },
    "midas_sales_summary": {
        "old": ["Store Number", "Date", "Car Count", "Parts Revenue", "Labor Revenue", "Tire Revenue", "Supplies Revenue", "Parts Cost", "Labor Cost", "Tire Cost", "Total Revenue w/ Supplies", "Parts GP", "Labor GP", "Tire GP", "GP w/ Supplies"],
        "new": ["wenco_id", "date", "car_count", "parts_revenue", "labor_revenue", "tire_revenue", "supplies_revenue", "parts_cost", "labor_cost", "tire_cost", "total_revenue_w_supplies", "parts_gp", "labor_gp", "tire_gp", "gp_w_supplies"],
        "table": "midas_sales_summary"
    },
    "bigo_timesheet": {
        "old": ["Store", "Date", "first_name", "last_name", "Hours"],
        "new": ["wenco_id", "date", "first_name", "last_name", "hours"],
        "table": "bigo_timesheet"
    },
    "bigo_tech_summary": {
        "old": ["First Name", "Last Name", "Start Date", "End Date", "Car Count", "Tire Count", "Alignment Count", "Nitrogen Count", "Parts Revenue", "Billed Labor Quantity", "Billed Labor Revenue", "Total Revenue", "Gross Profit"],
        "new": ["first_name", "last_name", "start_date", "end_date", "car_count", "tire_count", "alignment_count", "nitrogen_count", "parts_revenue", "tech_hours_flagged", "labor_revenue", "total_revenue", "gross_profit"],
        "table": "bigo_tech_summary"
    },
    "bigo_sales_summary": {
        "old": ["Store Number", "Date", "Car Count", "Tire Count", "Alignment Count", "Nitrogen Count", "Parts Revenue", "Billed Labor Quantity", "Billed Labor Revenue", "Supplies", "Total Revenue w/ Supplies", "Gross Profit No Supplies", "Gross Profit w/ Supplies"],
        "new": ["wenco_id", "date", "car_count", "tire_count", "alignment_count", "nitrogen_count", "parts_revenue", "labor_quantity", "labor_revenue", "supplies_revenue", "total_revenue_w_supplies", "gross_profit_no_supplies", "gross_profit_w_supplies"],
        "table": "bigo_sales_summary"
    }
}

def row_exists(cursor, table, columns, row):
    query = f"SELECT 1 FROM {table} WHERE " + " AND ".join([f"{col} = ?" for col in columns])
    cursor.execute(query, row)
    return cursor.fetchone() is not None

def transfer_data(old_cursor, new_cursor, mapping):
    old_data = get_table_data(old_cursor, mapping['table'])
    for row in old_data:
        new_row = [row[mapping['old'].index(col)] for col in mapping['old']]
        if not row_exists(new_cursor, mapping['table'], mapping['new'], new_row):
            insert_data(new_cursor, mapping['table'], mapping['new'], [new_row])

# Copy data from old to new database
for table, mapping in table_mappings.items():
    transfer_data(old_cursor, new_cursor, mapping)

# Commit the changes
new_conn.commit()

# Close the connections
old_conn.close()
new_conn.close()

print("Data transfer complete.")
