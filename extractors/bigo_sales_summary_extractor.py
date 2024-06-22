import pandas as pd
import os
from datetime import datetime
from data_models.bigo import BigoSalesSummary
from config.app_settings import ENGINE, BIGO_SS_TABLE
from sqlalchemy import text


class BigoSalesSummaryExtractor:
    @staticmethod
    def extract_ss_data(file_path):
        try:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            store_number = int(file_name.split('_')[1])  # Assuming store number is an integer

            bigo_summary = BigoSalesSummary(wenco_id=store_number)

            # Function to check which column contains 'Total Sales'
            def check_total_sales_column(file_path):
                df_test = pd.read_excel(file_path, engine="xlrd", skiprows=0, usecols=[0, 34, 35])
                df_test.columns = ['Store_or_Category', 'Total Sales 34', 'Total Sales 35']
                sales_group = df_test.loc[df_test['Store_or_Category'] == 'Sales Group']

                if not sales_group.empty:
                    if 'Total Sales' in sales_group['Total Sales 34'].values:
                        return 34
                    elif 'Total Sales' in sales_group['Total Sales 35'].values:
                        return 35
                    else:
                        return 36
                raise ValueError("Total Sales not found in columns 34, 35, or 36")

            try:
                total_sales_column = check_total_sales_column(file_path)
            except ValueError as e:
                print(e)
                return pd.DataFrame()

            # Extract required values for Revenue based on the column with 'Total Sales'
            if total_sales_column == 34:
                df = pd.read_excel(file_path, engine="xlrd", skiprows=0, usecols=[0, 6, 7, 11, 16, 20, 29, 33])
                #print("First instance (Total Sales in column 34)")
            elif total_sales_column == 35:
                df = pd.read_excel(file_path, engine="xlrd", skiprows=0, usecols=[0, 6, 8, 12, 17, 21, 30, 34])
                #print("Second instance (Total Sales in column 35)")
            elif total_sales_column == 36:
                df = pd.read_excel(file_path, engine="xlrd", skiprows=0, usecols=[0, 7, 9, 13, 18, 22, 31, 35])
                #print("Third instance (Total Sales in column 36)")
            else:
                raise ValueError("Unexpected column for Total Sales")

            #print(df)

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
                pass  # If not found, keep Car Count as 0

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

            #print(bigo_summary)

            # Convert to dictionary for dataframe
            result = bigo_summary.__dict__
            df = pd.DataFrame([result])

            conditions_for_empty_or_zero = (
                    (df['total_revenue_w_supplies'].isnull() | (df['total_revenue_w_supplies'] == 0)).all() and
                    (df['car_count'].isnull() | (df['car_count'] == 0)).all()
            )

            if conditions_for_empty_or_zero:
                print("returning empty dataframe")
                return pd.DataFrame()
            else:
                print(df)
                return df

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return pd.DataFrame()

    @staticmethod
    def delete_existing_records(df):
        with ENGINE.begin() as conn:
            for _, row in df.iterrows():
                query = text(f"DELETE FROM {BIGO_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date")
                result = conn.execute(query, {'wenco_id': row['wenco_id'], 'date': row['date']})
                print(
                    f"Query executed: DELETE FROM {BIGO_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date with params wenco_id={row['wenco_id']} and date={row['date']}")
                print(f"Number of rows deleted: {result.rowcount}")


# Test the function
if __name__ == "__main__":
    file_path = r"C:\Users\Wenco\Documents\WencoClearOutputs\BGO_14_SS_2024-06-20.XLS"
    extractor = BigoSalesSummaryExtractor()
    df = extractor.extract_ss_data(file_path)
    print(df)
