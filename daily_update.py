import pandas as pd
from datetime import datetime, timedelta
from config.app_settings import ENGINE, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE, BIGO_STORE_NUMBERS, BIGO_SS_TABLE, MIDAS_SBA_TABLE, BIGO_SBA_TABLE
from database.ss_data import get_missing_ss_dates
from database.sales_by_category_data import get_missing_sales_by_category_dates
from database.tech_data import get_missing_midas_tech_dates, get_missing_bigo_tech_dates
from generators.midas_report_generator import MidasReportGenerator
from generators.helpers import break_into_payroll_periods
from generators.bigo_report_generator import BigoReportGenerator


def midas_daily_update(start_date, end_date):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    midas_missing_ss = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
    print(f"midas missing ss: {midas_missing_ss}")
    midas_missing_tech = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
    print(f"midas missing tech: {midas_missing_tech}")
    timesheet_midas = {store: [(start_date_str, end_date_str)] for store in MIDAS_STORE_NUMBERS}
    print(f"midas timesheet: {timesheet_midas}")
    missing_sales_by_category = get_missing_sales_by_category_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SBA_TABLE)
    print(f"midas sales by category: {missing_sales_by_category}")

    midas_generator = MidasReportGenerator()
    midas_generator.prepare_pos()
    if midas_missing_ss:
        midas_generator.generate_ss_reports(midas_missing_ss)
        print("Midas sales summaries updated")
    if midas_missing_tech:
        midas_generator.generate_tech_reports(midas_missing_tech)
        print("Midas tech updated")
    if timesheet_midas:
        midas_generator.generate_timesheet_reports(timesheet_midas)
        print("Midas timesheets updated")
    if missing_sales_by_category:
        midas_generator.generate_sales_by_category_reports(missing_sales_by_category)
        print("Midas sales by category updated")
    midas_generator.actions.app.kill()
    print("Midas reports updated successfully")

def bigo_daily_update(start_date, end_date):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Check for missing sales summary data
    bigo_missing_ss = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
    print(f"bigo missing ss: {bigo_missing_ss}")
    bigo_missing_tech = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
    print(f"bigo missing tech: {bigo_missing_tech}")
    timesheet_bigo = [(start_date_str, end_date_str)]
    timesheet_bigo = break_into_payroll_periods(timesheet_bigo)
    print(f"bigo timesheet: {timesheet_bigo}")
    missing_sales_by_category = get_missing_sales_by_category_dates(start_date, end_date, BIGO_STORE_NUMBERS,
                                                                    BIGO_SBA_TABLE)
    print(f"bigo sales by category: {missing_sales_by_category}")

    bigo_generator = BigoReportGenerator()
    bigo_generator.prepare_pos()
    if bigo_missing_ss:
        bigo_generator.generate_ss_reports(bigo_missing_ss)
        print("Bigo sales summaries updated")
    if bigo_missing_tech:
        bigo_generator.generate_tech_reports(bigo_missing_tech)
        print("Bigo tech updated")
    if timesheet_bigo:
        bigo_generator.generate_timesheet_reports(timesheet_bigo)
        print("Bigo timesheet updated")
    if missing_sales_by_category:
        bigo_generator.generate_sbc_reports(missing_sales_by_category)
        print("Bigo SBC updated")
    bigo_generator.actions.app.kill()
    print("Bigo reports updated successfully")



def run_daily_update():
    # Get the current date and the date a week prior
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=7)
    print(f"Updating reports for date range {start_date} to {end_date}")

    try:
        midas_daily_update(start_date, end_date)
    except Exception as e:
        print(f"Error generating Midas reports: {e}. Retrying...")
        midas_daily_update(start_date, end_date)

    try:
        bigo_daily_update(start_date, end_date)
    except Exception as e:
        print(f"Error generating Bigo reports: {e}. Retrying...")
        bigo_daily_update(start_date, end_date)

if __name__ == "__main__":
    run_daily_update()
