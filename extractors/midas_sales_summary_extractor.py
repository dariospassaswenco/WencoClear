#extractors/midas_sales_summary_extractor
import re
import pdfplumber
import pandas as pd
from datetime import datetime
from data_models.midas import MidasSalesSummary
from config.app_settings import *
import os
from sqlalchemy import text

class MidasSalesSummaryExtractor:
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
    def extract_date(lines):
        for line in lines:
            if re.match(r"^For the Period", line):
                date_match = re.findall(r"\d{1,2}/\d{1,2}/\d{4}", line)
                if len(date_match) >= 2:
                    return datetime.strptime(date_match[0], '%m/%d/%Y').strftime('%Y-%m-%d')
        return None

    @staticmethod
    def extract_car_count(lines):
        for line in lines:
            if "Total Number of Repair Orders for Period" in line:
                car_count_match = re.search(r"\d+", line)
                if car_count_match:
                    return int(car_count_match.group())
        return None

    @staticmethod
    def extract_gross_profit_data(lines):
        gross_profit_started = False
        gross_profit_data = []
        for line in lines:
            if "Gross Profit (*Breakout)" in line or "Gross Profit (*breakout)" in line:
                gross_profit_started = True
            elif "w/o Supplies w/ Supplies Non Taxable Fees" in line:
                break
            elif gross_profit_started:
                gross_profit_data.append(line)
        return gross_profit_data

    @staticmethod
    def parse_gross_profit_data(gross_profit_data, parsed_data):
        for line in gross_profit_data:
            if line.startswith("Parts "):
                parts_data = re.findall(r"[\d.,]+", line)
                if len(parts_data) >= 3:
                    parsed_data.parts_revenue, parsed_data.parts_cost, parsed_data.parts_gp = map(
                        lambda x: float(x.replace(",", "")), parts_data[:3])
            elif line.startswith("Labor "):
                labor_data = re.findall(r"[\d.,]+", line)
                if len(labor_data) >= 3:
                    parsed_data.labor_revenue, parsed_data.labor_cost, parsed_data.labor_gp = map(
                        lambda x: float(x.replace(",", "")), labor_data[:3])
            elif line.startswith("* Parts "):
                tire_data = re.findall(r"[\d.,]+", line)
                if len(tire_data) >= 3:
                    parsed_data.tire_revenue, parsed_data.tire_cost, parsed_data.tire_gp = map(
                        lambda x: float(x.replace(",", "")), tire_data[:3])
            elif line.startswith("Total "):
                total_data = re.findall(r"[\d.,]+", line)
                if len(total_data) >= 3:
                    parsed_data.total_revenue_w_supplies, _, parsed_data.gp_w_supplies = map(
                        lambda x: float(x.replace(",", "")), total_data[:3])
        return parsed_data

    @staticmethod
    def extract_supplies(lines):
        supplies = {'taxable_supplies': 0, 'non_tax_supplies': 0}
        for line in lines:
            if line.startswith("Taxable Supplies"):
                match = re.search(r'\$([\d,.]+)', line)
                if match:
                    supplies['taxable_supplies'] = float(match.group(1).replace(',', ''))
            if line.startswith("Non Tax Supplies"):
                match = re.search(r'\$([\d,.]+)', line)
                if match:
                    supplies['non_tax_supplies'] = float(match.group(1).replace(',', ''))
        return supplies

    @staticmethod
    def extract_ss_data(file_path):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        store_number = int(file_name.split('_')[1])  # Convert store_number to int for wenco_id

        midas_summary = MidasSalesSummary(wenco_id=store_number)

        try:
            lines = MidasSalesSummaryExtractor.extract_lines(file_path)

            midas_summary.date = MidasSalesSummaryExtractor.extract_date(lines)
            midas_summary.car_count = MidasSalesSummaryExtractor.extract_car_count(lines)

            gross_profit_data = MidasSalesSummaryExtractor.extract_gross_profit_data(lines)
            parsed_gross_profit = MidasSalesSummaryExtractor.parse_gross_profit_data(gross_profit_data, midas_summary)

            for key, value in parsed_gross_profit.__dict__.items():
                setattr(midas_summary, key, value)

            supplies = MidasSalesSummaryExtractor.extract_supplies(lines)
            midas_summary.supplies_revenue = supplies['taxable_supplies'] + supplies['non_tax_supplies']
            midas_summary.total_revenue_w_supplies += midas_summary.supplies_revenue
            midas_summary.gp_w_supplies += midas_summary.supplies_revenue

            # Convert to dictionary for dataframe
            result = midas_summary.__dict__
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
    # Function to delete existing records for Midas Sales Summary
    def delete_existing_records(df):
        with ENGINE.begin() as conn:
            for _, row in df.iterrows():
                query = text(f"DELETE FROM {MIDAS_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date")
                result = conn.execute(query, {'wenco_id': row['wenco_id'], 'date': row['date']})
                print(
                    f"Query executed: DELETE FROM {MIDAS_SS_TABLE} WHERE wenco_id = :wenco_id AND date = :date with params wenco_id={row['wenco_id']} and date={row['date']}")
                print(f"Number of rows deleted: {result.rowcount}")