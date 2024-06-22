import pandas as pd
import sqlite3
from config.app_settings import CLEAR_DATABASE_PATH

def get_kpi_goals_by_shop():
    """
    Queries the kpi_goals_by_shop table and returns it as a DataFrame.
    """
    try:
        conn = sqlite3.connect(CLEAR_DATABASE_PATH)
        query = "SELECT * FROM kpi_goals_by_shop"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching KPI goals: {e}")
        return pd.DataFrame()

def update_kpi_goals_by_shop(df):
    """
    Updates the kpi_goals_by_shop table in the database with the given DataFrame.
    Rows with changed values will be updated in the database.

    :param df: DataFrame containing the KPI goals data
    """
    try:
        conn = sqlite3.connect(CLEAR_DATABASE_PATH)
        cursor = conn.cursor()

        # Fetch existing KPI goals from the database
        existing_kpi_goals = pd.read_sql_query("SELECT * FROM kpi_goals_by_shop", conn)

        # Update rows that differ from the existing data
        for index, row in df.iterrows():
            cursor.execute("""
                UPDATE kpi_goals_by_shop
                SET avg_cars_per_day_goal = ?, average_repair_order_goal = ?, gross_profit_margin_goal = ?, 
                    tech_efficiency_goal = ?, tech_ot_per_vehicle_goal = ?, alignments_per_day_goal = ?, 
                    tires_per_day_goal = ?, nitrogen_per_tire_goal = ?
                WHERE wenco_id = ?
            """, (
                row['avg_cars_per_day_goal'], row['average_repair_order_goal'], row['gross_profit_margin_goal'],
                row['tech_efficiency_goal'], row['tech_ot_per_vehicle_goal'], row['alignments_per_day_goal'],
                row['tires_per_day_goal'], row['nitrogen_per_tire_goal'], row['wenco_id']
            ))

        conn.commit()
        conn.close()
        print("KPI goals updated successfully.")
    except Exception as e:
        print(f"Error updating KPI goals: {e}")

def get_weekly_revenue_goals():
    """
    Queries the weekly_revenue_goals table and returns it as a DataFrame.
    """
    try:
        conn = sqlite3.connect(CLEAR_DATABASE_PATH)
        query = "SELECT * FROM weekly_revenue_goals"
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df
    except Exception as e:
        print(f"Error fetching weekly revenue goals: {e}")
        return pd.DataFrame()

def transpose_weekly_revenue_goals(df):
    """
    Transposes the weekly_revenue_goals DataFrame to have shops as rows and week_end dates as columns.
    """
    try:
        # Ensure the data types are correct for pivoting
        df['wenco_id'] = df['wenco_id'].astype(int)
        df['week_end_date'] = pd.to_datetime(df['week_end_date']).dt.strftime('%Y-%m-%d')
        df['revenue_goal'] = df['revenue_goal'].astype(float)

        # Print the DataFrame after ensuring data types
        print("DataFrame with correct data types:\n", df)

        # Pivot the DataFrame to have shops as rows and week_end dates as columns
        df_pivot = df.pivot(index='wenco_id', columns='week_end_date', values='revenue_goal')

        # Print the pivoted DataFrame
        print("Pivoted DataFrame:\n", df_pivot)

        return df_pivot
    except Exception as e:
        print(f"Error transposing weekly revenue goals: {e}")
        return pd.DataFrame()

def update_weekly_revenue_goals(df):
    """
    Updates the weekly_revenue_goals table in the database with the given DataFrame.
    The DataFrame should have shops as rows and week_end dates as columns.

    :param df: DataFrame containing the weekly revenue goals data
    """
    try:
        conn = sqlite3.connect(CLEAR_DATABASE_PATH)
        cursor = conn.cursor()

        # Clear existing data
        cursor.execute("DELETE FROM weekly_revenue_goals")

        # Insert new data
        df.to_sql('weekly_revenue_goals', conn, if_exists='append', index=False)

        conn.commit()
        conn.close()
        print("Weekly revenue goals updated successfully.")
    except Exception as e:
        print(f"Error updating weekly revenue goals: {e}")

if __name__ == "__main__":
    # Run the function to query and print the DataFrame
    df = get_weekly_revenue_goals()
    print("Original DataFrame:\n", df)

    # Transpose the DataFrame
    df_transposed = transpose_weekly_revenue_goals(df)
    print("Transposed DataFrame:\n", df_transposed)
