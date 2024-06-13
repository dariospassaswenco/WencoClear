import pandas as pd
import os
from datetime import datetime
from data_models.bigo import BigoTechSummary

class BigoTechExtractor:
    @staticmethod
    def process_tech_data(df):
        tech_name = df.iloc[3]['Store_or_Category'].split('For: ')[1]
        date_str = df.iloc[2]['Store_or_Category'].split('Date Range: ')[1].split(' to ')[0]

        # Convert date to year-month-day format
        date = datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')

        # Initialize default values
        car_count_total = 0
        tire_quantity = 0
        alignments = 0
        nitrogens = 0
        revenue = 0
        gross_profit = 0
        parts_revenue = 0
        labor_quantity = 0
        labor_cost = 0

        # Locate Car Count
        try:
            car_count = df.loc[df['Car Count Label'] == 'Car Count']
            car_count_total = car_count['Car Count Number'].iloc[0]
        except Exception:
            pass

        # Locate row with Parts Quantity for Tire Count
        try:
            tires_total = df.loc[df['Store_or_Category'] == 'Tires Total:']
            tire_quantity = tires_total['Parts Quantity'].iloc[0]
        except Exception:
            pass

        # Locate row with Alignments
        try:
            alignments_total = df.loc[df['Store_or_Category'] == 'ALIGNMENTS']
            alignments = alignments_total['Labor Quantity'].iloc[0]
        except Exception:
            pass

        # Locate row with Nitrogen
        try:
            nitrogen_total = df.loc[df['Store_or_Category'] == 'NITROGEN']
            nitrogens = nitrogen_total['Labor Quantity'].iloc[0]
        except Exception:
            pass

        # Locate row with Total Sales and other values
        try:
            sales_service_total = df.loc[df['Store_or_Category'] == 'Sales & Service Total:']
            revenue = sales_service_total['Total Sales'].iloc[0]
            gross_profit = sales_service_total['GP'].iloc[0]
            parts_revenue = sales_service_total['Parts Revenue'].iloc[0]
            labor_quantity = sales_service_total['Labor Quantity'].iloc[0]
            labor_cost = sales_service_total['Labor Cost'].iloc[0]
        except Exception:
            pass

        # Create a dictionary with technician's data
        tech_summary = BigoTechSummary(
            first_name=tech_name.split(', ')[0],
            last_name=tech_name.split(' ')[1] if len(tech_name.split(' ')) > 1 else '',
            date=date,
            car_count=car_count_total,
            tire_count=tire_quantity,
            alignment_count=alignments,
            nitrogen_count=nitrogens,
            parts_revenue=parts_revenue,
            tech_hours_flagged=labor_quantity,
            labor_revenue=labor_cost,
            total_revenue=revenue,
            gross_profit=gross_profit
        )

        return tech_summary

    @staticmethod
    def extract_tech_data(file_path):
        try:
            df = pd.read_excel(file_path, engine="xlrd", skiprows=0, usecols=[0, 1, 8, 10, 15, 20, 24, 33, 37])

            df.columns = ['Store_or_Category', 'Car Count Label', 'Car Count Number', 'Parts Quantity',
                          'Parts Revenue', 'Labor Quantity', 'Labor Cost', 'GP', 'Total Sales']

            new_tech_indices = df[df['Store_or_Category'].str.contains(r'Store No\.', na=False)].index.tolist()
            tech_data = []

            for i in range(len(new_tech_indices)):
                start_index = new_tech_indices[i]
                end_index = new_tech_indices[i + 1] if i < len(new_tech_indices) - 1 else len(df)

                # Extract data for each technician based on start and end indices
                tech_df = df.iloc[start_index:end_index]
                tech_info = BigoTechExtractor.process_tech_data(tech_df)
                tech_data.append(tech_info.__dict__)

            return pd.DataFrame(tech_data)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return pd.DataFrame()
