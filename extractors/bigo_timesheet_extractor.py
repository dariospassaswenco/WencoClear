import pandas as pd
import os
from datetime import datetime
from config.app_settings import BIGO_POS_CTRL_MAP, OUTPUTS
from data_models.bigo import BigoTimesheet
from config.app_settings import ENGINE, BIGO_TIMESHEET_TABLE


class BigoTimesheetExtractor:
    @staticmethod
    def extract_timesheet_data(file_path):
        try:
            # Read Excel file into DataFrame
            df = pd.read_excel(file_path, engine="xlrd", skiprows=3, usecols=[4, 5, 6, 12])

            # Rename the columns for better understanding
            df.columns = ['Store', 'Date', 'Employee Name', 'Hours']

            # Fill missing values in the 'Employee Name' and 'Shop Store' columns with forward values
            df['Employee Name'] = df['Employee Name'].ffill()
            df['Store'] = df['Store'].ffill()

            # Iterate through the DataFrame and replace lines starting with "BIGO TIRES"
            prev_name = None
            for idx, row in df.iterrows():
                if row['Employee Name'].startswith("BIGO TIRES"):
                    if prev_name is not None:
                        df.at[idx, 'Employee Name'] = prev_name
                else:
                    prev_name = row['Employee Name']

            prev_name = None
            for idx, row in df.iterrows():
                if row['Employee Name'].startswith("BIG O TIRES"):
                    if prev_name is not None:
                        df.at[idx, 'Employee Name'] = prev_name
                else:
                    prev_name = row['Employee Name']

            # Drop rows with NaN values in the 'Date' column
            df = df.dropna(subset=['Date'])

            # Split names into components and assign to first_name and last_name
            df['components'] = df['Employee Name'].str.split(' ')
            df['last_name'] = df['components'].str[-2]  # Second-to-last element
            df['first_name'] = df['components'].str[-1]  # Last element

            # Rearrange the order of the columns
            df = df[['Store', 'Date', 'first_name', 'last_name', 'Hours']]

            # Ensure the 'Store' column values are strings before mapping
            df['Store'] = df['Store'].astype(str).str.split('.').str[0]

            # Apply store mapping to 'Store' column in DataFrame
            df['Store'] = df['Store'].replace(BIGO_POS_CTRL_MAP)

            # Explicitly infer types after replacing values to avoid warnings
            df = df.infer_objects(copy=False)

            # Convert 'Date' Column to date format
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

            # Add the date_entered column
            date_entered = datetime.now().strftime('%Y-%m-%d')
            df['date_entered'] = date_entered

            # Convert to list of BigoTimesheet dataclass instances
            timesheet_entries = [
                BigoTimesheet(
                    wenco_id=row['Store'],
                    date=row['Date'],
                    date_entered=row['date_entered'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    hours=row['Hours']
                ).__dict__ for index, row in df.iterrows()
            ]

            return pd.DataFrame(timesheet_entries)

        except Exception as e:
            print(f"Error processing file: {e}")
            return pd.DataFrame()

    @staticmethod
    def delete_existing_records(df):
        with ENGINE.connect() as conn:
            for _, row in df.iterrows():
                query = text(
                    f"SELECT date_entered FROM {BIGO_TIMESHEET_TABLE} WHERE wenco_id = :wenco_id AND last_name = :last_name AND date = :date")
                result = conn.execute(query, {'wenco_id': row['wenco_id'], 'last_name': row['last_name'],
                                              'date': row['date']}).fetchone()
                if result:
                    existing_date_entered = datetime.strptime(result['date_entered'], '%Y-%m-%d')
                    new_date_entered = datetime.strptime(row['date_entered'], '%Y-%m-%d')
                    if new_date_entered > existing_date_entered:
                        delete_query = text(
                            f"DELETE FROM {BIGO_TIMESHEET_TABLE} WHERE wenco_id = :wenco_id AND last_name = :last_name AND date = :date")
                        conn.execute(delete_query,
                                     {'wenco_id': row['wenco_id'], 'last_name': row['last_name'], 'date': row['date']})
                        print(
                            f"Deleted existing record for wenco_id {row['wenco_id']}, last_name {row['last_name']} and date {row['date']}")

if __name__ == '__main__':
    # Test the extraction with a sample file path
    sample_file_path = os.path.join(OUTPUTS, "BGO_TS_TS_2024-02-11.XLS")
    extractor = BigoTimesheetExtractor()
    df = extractor.extract_timesheet_data(sample_file_path)
    print(df)
