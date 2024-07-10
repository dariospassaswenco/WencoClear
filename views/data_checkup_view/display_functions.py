from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from config.app_settings import *
from database.query_functions_df import query_sales_summary_data, query_tech_data, query_timesheet_data, query_sales_by_category_data
import pandas as pd
import traceback

def create_empty_dataframe(start_date, end_date, stores):
    date_range = pd.date_range(start=start_date, end=end_date)
    columns = [date.strftime('%Y-%m-%d') for date in date_range]
    df = pd.DataFrame(index=stores, columns=columns).fillna('No Data')
    print("Created empty dataframe with columns:", columns)  # Debug statement
    return df

def filter_stores_by_type(store_type):
    if store_type == "Midas":
        return [f"Midas {store}" for store in MIDAS_STORE_NUMBERS]
    elif store_type == "Bigo":
        return [f"Bigo {store}" for store in BIGO_STORE_NUMBERS]
    else:
        return [f"Midas {store}" for store in MIDAS_STORE_NUMBERS] + [f"Bigo {store}" for store in BIGO_STORE_NUMBERS]

def merge_dataframes(empty_df, data_df, column_name):
    try:
        for index, row in data_df.iterrows():
            store = row.name
            for date, value in row.items():
                if store in empty_df.index and date in empty_df.columns:
                    empty_df.at[store, date] = value
        return empty_df
    except Exception as e:
        print(f"Error in merge_dataframes: {e}")
        traceback.print_exc()

def display_dataframe(view, df, results_table):
    try:
        results_table.clear()  # Clear the table before adding new data

        # Add day names to column headers
        columns_with_days = [f"{col}\n{datetime.strptime(col, '%Y-%m-%d').strftime('%A')}" for col in df.columns]

        # Set table row and column counts
        results_table.setRowCount(len(df))
        results_table.setColumnCount(len(df.columns))
        results_table.setHorizontalHeaderLabels(columns_with_days)
        results_table.setVerticalHeaderLabels(df.index.astype(str).tolist())

        # Populate the table
        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QTableWidgetItem()
                cell_value = df.iloc[row, col]
                item.setText(str(cell_value) if cell_value != 'No Data' else "")
                date = datetime.strptime(df.columns[col], '%Y-%m-%d')
                if date.strftime('%Y-%m-%d') in CLOSED_DAYS:
                    item.setBackground(Qt.black)
                    item.setText("Closed")
                elif date.weekday() == 6:  # Sunday
                    item.setBackground(Qt.gray)
                elif cell_value != 'No Data' and cell_value != '' and (not isinstance(cell_value, str) or "Missing" not in cell_value):
                    item.setBackground(Qt.green)
                else:
                    item.setBackground(Qt.red)
                results_table.setItem(row, col, item)
    except Exception as e:
        print(f"Error displaying data: {e}")
        traceback.print_exc()

def display_sales_summary_data(view, start_date, end_date, results_table):
    store_type = view.store_type_combo.currentText()
    stores = filter_stores_by_type(store_type)
    df = create_empty_dataframe(start_date, end_date, stores)

    if store_type == "All" or store_type == "Midas":
        data_df_midas = query_sales_summary_data(start_date, end_date, "Midas")
        df = merge_dataframes(df, data_df_midas, 'revenue')

    if store_type == "All" or store_type == "Bigo":
        data_df_bigo = query_sales_summary_data(start_date, end_date, "Bigo")
        df = merge_dataframes(df, data_df_bigo, 'revenue')

    display_dataframe(view, df, results_table)

def display_tech_data(view, start_date, end_date, results_table):
    store_type = view.store_type_combo.currentText()
    stores = filter_stores_by_type(store_type)
    df = create_empty_dataframe(start_date, end_date, stores)

    if store_type == "All" or store_type == "Midas":
        data_df_midas = query_tech_data(start_date, end_date, "Midas")
        df = merge_dataframes(df, data_df_midas, 'last_name')

    if store_type == "All" or store_type == "Bigo":
        data_df_bigo = query_tech_data(start_date, end_date, "Bigo")
        df = merge_dataframes(df, data_df_bigo, 'last_name')

    display_dataframe(view, df, results_table)

def display_timesheet_data(view, start_date, end_date, results_table):
    store_type = view.store_type_combo.currentText()
    stores = filter_stores_by_type(store_type)
    df = create_empty_dataframe(start_date, end_date, stores)

    if store_type == "All" or store_type == "Midas":
        data_df_midas = query_timesheet_data(start_date, end_date, "Midas")
        df = merge_dataframes(df, data_df_midas, 'last_name')

    if store_type == "All" or store_type == "Bigo":
        data_df_bigo = query_timesheet_data(start_date, end_date, "Bigo")
        df = merge_dataframes(df, data_df_bigo, 'last_name')

    display_dataframe(view, df, results_table)

def display_all_data(view, start_date, end_date, results_table):
    stores = filter_stores_by_type("All")
    df = create_empty_dataframe(start_date, end_date, stores)

    data_df_midas_sales = query_sales_summary_data(start_date, end_date, "Midas")
    data_df_bigo_sales = query_sales_summary_data(start_date, end_date, "Bigo")
    data_df_midas_tech = query_tech_data(start_date, end_date, "Midas")
    data_df_bigo_tech = query_tech_data(start_date, end_date, "Bigo")
    data_df_midas_timesheet = query_timesheet_data(start_date, end_date, "Midas")
    data_df_bigo_timesheet = query_timesheet_data(start_date, end_date, "Bigo")
    data_df_midas_sales_by_category = query_sales_by_category_data(start_date, end_date, "Midas")

    df_sales = create_empty_dataframe(start_date, end_date, stores)
    df_sales = merge_dataframes(df_sales, data_df_midas_sales, 'revenue')
    df_sales = merge_dataframes(df_sales, data_df_bigo_sales, 'revenue')

    df_tech = create_empty_dataframe(start_date, end_date, stores)
    df_tech = merge_dataframes(df_tech, data_df_midas_tech, 'last_name')
    df_tech = merge_dataframes(df_tech, data_df_bigo_tech, 'last_name')

    df_timesheet = create_empty_dataframe(start_date, end_date, stores)
    df_timesheet = merge_dataframes(df_timesheet, data_df_midas_timesheet, 'last_name')
    df_timesheet = merge_dataframes(df_timesheet, data_df_bigo_timesheet, 'last_name')

    df_sales_by_category = create_empty_dataframe(start_date, end_date, stores)
    df_sales_by_category = merge_dataframes(df_sales_by_category, data_df_midas_sales_by_category, 'category')

    # Combine all dataframes
    # In the display_all_data function, modify the loop like this:
    for store in df.index:
        for date in df.columns:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            if date_obj.weekday() == 6:  # Sunday
                df.at[store, date] = ''  # Empty string for Sundays
            else:
                missing_data = []
                if df_sales.at[store, date] == 'No Data' or df_sales.at[store, date] == '':
                    missing_data.append('Sales Summary')
                if df_tech.at[store, date] == 'No Data' or df_tech.at[store, date] == '':
                    missing_data.append('Tech')
                if df_timesheet.at[store, date] == 'No Data' or df_timesheet.at[store, date] == '':
                    missing_data.append('Timesheet')
                if store.startswith('Midas'):  # Only check Sales By Category for Midas stores
                    if df_sales_by_category.at[store, date] == 'No Data' or df_sales_by_category.at[store, date] == '':
                        missing_data.append('Sales By Category')
                if not missing_data:
                    df.at[store, date] = 'All Data Exists'
                else:
                    df.at[store, date] = f"Missing: {', '.join(missing_data)}"

    display_all_reports_dataframe(view, df, results_table)


def display_all_reports_dataframe(view, df, results_table):
    try:
        results_table.clear()  # Clear the table before adding new data

        # Add day names to column headers
        columns_with_days = [f"{col}\n{datetime.strptime(col, '%Y-%m-%d').strftime('%A')}" for col in df.columns]

        # Set table row and column counts
        results_table.setRowCount(len(df))
        results_table.setColumnCount(len(df.columns))
        results_table.setHorizontalHeaderLabels(columns_with_days)
        results_table.setVerticalHeaderLabels(df.index.astype(str).tolist())

        # Populate the table
        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QTableWidgetItem()
                date = datetime.strptime(df.columns[col], '%Y-%m-%d')

                if date.strftime('%Y-%m-%d') in CLOSED_DAYS:
                    item.setBackground(Qt.black)
                    item.setText("Closed")
                elif date.weekday() == 6:  # Sunday
                    item.setBackground(Qt.gray)
                    item.setText("")  # Empty text for Sundays
                else:
                    cell_value = df.iloc[row, col]
                    item.setText(str(cell_value) if cell_value != 'No Data' else "")
                    if cell_value == 'All Data Exists':
                        item.setBackground(Qt.green)
                    else:
                        item.setBackground(Qt.red)

                results_table.setItem(row, col, item)
    except Exception as e:
        print(f"Error displaying all reports data: {e}")
        traceback.print_exc()

def display_sales_by_category_data(view, start_date, end_date, results_table):
    store_type = "Midas"  # This is specific to Midas
    print(f"Store type for Sales By Category: {store_type}")  # Debug statement
    stores = filter_stores_by_type(store_type)
    df = create_empty_dataframe(start_date, end_date, stores)
    data_df = query_sales_by_category_data(start_date, end_date, store_type)
    df = merge_dataframes(df, data_df, 'category')
    display_dataframe(view, df, results_table)