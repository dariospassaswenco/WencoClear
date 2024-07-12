import pandas as pd
from data_models.bigo import BigoSalesByCategory
import os
import numpy as np
from datetime import datetime


class BigoSalesByCategoryExtractor:
    @staticmethod
    def extract_sbc_data(file_path):
        try:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            store_number = int(file_name.split('_')[1])

            def find_column_indices_and_date(file_path):
                # Read the first 20 rows to ensure we capture the 'Selected Date:' line
                df_test = pd.read_excel(file_path, engine="xlrd", nrows=20)

                # Find the date
                date_row = df_test[df_test.iloc[:, 0].str.contains("Selected Date:", na=False)].iloc[0, 0]
                date_str = date_row.split(":")[1].strip()
                date = datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")

                # Find the row index of 'Sales Group'
                sales_group_row = df_test[df_test.iloc[:, 0] == 'Sales Group'].index[0]

                # Get the row below 'Sales Group'
                data_row = df_test.iloc[sales_group_row + 1]

                # Find non-empty cells in this row
                non_empty_indices = np.where(~pd.isnull(data_row))[0]

                return non_empty_indices.tolist(), date

            # Get the column indices and date
            column_indices, date = find_column_indices_and_date(file_path)
            print("Column indices:", column_indices)
            print("Extracted date:", date)

            # Now you can use these indices to read the specific columns you need
            df = pd.read_excel(file_path, engine="xlrd", usecols=column_indices)

            # Rename the columns for easier access
            new_columns = ['Category', 'parts_quantity', 'parts_sales', 'labor_quantity', 'labor_sales',
                           'discounts_quantity', 'discounts_amount', 'ext_cost', 'gross_profit_percent',
                           'gross_profit', 'total_sales']
            df.columns = new_columns[:len(df.columns)]  # In case there are fewer columns than expected

            # Find the row index where actual data starts (row after 'Sales Group')
            start_row = df[df['Category'] == 'Sales Group'].index[0] + 1

            # Slice the dataframe to include only the relevant data
            df = df.iloc[start_row:].reset_index(drop=True)

            # Clean the DataFrame
            df = BigoSalesByCategoryExtractor.clean_dataframe(df)

            # Add wenco_id and date columns
            df['wenco_id'] = store_number
            df['date'] = date

            # Reorder columns to match BigoSalesByCategory dataclass
            column_order = ['wenco_id', 'date', 'Category'] + [col for col in new_columns if col != 'Category']
            df = df.reindex(columns=column_order)

            # Rename 'Category' to 'sales_category' to match the dataclass
            df = df.rename(columns={'Category': 'sales_category'})

            print("Cleaned DataFrame:")
            print(df)

            return df

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return pd.DataFrame()

    @staticmethod
    def clean_dataframe(df):
        # Remove rows where 'Category' is NaN
        df = df.dropna(subset=['Category'])

        # Define rows to exclude
        rows_to_exclude = [
            'Sales, Service, & Fees Total',
            'Sales, Service, Fees & Variance',
            'Total:',
            'FREE SERVICE CHECKS',
            'Invoice Count',
            'Car Count'
        ]

        # Remove specified rows and rows containing 'Total:'
        df = df[~df['Category'].isin(rows_to_exclude) & ~df['Category'].str.contains('Total:', na=False)]

        # Convert numeric columns to float, replacing any remaining NaNs with 0
        numeric_columns = df.columns[1:]  # All columns except 'Category'
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Remove rows where all numeric columns are 0
        df = df[(df[numeric_columns] != 0).any(axis=1)]

        # Reset the index after dropping rows
        df = df.reset_index(drop=True)

        return df


# Test the function
if __name__ == "__main__":
    file_path = r"C:\Users\Wenco\Documents\WencoClearOutputs\BGO_15_SBA_2024-07-10.XLS"
    extractor = BigoSalesByCategoryExtractor()
    df = extractor.extract_sbc_data(file_path)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    print(df)