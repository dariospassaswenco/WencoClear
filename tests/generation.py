from datetime import datetime, timedelta
from generators.midas_report_generator import MidasReportGenerator
from generators.bigo_report_generator import BigoReportGenerator
from config.app_settings import MIDAS_STORE_NUMBERS, BIGO_STORE_NUMBERS

def test_midas_reports():
    print("Testing Midas Reports")

    # Generate future dates
    test_date = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')

    # Limit to the first three Midas stores
    limited_midas_store_numbers = {store: MIDAS_STORE_NUMBERS[store] for store in list(MIDAS_STORE_NUMBERS)[:3]}

    future_dates_ss = {store: [test_date] for store in limited_midas_store_numbers}
    future_dates_tech_ts = {store: [(test_date, test_date)] for store in limited_midas_store_numbers}

    print("Midas Sales Summary Data to be passed:")
    print(future_dates_ss)

    print("Midas Tech Data to be passed:")
    print(future_dates_tech_ts)

    print("Midas Timesheet Data to be passed:")
    print(future_dates_tech_ts)

    midas_generator = MidasReportGenerator()
    midas_generator.prepare_pos()

    # Test Sales Summary Report
    print("Testing Midas Sales Summary Report")
    midas_generator.generate_ss_reports(future_dates_ss)

    # Test Tech Report
    print("Testing Midas Tech Report")
    midas_generator.generate_tech_reports(future_dates_tech_ts)

    # Test Timesheet Report
    print("Testing Midas Timesheet Report")
    midas_generator.generate_timesheet_reports(future_dates_tech_ts)

    midas_generator.actions.app.kill()  # Close POS
    print("Midas Reports Test Completed")

def test_bigo_reports():
    print("Testing Bigo Reports")

    # Generate future dates
    test_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    future_dates_ss = {store: [test_date] for store in BIGO_STORE_NUMBERS}
    future_dates_list = [(test_date, test_date)]

    print("Bigo Sales Summary Data to be passed:")
    print(future_dates_ss)

    print("Bigo Tech Data to be passed:")
    print(future_dates_list)

    print("Bigo Timesheet Data to be passed:")
    print(future_dates_list)

    bigo_generator = BigoReportGenerator()
    bigo_generator.prepare_pos()

    # Test Sales Summary Report
    print("Testing Bigo Sales Summary Report")
    bigo_generator.generate_ss_reports(future_dates_ss)

    # Test Tech Report
    print("Testing Bigo Tech Report")
    bigo_generator.generate_tech_reports(future_dates_list)

    # Test Timesheet Report
    print("Testing Bigo Timesheet Report")
    bigo_generator.generate_timesheet_reports(future_dates_list)

    bigo_generator.actions.app.kill()  # Close POS
    print("Bigo Reports Test Completed")

if __name__ == "__main__":
    test_midas_reports()
    test_bigo_reports()
