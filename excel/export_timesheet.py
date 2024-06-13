import os
import pandas as pd
from config.app_settings import EXCELEXPORT


def export_timesheet_data(df, start_date, end_date):
    # Sort the data by last name and first name
    df.sort_values(by=['last_name', 'first_name'], inplace=True)

    # Pivot the data to get dates as columns
    pivot_data = df.pivot_table(index=['last_name', 'first_name'], columns='date', values='hours', fill_value=0)

    # Reset index to make last_name and first_name columns again
    pivot_data.reset_index(inplace=True)

    # Create the file name and path
    file_name = f"timesheet_data_{start_date}_{end_date}.xlsx"
    file_path = os.path.join(EXCELEXPORT, file_name)

    # Export to Excel
    pivot_data.to_excel(file_path, index=False)
    print(f"Timesheet data exported to {file_path}")
