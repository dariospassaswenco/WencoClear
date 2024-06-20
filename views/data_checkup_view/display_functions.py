# views/data_checkup_views/display_functions

from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from config.app_settings import *
import pandas as pd
import traceback

def transform_missing_dates_to_df(missing_data, start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date)
    columns = [date.strftime('%Y-%m-%d') for date in date_range]
    df = pd.DataFrame(index=missing_data.keys(), columns=columns)
    df = df.fillna('Present')

    for store, dates in missing_data.items():
        for date in dates:
            if date in df.columns:
                df.at[store, date] = 'Missing'

    return df

def filter_stores_by_type(df, store_type):
    if store_type == "Midas":
        return df[df.index.isin(MIDAS_STORE_NUMBERS)]
    elif store_type == "Bigo":
        return df[df.index.isin(BIGO_STORE_NUMBERS)]
    return df

def display_sales_summary_data(view, ss_data, start_date, end_date, results_table):
    try:
        results_table.clear()  # Clear the table before adding new data

        # Create a DataFrame for the date range and all Midas and Bigo stores
        date_range = pd.date_range(start=start_date, end=end_date)
        columns = [date.strftime('%Y-%m-%d') for date in date_range]
        all_stores = MIDAS_STORE_NUMBERS + BIGO_STORE_NUMBERS

        # Initialize DataFrame
        df = pd.DataFrame(index=all_stores, columns=columns).fillna('Present')

        # Fill in the DataFrame for Midas and Bigo stores
        for store, dates in ss_data.items():
            for date in dates:
                date_str = date if isinstance(date, str) else date.strftime('%Y-%m-%d')
                if date_str in df.columns:
                    df.at[store, date_str] = 'Missing'

        # Filter stores based on the selected store type
        store_type = view.store_type_combo.currentText()
        df = filter_stores_by_type(df, store_type)

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
                item.setText("")
                date = datetime.strptime(df.columns[col], '%Y-%m-%d')
                if date.strftime('%Y-%m-%d') in CLOSED_DAYS:
                    item.setBackground(Qt.black)
                    item.setText("Closed")
                elif date.weekday() == 6:  # Sunday
                    item.setBackground(Qt.gray)
                elif df.iloc[row, col] == 'Missing':
                    item.setBackground(Qt.red)
                else:
                    item.setBackground(Qt.green)
                results_table.setItem(row, col, item)

    except Exception as e:
        print(f"Error displaying sales summary data: {e}")

def display_tech_data(view, tech_data, start_date, end_date, results_table):
    try:
        results_table.clear()  # Clear the table before adding new data

        # Create a DataFrame for the date range and all Midas stores
        date_range = pd.date_range(start=start_date, end=end_date)
        columns = [date.strftime('%Y-%m-%d') for date in date_range]
        midas_stores = MIDAS_STORE_NUMBERS
        bigo_store = ["Bigo Tech Data"]

        # Initialize dataframes
        df_midas = pd.DataFrame(index=midas_stores, columns=columns).fillna('Present')
        df_bigo = pd.DataFrame(index=bigo_store, columns=columns).fillna('Present')

        # Fill in the DataFrame for Midas stores
        if "Midas" in tech_data:
            midas_missing_dates = tech_data["Midas"]
            for store, dates in midas_missing_dates.items():
                for date in dates:
                    date_str = date if isinstance(date, str) else date.strftime('%Y-%m-%d')
                    if date_str in df_midas.columns:
                        df_midas.at[store, date_str] = 'Missing'

        # Fill in the DataFrame for Bigo store
        if "Bigo" in tech_data:
            bigo_missing_dates = tech_data["Bigo"]
            df_bigo.loc["Bigo Tech Data"] = ['Missing' if date in bigo_missing_dates else 'Found' for date in columns]

        # Concatenate Midas and Bigo dataframes
        df = pd.concat([df_midas, df_bigo])

        # Filter stores based on the selected store type
        store_type = view.store_type_combo.currentText()
        df = filter_stores_by_type(df, store_type)

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
                item.setText("")
                date = datetime.strptime(df.columns[col], '%Y-%m-%d')
                if date.strftime('%Y-%m-%d') in CLOSED_DAYS:
                    item.setBackground(Qt.black)
                    item.setText("Closed")
                elif date.weekday() == 6:  # Sunday
                    item.setBackground(Qt.gray)
                elif df.iloc[row, col] == 'Missing':
                    item.setBackground(Qt.red)
                else:
                    item.setBackground(Qt.green)
                results_table.setItem(row, col, item)

    except Exception as e:
        print(f"Error displaying tech data: {e}")

def display_timesheet_data(view, timesheet_data, start_date, end_date, results_table):
    try:
        # Ensure all stores are present in the timesheet_data, even if they have no missing dates
        all_stores = MIDAS_STORE_NUMBERS + BIGO_STORE_NUMBERS
        for store in all_stores:
            if store not in timesheet_data:
                timesheet_data[store] = []

        # Create a DataFrame for the date range
        date_range = pd.date_range(start=start_date, end=end_date)
        columns = [date.strftime('%Y-%m-%d') for date in date_range]
        df = pd.DataFrame(index=timesheet_data.keys(), columns=columns)
        df = df.fillna('Present')

        # Mark 'Missing' for each date range in timesheet_data
        for store, date_ranges in timesheet_data.items():
            for date_range in date_ranges:
                if isinstance(date_range, tuple):
                    start, end = date_range
                    for date in pd.date_range(start=start, end=end):
                        date_str = date.strftime('%Y-%m-%d')
                        if date_str in df.columns:
                            df.at[store, date_str] = 'Missing'
                else:
                    date_str = date_range if isinstance(date_range, str) else date_range.strftime('%Y-%m-%d')
                    if date_str in df.columns:
                        df.at[store, date_str] = 'Missing'

        # Filter stores based on the selected store type
        store_type = view.store_type_combo.currentText()
        df = filter_stores_by_type(df, store_type)

        columns_with_days = [f"{col}\n{datetime.strptime(col, '%Y-%m-%d').strftime('%A')}" for col in df.columns]

        results_table.setRowCount(len(df))
        results_table.setColumnCount(len(df.columns))
        results_table.setHorizontalHeaderLabels(columns_with_days)
        results_table.setVerticalHeaderLabels(df.index.astype(str).tolist())

        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QTableWidgetItem()
                item.setText("")
                date = datetime.strptime(df.columns[col], '%Y-%m-%d')
                if date.strftime('%Y-%m-%d') in CLOSED_DAYS:
                    item.setBackground(Qt.black)
                    item.setText("Closed")
                elif date.weekday() == 6:  # Sunday
                    item.setBackground(Qt.gray)
                elif df.iloc[row, col] == 'Missing':
                    item.setBackground(Qt.red)
                else:
                    item.setBackground(Qt.green)
                results_table.setItem(row, col, item)
    except Exception as e:
        print(f"Error displaying timesheet data: {e}")

def display_all_data(view, combined_results, start_date, end_date, results_table):
    try:
        columns = [date.strftime('%Y-%m-%d') for date in pd.date_range(start=start_date, end=end_date)]
        df = pd.DataFrame.from_dict(combined_results, orient='index', columns=columns)

        # Filter stores based on the selected store type
        store_type = view.store_type_combo.currentText()
        df = filter_stores_by_type(df, store_type)

        columns_with_days = []
        for col in df.columns:
            date = datetime.strptime(col, '%Y-%m-%d')
            columns_with_days.append(f"{col}\n{date.strftime('%A')}")

        results_table.setRowCount(len(df))
        results_table.setColumnCount(len(df.columns))
        results_table.setHorizontalHeaderLabels(columns_with_days)
        results_table.setVerticalHeaderLabels(df.index.astype(str).tolist())

        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QTableWidgetItem()
                value = df.iloc[row, col]
                item.setText(str(value))
                date = datetime.strptime(df.columns[col], '%Y-%m-%d')
                if date.strftime('%Y-%m-%d') in CLOSED_DAYS:
                    item.setBackground(Qt.black)
                    item.setText("Closed")
                elif date.weekday() == 6:  # Sunday
                    item.setBackground(Qt.gray)
                elif value == "All Present":
                    item.setBackground(Qt.green)
                else:
                    item.setBackground(Qt.red)
                results_table.setItem(row, col, item)
    except Exception as e:
        print(f"Error displaying all data: {e}")
        traceback.print_exc()

def combine_all_results(midas_ss, bigo_ss, midas_tech, bigo_tech, midas_timesheet, bigo_timesheet, start_date,
                        end_date):
    combined_results = {}

    # Combine Midas results
    for store in MIDAS_STORE_NUMBERS:
        store_name = f"Midas {store}"
        combined_results[store_name] = {}

        for date in pd.date_range(start=start_date, end=end_date):
            date_str = date.strftime('%Y-%m-%d')
            if date_str in CLOSED_DAYS or date.weekday() == 6:
                continue

            missing_items = []
            if date_str in midas_ss.get(store, []):
                missing_items.append("Sales")
            if date_str in midas_tech.get(store, []):
                missing_items.append("Tech")
            if date_str in midas_timesheet.get(store, []):
                missing_items.append("Timesheet")

            if missing_items:
                combined_results[store_name][date_str] = f"Missing: {', '.join(missing_items)}"
            else:
                combined_results[store_name][date_str] = "All Present"

    # Combine Bigo results
    for store in BIGO_STORE_NUMBERS:
        store_name = f"Bigo {store}"
        combined_results[store_name] = {}

        for date in pd.date_range(start=start_date, end=end_date):
            date_str = date.strftime('%Y-%m-%d')
            if date_str in CLOSED_DAYS or date.weekday() == 6:
                continue

            missing_items = []
            if date_str in bigo_ss.get(store, []):
                missing_items.append("Sales")
            if date_str in bigo_timesheet.get(store, []):
                missing_items.append("Timesheet")

            # Tech is combined for all Bigo
            if date_str in bigo_tech:
                missing_items.append("Tech")

            if missing_items:
                combined_results[store_name][date_str] = f"Missing: {', '.join(missing_items)}"
            else:
                combined_results[store_name][date_str] = "All Present"

    return combined_results
