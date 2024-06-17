import re
import pdfplumber
import pandas as pd
from datetime import datetime
from data_models.midas import MidasTechSummary
from config.app_settings import MIDAS_ADDRESS_MAP, ENGINE, MIDAS_TECH_TABLE
from sqlalchemy import text


class MidasTechExtractor:
    @staticmethod
    def extract_lines(file_path):
        lines = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                for line in text.split('\n'):
                    lines.append(line.strip())
        return lines

    @staticmethod
    def extract_tech_data(file_path):
        lines = MidasTechExtractor.extract_lines(file_path)
        all_data = []

        store_address = lines[1]  # Assume address is always in the second line
        store_number = MIDAS_ADDRESS_MAP.get(store_address)

        date_pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{4})")
        date_str = None
        for line in lines:
            date_match = date_pattern.search(line)
            if date_match:
                date_str = datetime.strptime(date_match.group(), "%m/%d/%Y").strftime("%Y-%m-%d")
                break

        for line in lines:
            tech_pattern = r"([A-Z]+)\s+([A-Z]+)\s+([A-Z]+)\s+(\d+\.\d+)\s+\$([\d,]+\.\d+)\s+\$([\d,]+\.\d+)\s+(\d+)\s+\$([\d,]+\.\d+)"
            tech_info = re.search(tech_pattern, line)
            if tech_info:
                info = tech_info.groups()
                tech_summary = MidasTechSummary(
                    wenco_id=store_number,
                    first_name=info[1],
                    last_name=info[2],
                    date=date_str,
                    tech_hours_flagged=float(info[3]),
                    labor_revenue=float(info[4].replace(',', '')),
                    part_revenue=float(info[5].replace(',', '')),
                    car_count=int(info[6]),
                    total_revenue=float(info[7].replace(',', ''))
                )
                all_data.append(tech_summary.__dict__)

        df = pd.DataFrame(all_data)
        return df

    @staticmethod
    def delete_existing_records(df):
        with ENGINE.connect() as conn:
            for _, row in df.iterrows():
                # Check if the record exists
                check_query = text(
                    f"SELECT COUNT(*) FROM {MIDAS_TECH_TABLE} WHERE wenco_id = :wenco_id AND date = :date")
                result = conn.execute(check_query, {'wenco_id': row['wenco_id'], 'date': row['date']}).scalar()

                if result > 0:
                    # If the record exists, delete it
                    delete_query = text(f"DELETE FROM {MIDAS_TECH_TABLE} WHERE wenco_id = :wenco_id AND date = :date")
                    conn.execute(delete_query, {'wenco_id': row['wenco_id'], 'date': row['date']})
                    print(f"Deleted existing record for wenco_id {row['wenco_id']} and date {row['date']}")