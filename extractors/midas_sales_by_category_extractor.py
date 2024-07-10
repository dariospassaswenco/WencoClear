import re
import pdfplumber
import pandas as pd
from config.app_settings import MIDAS_ADDRESS_MAP
from datetime import datetime
from data_models.midas import MidasSalesByCategory

class MidasSalesByCategoryExtractor:
    @staticmethod
    def extract_sales_by_category_data(file_path):
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages)

        lines = text.split('\n')
        date = MidasSalesByCategoryExtractor.extract_date(lines)
        wenco_id = MidasSalesByCategoryExtractor.extract_wenco_id(lines)

        sales_data = []
        for line in lines:
            print(f"Processing line: {line}")  # Debug print
            if line.strip().startswith("DISCOUNTS"):
                data = MidasSalesByCategoryExtractor.parse_discount_line(line, date, wenco_id)
            else:
                data = MidasSalesByCategoryExtractor.parse_regular_line(line, date, wenco_id)
            if data:
                sales_data.append(data)
            else:
                print(f"Failed to parse line: {line}")  # Debug print

        df = pd.DataFrame([vars(sale) for sale in sales_data])
        return df if not df.empty else pd.DataFrame()

    @staticmethod
    def extract_date(lines):
        for line in lines:
            if "Labor Category :All Labor Categories" in line:
                date_range_str = lines[lines.index(line) + 1].strip()
                try:
                    start_date_str = date_range_str.split(' To ')[0]
                    date_obj = datetime.strptime(start_date_str, "%m/%d/%Y")
                    return date_obj.strftime("%Y-%m-%d")
                except (ValueError, IndexError) as e:
                    print(f"Unable to parse date: {date_range_str}. Error: {e}")
                    return date_range_str
        return ""

    @staticmethod
    def extract_wenco_id(lines):
        for line in lines:
            if "Midas Auto Service & Tires" in line:
                address = lines[lines.index(line) + 1].strip()
                return MIDAS_ADDRESS_MAP.get(address, "Unknown")
        return "Unknown"

    @staticmethod
    def parse_discount_line(line, date, wenco_id):
        parts = line.split()
        if len(parts) == 14 and parts[0] == "DISCOUNTS":
            try:
                values = [
                    float(parts[1]),  # jobs
                    float(parts[2]),  # time
                    MidasSalesByCategoryExtractor.clean_number(parts[3]),  # labor
                    MidasSalesByCategoryExtractor.clean_number(parts[4]),  # parts
                    MidasSalesByCategoryExtractor.clean_number(parts[5]),  # other
                    MidasSalesByCategoryExtractor.clean_number(parts[6]),  # total
                    float(parts[7]),  # cost_of_stock_inv
                    float(parts[8]),  # cost_of_non_stock
                    float(parts[9]),  # sublet_costs
                    float(parts[10]),  # labor_costs
                    float(parts[11]),  # total_costs
                    float(parts[12].rstrip('%')) / 100,  # profit (percentage to decimal)
                    MidasSalesByCategoryExtractor.clean_number(parts[13].lstrip('$'))  # job_avg
                ]

                return MidasSalesByCategory(
                    wenco_id=wenco_id,
                    category="DISCOUNTS",
                    date=date,
                    jobs=values[0],
                    time=values[1],
                    labor=values[2],
                    parts=values[3],
                    other=values[4],
                    total=values[5],
                    cost_of_stock_inv=values[6],
                    cost_of_non_stock=values[7],
                    sublet_costs=values[8],
                    labor_costs=values[9],
                    total_costs=values[10],
                    profit=values[11],
                    job_avg=values[12]
                )
            except (ValueError, IndexError) as e:
                print(f"Error parsing discount line: {line}")
                print(f"Error details: {e}")
        else:
            print(f"Not a valid discount line: {line}")
        return None

    @staticmethod
    def parse_regular_line(line, date, wenco_id):
        pattern = r"(.*?)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)%\s+\$([\d,().-]+)"
        match = re.search(pattern, line)
        if match:
            category = match.group(1).strip()
            values = [MidasSalesByCategoryExtractor.clean_number(v) for v in match.groups()[1:]]
            if len(values) == 13:
                return MidasSalesByCategory(
                    wenco_id=wenco_id,
                    category=category,
                    date=date,
                    jobs=values[0],
                    time=values[1],
                    labor=values[2],
                    parts=values[3],
                    other=values[4],
                    total=values[5],
                    cost_of_stock_inv=values[6],
                    cost_of_non_stock=values[7],
                    sublet_costs=values[8],
                    labor_costs=values[9],
                    total_costs=values[10],
                    profit=values[11] / 100,  # Convert percentage to decimal
                    job_avg=values[12]
                )
        return None

    @staticmethod
    def clean_number(value):
        # Remove commas, dollar signs, and handle parentheses for negative values
        cleaned = value.replace(',', '').replace('$', '').replace('(', '-').replace(')', '')
        return float(cleaned) if cleaned else 0.0