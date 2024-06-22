import pandas as pd
import sqlite3
from config.app_settings import CLEAR_DATABASE_PATH

def get_all_closed_days():
    """
    Retrieves all closed days from the database and returns them as a DataFrame.
    """
    try:
        conn = sqlite3.connect(CLEAR_DATABASE_PATH)
        query = "SELECT date, reason FROM closed_days"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching closed days: {e}")
        return pd.DataFrame()

def update_closed_days(df):
    """
    Updates the closed days in the database based on the DataFrame input.
    Any differences will be inserted into the table.

    :param df: DataFrame containing closed days data
    """
    try:
        conn = sqlite3.connect(CLEAR_DATABASE_PATH)
        cursor = conn.cursor()

        # Fetch existing closed days from the database
        existing_closed_days = pd.read_sql_query("SELECT date, reason FROM closed_days", conn)

        # Find rows to insert by checking which rows in df are not in existing_closed_days
        new_closed_days = df[~df.apply(tuple, 1).isin(existing_closed_days.apply(tuple, 1))]

        # Insert new closed days into the database
        for _, row in new_closed_days.iterrows():
            cursor.execute("INSERT INTO closed_days (date, reason) VALUES (?, ?)", (row['date'], row['reason']))

        conn.commit()
        conn.close()
        print("Closed days updated successfully.")
    except Exception as e:
        print(f"Error updating closed days: {e}")
