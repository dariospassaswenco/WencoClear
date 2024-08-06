import pandas as pd
import os
from datetime import datetime
from data_models.bigo import BigoSalesSummary
from config.app_settings import ENGINE, BIGO_SS_TABLE
from sqlalchemy import text
import numpy as np

class BigoSalesSummaryExtractor:
    @staticmethod
    def safe_convert(value, to_type, default=0):
        try:
            if pd.isna(value):
                return default
            return to_type(value)
        except:
            return default

    @staticmethod
    def extract_row_data(row):
        # Extract values in the specified order
        values = row.dropna().tolist()
        # print(values)
        if len(values) < 9:
            return None  # Not enough values in the row

        data = {
            'parts_quantity': BigoSalesSummaryExtractor.safe_convert(values[1], float),
            'parts_amount': BigoSalesSummaryExtractor.safe_convert(values[2], float),
            'labor_quantity': BigoSalesSummaryExtractor.safe_convert(values[3], float),
            'labor_amount': BigoSalesSummaryExtractor.safe_convert(values[4], float),
            'discounts_quantity': BigoSalesSummaryExtractor.safe_convert(values[5], int) if len(values) > 9 else 0,
            'discounts_amount': BigoSalesSummaryExtractor.safe_convert(values[6 if len(values) > 9 else 5], float),
            'ext_cost': BigoSalesSummaryExtractor.safe_convert(values[-6], float),
            'gross_profit_percent': BigoSalesSummaryExtractor.safe_convert(values[-5], float),
            'gross_profit_amount': BigoSalesSummaryExtractor.safe_convert(values[-4], float),
            'total_sales': BigoSalesSummaryExtractor.safe_convert(values[-3], float)
        }
        # print(data)
        return data

    @staticmethod
    def extract_required_data(df):
        try:
            data = {
                'wenco_id': df['wenco_id'].iloc[0],
                'date': df['date'].iloc[0],
                'car_count': 0,  # We'll update this below
                'tire_count': 0.0,
                'alignment_count': 0.0,
                'nitrogen_count': 0.0,
                'parts_revenue': 0.0,
                'labor_quantity': 0.0,
                'labor_revenue': 0.0,
                'supplies_revenue': 0.0,
                'total_revenue_w_supplies': 0.0,
                'gross_profit_w_supplies': 0.0,
            }

            # Extract car count
            car_count_row = df[df.iloc[:, 0] == 'Car Count']
            if not car_count_row.empty:
                # Find the first non-NaN value after 'Car Count'
                car_count_values = car_count_row.iloc[0, 1:].dropna()
                if not car_count_values.empty:
                    data['car_count'] = BigoSalesSummaryExtractor.safe_convert(car_count_values.iloc[0], int)

            # Extract data for specific rows
            rows_to_extract = ['Tires Total:', 'ALIGNMENTS', 'NITROGEN', 'Shop Supplies Total:',
                               'Sales & Service Total:']
            for row_name in rows_to_extract:
                row = df[df.iloc[:, 0] == row_name]
                if not row.empty:
                    row_data = BigoSalesSummaryExtractor.extract_row_data(row.iloc[0])
                    if row_data:
                        if row_name == 'Tires Total:':
                            data['tire_count'] = row_data['parts_quantity']
                        elif row_name == 'ALIGNMENTS':
                            data['alignment_count'] = row_data['labor_quantity']
                        elif row_name == 'NITROGEN':
                            data['nitrogen_count'] = row_data['labor_quantity']
                        elif row_name == 'Shop Supplies Total:':
                            data['supplies_revenue'] = row_data['parts_amount']
                        elif row_name == 'Sales & Service Total:':
                            data['parts_revenue'] = row_data['parts_amount']
                            data['labor_quantity'] = row_data['labor_quantity']
                            data['labor_revenue'] = row_data['labor_amount']
                            data['total_revenue_w_supplies'] = row_data['total_sales']
                            data['gross_profit_w_supplies'] = row_data['gross_profit_amount']

            # Calculate gross_profit_no_supplies
            data['gross_profit_no_supplies'] = int(data['gross_profit_w_supplies'] - data['supplies_revenue'])

            return pd.DataFrame([data])
        except Exception as e:
            # print(f"Error in extract_required_data: {str(e)}")
            # print("DataFrame contents:")
            # print(df)
            raise

    @staticmethod
    def extract_ss_data(file_path):
        try:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            store_number = int(file_name.split('_')[1])

            # First, read the Excel file to determine the number of columns
            df_test = pd.read_excel(file_path, engine="xlrd", nrows=1)
            num_cols = len(df_test.columns)
            # print(f"Number of columns in the Excel file: {num_cols}")

            # Now read the entire file with the correct number of columns
            df = pd.read_excel(file_path, engine="xlrd", usecols=range(num_cols))

            # Find the date
            date_row = df[df.iloc[:, 0].str.contains("Selected Date:", na=False)]
            if date_row.empty:
                raise ValueError("Unable to find 'Selected Date:' in the Excel file")
            date_str = date_row.iloc[0, 0].split(":")[1].strip()
            date = datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")

            # Add wenco_id and date to the dataframe
            df['wenco_id'] = store_number
            df['date'] = date

            # print("DataFrame after reading:")
            # print(df)

            # Extract required data
            result_df = BigoSalesSummaryExtractor.extract_required_data(df)

            return result_df

        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            raise

    @staticmethod
    def delete_existing_records(df):
        with ENGINE.begin() as conn:
            for _, row in df.iterrows():
                query = text(f"DELETE FROM {BIGO_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date")
                result = conn.execute(query, {'wenco_id': row['wenco_id'], 'date': row['date']})
                print(f"Query executed: DELETE FROM {BIGO_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date with params wenco_id={row['wenco_id']} and date={row['date']}")
                print(f"Number of rows deleted: {result.rowcount}")

if __name__ == "__main__":
    file_path = r"C:\WencoClear\Reports_Archive\Bigo\sales_summaries\BGO_14_SS_2024-07-31.XLS"
    extractor = BigoSalesSummaryExtractor()
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    try:
        df = extractor.extract_ss_data(file_path)
        print("Final DataFrame:")
        print(df)
    except Exception as e:
        print(f"An error occurred: {str(e)}")