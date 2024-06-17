import pandas as pd
import pdfplumber
import os
from datetime import datetime
import re
from collections import namedtuple
from config.app_settings import MIDAS_ADDRESS_MAP, OUTPUTS
from data_models.midas import MidasTimesheet
from config.app_settings import ENGINE, MIDAS_TIMESHEET_TABLE
class MidasTimesheetExtractor:
    @staticmethod
    def extract_lines(file_path):
        lines = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:  # Check if text extraction is successful
                    for line in text.split('\n'):
                        lines.append(line.strip())
        return lines

    @staticmethod
    def extract_timesheet_data(file_path):
        all_data = []
        lines = MidasTimesheetExtractor.extract_lines(file_path)
        date_entered = datetime.now().strftime('%Y-%m-%d')

        if len(lines) >= 4:
            address = lines[3].strip()
        else:
            address = None

        # Extract employee names and their clock info
        employee_lines = []
        current_employee = None
        for i, line in enumerate(lines):
            if line.strip() == "Employee" and i + 1 < len(lines):
                employee_name = lines[i + 1].strip()
                if ',' in employee_name:
                    last_name, first_name = employee_name.split(',', 1)
                else:
                    first_name, last_name = employee_name.split(' ', 1)
                current_employee = {'first_name': first_name.strip(), 'last_name': last_name.strip(), 'clock_data': []}
                employee_lines.append(current_employee)
            elif current_employee is not None:
                clock_data = re.findall(
                    r'(\d{2}/\d{2}/\d{2} \d{2}:\d{2} [AP]M \d{2}/\d{2}/\d{2} \d{2}:\d{2} [AP]M .* \d+\.\d{2})',
                    line)
                current_employee['clock_data'].extend(clock_data)

        # Extract required information and store in 'data'
        for emp in employee_lines:
            for clock_entry in emp['clock_data']:
                parts = clock_entry.split(' ')
                date_in = parts[0]
                hours = float(parts[-1])

                store_id = MIDAS_ADDRESS_MAP.get(address)

                if store_id:
                    timesheet_entry = MidasTimesheet(
                        wenco_id=store_id,
                        date=datetime.strptime(date_in, '%m/%d/%y').strftime('%Y-%m-%d'),
                        date_entered=date_entered,
                        first_name=emp['first_name'],
                        last_name=emp['last_name'],
                        hours=hours
                    )
                    all_data.append(timesheet_entry.__dict__)

        df = pd.DataFrame(all_data)

        return df

    @staticmethod
    def delete_existing_records(df):
        with ENGINE.connect() as conn:
            for _, row in df.iterrows():
                query = text(
                    f"SELECT date_entered FROM {MIDAS_TIMESHEET_TABLE} WHERE wenco_id = :wenco_id AND last_name = :last_name AND date = :date")
                result = conn.execute(query, {'wenco_id': row['wenco_id'], 'last_name': row['last_name'],
                                              'date': row['date']}).fetchone()
                if result:
                    existing_date_entered = datetime.strptime(result['date_entered'], '%Y-%m-%d')
                    new_date_entered = datetime.strptime(row['date_entered'], '%Y-%m-%d')
                    if new_date_entered > existing_date_entered:
                        delete_query = text(
                            f"DELETE FROM {MIDAS_TIMESHEET_TABLE} WHERE wenco_id = :wenco_id AND last_name = :last_name AND date = :date")
                        conn.execute(delete_query,
                                     {'wenco_id': row['wenco_id'], 'last_name': row['last_name'], 'date': row['date']})
                        print(
                            f"Deleted existing record for wenco_id {row['wenco_id']}, last_name {row['last_name']} and date {row['date']}")
if __name__ == '__main__':
    # Test the extraction with a sample file path
    sample_file_path = os.path.join(OUTPUTS, 'mid_2_ts_2024-03-03.pdf')
    extractor = MidasTimesheetExtractor()
    df = extractor.extract_timesheet_data(sample_file_path)
    print(df)
