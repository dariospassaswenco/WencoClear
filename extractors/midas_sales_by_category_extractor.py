import re
import pdfplumber
import pandas as pd
from config.app_settings import MIDAS_ADDRESS_MAP
from datetime import datetime
from data_models.midas import MidasSalesByCategory

class MidasSalesByCategoryExtractor:
    CATEGORIES = [
        "15K SYSTEM GUARANTEE", "AIR CONDITIONING", "BELTS", "BRAKES",
        "COOLING SYSTEM", "DISCOUNTS", "DRIVE TRAIN", "ELECTRICAL",
        "ENGINE SERVICE", "EXHAUST", "FILTERS", "FLUID FLUSH SERVICE",
        "FREE ALIGNMENT CHECK", "FUEL SYSTEM CLEAN", "LIGHTS, LAMPS, BULBS",
        "OIL CHANGE", "OTHER", "SHOCKS/STRUTS", "SMART OIL 15 K",
        "SMART OIL JOBS", "STARTING & CHARGING", "STEERING/SUSPENSION",
        "TIRE SERVICE", "TRANSMISSION SERVICE", "TUNE UP",
        "WHEEL ALIGNMENT", "WIPER BLADES", "X-BATTERIES",
        "CUSTOMER STATES", "SMART OIL CHANGE 15K", "FACTORY SCHED MAINT",
        "STATE INSPECTION", "SUBLET/OUTSIDE SERV.", "VALVOLINE DRIVES",
        "X-NON ROYALTY", "X-TIRES"
    ]

    CATEGORY_MAPPINGS = {
        "15K SYSTEM": "15K SYSTEM GUARANTEE",
        "FREE ALIGNMENT": "FREE ALIGNMENT CHECK",
        # Add more mappings as needed
    }

    @staticmethod
    def extract_sales_by_category_data(file_path):
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages)

        lines = text.split('\n')
        print(lines)
        date = MidasSalesByCategoryExtractor.extract_date(lines)
        wenco_id = MidasSalesByCategoryExtractor.extract_wenco_id(lines)

        sales_data = []
        for line in lines:
            data = MidasSalesByCategoryExtractor.parse_line(line, date, wenco_id)
            if data:
                sales_data.append(data)

        # Convert the list of MidasSalesByCategory objects to a DataFrame
        df = pd.DataFrame([vars(sale) for sale in sales_data])

        # Check if the DataFrame is empty or if total is zero for all rows
        if df.empty or (df['total'] == 0).all():
            return pd.DataFrame()  # Return an empty DataFrame

        return df

    @staticmethod
    def extract_date(lines):
        for line in lines:
            if "Labor Category :All Labor Categories" in line:
                date_range_str = lines[lines.index(line) + 1].strip()
                try:
                    start_date_str = date_range_str.split(' To ')[0]
                    print(start_date_str)
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
    def parse_line(line, date, wenco_id):
        pattern = r"(\S+(?:\s+\S+)*)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)\s+([\d,().-]+)%\s+\$([\d,().-]+)"
        match = re.search(pattern, line)
        if match:
            category = match.group(1)
            values = [MidasSalesByCategoryExtractor.clean_number(v) for v in match.groups()[1:]]

            # Check if the category needs to be mapped to a full category name
            for partial, full in MidasSalesByCategoryExtractor.CATEGORY_MAPPINGS.items():
                if partial in category:
                    category = full
                    break

            # If the category is not in the CATEGORIES list, skip this line
            if category not in MidasSalesByCategoryExtractor.CATEGORIES:
                return None

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
                    stock=values[6],
                    inv=values[7],
                    non_stock=values[8],
                    sublet=values[9],
                    labor_costs=values[10],
                    costs=values[11],
                    profit=values[11],  # Using costs as profit, adjust if needed
                    job_avg=values[12]
                )
            else:
                print(f"Unexpected number of values for category {category}: {len(values)}")
        return None

    @staticmethod
    def clean_number(value):
        return float(value.replace(',', '').replace('(', '-').replace(')', ''))