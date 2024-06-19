from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from config.app_settings import *
import pandas as pd
import traceback

def transform_missing_dates_to_df(missing_data, start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date)
    columns = [date.strftime('%Y-%m-%d') for date in date_range]

    # Include all stores and initialize them with 'Present'
    all_stores = set(missing_data.keys())
    for store, dates in missing_data.items():
        all_stores.update(store)

    df = pd.DataFrame(index=all_stores, columns=columns)
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
        if "Bigo" in tech_data:
            bigo_missing_dates = tech_data["Bigo"]
            df_bigo = pd.DataFrame(
                columns=[date.strftime('%Y-%m-%d') for date in pd.date_range(start=start_date, end=end_date)]
            )
            df_bigo.loc[0] = ['Missing' if date in bigo_missing_dates else 'Found' for date in df_bigo.columns]
            df_bigo.index = ["Bigo Tech Data"]

        if "Midas" in tech_data:
            midas_missing_dates = tech_data["Midas"]
            df_midas = transform_missing_dates_to_df(midas_missing_dates, start_date, end_date)
        else:
            df_midas = pd.DataFrame()

        if not df_midas.empty and "Bigo" in tech_data:
            df = pd.concat([df_midas, df_bigo])
        elif not df_midas.empty:
            df = df_midas
        else:
            df = df_bigo

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
        print(f"Error displaying tech data: {e}")

def display_timesheet_data(view, missing_data, start_date, end_date, results_table):
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
        print(f"Error displaying timesheet data: {e}")

def display_all_data(view, combined_results, start_date, end_date, results_table):
    try:
        columns = [date.strftime('%Y-%m-%d') for date in pd.date_range(start=start_date, end=end_date)]
        df = pd.DataFrame.from_dict(combined_results, orient='index', columns=columns)

        # Ensure all dates and stores are represented
        for col in columns:
            if col not in df.columns:
                df[col] = 'All Present'
        df = df.fillna('All Present')

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
