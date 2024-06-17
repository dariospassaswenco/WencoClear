import pandas as pd
import os
from datetime import datetime
from data_models.bigo import BigoSalesSummary
from config.app_settings import ENGINE, BIGO_SS_TABLE


class BigoSalesSummaryExtractor:
    @staticmethod
    def extract_ss_data(file_path):
        try:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            store_number = int(file_name.split('_')[1])  # Assuming store number is an integer

            bigo_summary = BigoSalesSummary(wenco_id=store_number)

            # Read Excel file into DataFrame
            df_test = pd.read_excel(file_path, engine="xlrd", skiprows=0, usecols=[0, 34])
            df_test.columns = ['Store_or_Category', 'Total Sales']
            # Locate row with Total Sales
            sales_group = df_test.loc[df_test['Store_or_Category'] == 'Sales Group']
            nan_test = sales_group['Total Sales'].iloc[0]
            # Extract required values for Revenue
            if nan_test == "Total Sales":
                df = pd.read_excel(file_path, engine="xlrd", skiprows=0, usecols=[0, 6, 7, 11, 16, 20, 29, 33])
            else:
                df = pd.read_excel(file_path, engine="xlrd", skiprows=0, usecols=[0, 6, 8, 12, 17, 21, 30, 34])

            # Rename the columns for better understanding
            df.columns = ['Store_or_Category', 'Car Count', 'Parts Quantity',
                          'Parts Revenue', 'Labor Quantity', 'Labor Cost', 'GP', 'Total Sales']

            # Get the second row of the DataFrame
            date_row = df.iloc[2]
            # Extract the date range using string manipulation
            start_date = date_row['Store_or_Category'].split(':')[1].strip()
            # Convert the date format to "year-month-day"
            bigo_summary.date = datetime.strptime(start_date, '%m/%d/%Y').strftime('%Y-%m-%d')

            # Locate Car Count
            try:
                car_count = df.loc[df['Store_or_Category'] == 'Car Count']
                bigo_summary.car_count = int(car_count['Car Count'].iloc[0])
            except Exception as e:
                pass  # If not found, keep Tire Count as 0

            # Locate row with Parts Quantity for Tire Count
            try:
                tires_total = df.loc[df['Store_or_Category'] == 'Tires Total:']
                bigo_summary.tire_count = float(tires_total['Parts Quantity'].iloc[0])
            except Exception as e:
                pass  # If not found, keep Tire Count as 0

            # Locate row with Alignments
            try:
                alignments_total = df.loc[df['Store_or_Category'] == 'ALIGNMENTS']
                bigo_summary.alignment_count = float(alignments_total['Labor Quantity'].iloc[0])
            except Exception as e:
                pass

            # Locate row with Nitrogen
            try:
                nitrogen_total = df.loc[df['Store_or_Category'] == 'NITROGEN']
                bigo_summary.nitrogen_count = float(nitrogen_total['Labor Quantity'].iloc[0])
            except Exception as e:
                pass

            # Locate row with Supplies
            try:
                supplies_total = df.loc[df['Store_or_Category'] == 'SHOP SUPPLIES - SERVICE']
                bigo_summary.supplies_revenue = float(supplies_total['GP'].iloc[0])
            except Exception as e:
                pass

            # Locate row with Total Sales and Gross Profit
            try:
                sales_service_total = df.loc[df['Store_or_Category'] == 'Sales & Service Total:']
                bigo_summary.total_revenue_w_supplies = float(sales_service_total['Total Sales'].iloc[0])
                gross_profit = float(sales_service_total['GP'].iloc[0])
                bigo_summary.gross_profit_no_supplies = gross_profit - bigo_summary.supplies_revenue
                bigo_summary.gross_profit_w_supplies = gross_profit
                bigo_summary.parts_revenue = float(sales_service_total['Parts Revenue'].iloc[0])
                bigo_summary.labor_quantity = float(sales_service_total['Labor Quantity'].iloc[0])
                bigo_summary.labor_revenue = float(sales_service_total['Labor Cost'].iloc[0])
            except Exception as e:
                pass

            # Convert to dictionary for dataframe
            result = bigo_summary.__dict__
            df = pd.DataFrame([result])

            conditions_for_empty_or_zero = (
                (df['total_revenue_w_supplies'].isnull() | (df['total_revenue_w_supplies'] == 0)).all() and
                (df['car_count'].isnull() | (df['car_count'] == 0)).all()
            )

            if conditions_for_empty_or_zero:
                return pd.DataFrame()
            else:
                return df

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return pd.DataFrame()

    @staticmethod
    def delete_existing_records(df):
        with ENGINE.connect() as conn:
            for _, row in df.iterrows():
                # Check if the record exists
                check_query = text(f"SELECT COUNT(*) FROM {BIGO_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date")
                result = conn.execute(check_query, {'wenco_id': row['wenco_id'], 'date': row['date']}).scalar()

                if result > 0:
                    # If the record exists, delete it
                    delete_query = text(f"DELETE FROM {BIGO_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date")
                    conn.execute(delete_query, {'wenco_id': row['wenco_id'], 'date': row['date']})
                    print(f"Deleted existing record for wenco_id {row['wenco_id']} and date {row['date']}")