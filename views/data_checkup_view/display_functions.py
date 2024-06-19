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

def display_data(view, missing_data, start_date, end_date, results_table):
    try:
        df = transform_missing_dates_to_df(missing_data, start_date, end_date)

        columns = []
        for col in df.columns:
            date = datetime.strptime(col, '%Y-%m-%d')
            columns.append(f"{col}\n{date.strftime('%A')}")

        results_table.setRowCount(len(df))
        results_table.setColumnCount(len(df.columns))
        results_table.setHorizontalHeaderLabels(columns)
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
        print(f"Error displaying data: {e}")

def display_tech_data(view, tech_data, start_date, end_date, results_table):
    try:
        results_table.clear()  # Clear the table before adding new data

        # Display Midas Tech Data
        if "Midas" in tech_data:
            midas_missing_dates = tech_data["Midas"]
            df_midas = transform_missing_dates_to_df(midas_missing_dates, start_date, end_date)
            columns = []
            for col in df_midas.columns:
                date = datetime.strptime(col, '%Y-%m-%d')
                columns.append(f"{col}\n{date.strftime('%A')}")

            results_table.setRowCount(len(df_midas))
            results_table.setColumnCount(len(df_midas.columns))
            results_table.setHorizontalHeaderLabels(columns)
            results_table.setVerticalHeaderLabels(df_midas.index.astype(str).tolist())

            for row in range(len(df_midas)):
                for col in range(len(df_midas.columns)):
                    item = QTableWidgetItem()
                    item.setText("")
                    date = datetime.strptime(df_midas.columns[col], '%Y-%m-%d')
                    if date.strftime('%Y-%m-%d') in CLOSED_DAYS:
                        item.setBackground(Qt.black)
                        item.setText("Closed")
                    elif date.weekday() == 6:  # Sunday
                        item.setBackground(Qt.gray)
                    elif df_midas.iloc[row, col] == 'Missing':
                        item.setBackground(Qt.red)
                    else:
                        item.setBackground(Qt.green)
                    results_table.setItem(row, col, item)

        # Display Bigo Tech Data
        if "Bigo" in tech_data:
            bigo_missing_dates = tech_data["Bigo"]
            df_bigo = pd.DataFrame(
                columns=[date.strftime('%Y-%m-%d') for date in pd.date_range(start=start_date, end=end_date)]
            )
            df_bigo.loc[0] = ['Missing' if date in bigo_missing_dates else 'Found' for date in df_bigo.columns]
            df_bigo.index = ["Bigo Tech Data"]

            # Add Bigo data to the table below the Midas data
            start_row = len(df_midas) if "Midas" in tech_data else 0
            results_table.setRowCount(start_row + 1)
            for col in range(len(df_bigo.columns)):
                item = QTableWidgetItem()
                item.setText("")
                date = datetime.strptime(df_bigo.columns[col], '%Y-%m-%d')
                if date.strftime('%Y-%m-%d') in CLOSED_DAYS:
                    item.setBackground(Qt.black)
                    item.setText("Closed")
                elif date.weekday() == 6:  # Sunday
                    item.setBackground(Qt.gray)
                elif df_bigo.iloc[0, col] == 'Missing':
                    item.setBackground(Qt.red)
                else:
                    item.setBackground(Qt.green)
                results_table.setItem(start_row, col, item)
            results_table.setVerticalHeaderItem(start_row, QTableWidgetItem("Bigo Tech Data"))

    except Exception as e:
        print(f"Error displaying tech data: {e}")


def display_timesheet_data(view, timesheet_data, start_date, end_date, results_table):
    try:
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
