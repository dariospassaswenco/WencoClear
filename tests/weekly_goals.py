import pandas as pd
import sqlite3
import os
import tempfile
from config.app_settings import CLEAR_DATABASE_PATH
from database.goals import update_weekly_revenue_goals, get_weekly_revenue_goals

def create_test_db():
    conn = sqlite3.connect(CLEAR_DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_revenue_goals (
            wenco_id INTEGER,
            week_end_date TEXT,
            revenue_goal FLOAT,
            PRIMARY KEY (wenco_id, week_end_date)
        );
    """)
    conn.commit()
    conn.close()

def test_update_weekly_revenue_goals():
    data = {
        'wenco_id': [1, 2, 3],
        '2024-06-01': [1000.0, 2000.0, 3000.0],
        '2024-06-08': [1100.0, 2100.0, 3100.0]
    }
    df = pd.DataFrame(data).set_index('wenco_id')

    update_weekly_revenue_goals(df)

    conn = sqlite3.connect(CLEAR_DATABASE_PATH)
    query = "SELECT * FROM weekly_revenue_goals"
    df_db = pd.read_sql_query(query, conn)
    conn.close()

    df_db_pivot = df_db.pivot(index='wenco_id', columns='week_end_date', values='revenue_goal')

    # Debug output
    print("Original DataFrame:\n", df)
    print("Database DataFrame:\n", df_db_pivot)

    assert df.equals(df_db_pivot), f"Data mismatch after update\nOriginal DataFrame:\n{df}\nDatabase DataFrame:\n{df_db_pivot}"

def test_get_weekly_revenue_goals():
    data = {
        'wenco_id': [1, 2, 3],
        '2024-06-01': [1000.0, 2000.0, 3000.0],
        '2024-06-08': [1100.0, 2100.0, 3100.0]
    }
    expected_df = pd.DataFrame(data).set_index('wenco_id')

    fetched_df = get_weekly_revenue_goals()

    # Debug output
    print("Expected DataFrame:\n", expected_df)
    print("Fetched DataFrame:\n", fetched_df)

    assert expected_df.equals(fetched_df), f"Data mismatch after fetch\nExpected DataFrame:\n{expected_df}\nFetched DataFrame:\n{fetched_df}"

if __name__ == "__main__":
    temp_db, CLEAR_DATABASE_PATH = tempfile.mkstemp()
    os.close(temp_db)

    try:
        create_test_db()

        test_update_weekly_revenue_goals()
        print("test_update_weekly_revenue_goals passed")

        test_get_weekly_revenue_goals()
        print("test_get_weekly_revenue_goals passed")
    finally:
        os.remove(CLEAR_DATABASE_PATH)
