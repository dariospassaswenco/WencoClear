from datetime import datetime, timedelta
from generators.midas_report_generator import MidasReportGenerator
from generators.bigo_report_generator import BigoReportGenerator
from navigation.ro_basic_navigation import MidasNavigation
from navigation.navex_basic_navigation import BigoNavigation
from config.app_settings import *

def test_midas_reports():
    print("Testing Midas Reports")

    # Generate future dates
    start_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    end_date = (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d')
    future_dates = {store: [start_date] for store in MIDAS_STORE_NUMBERS}

    midas_navigation = MidasNavigation()
    midas_navigation.prepare_pos()

    midas_generator = MidasReportGenerator()
    midas_generator.prepare_pos()

    # Test Sales Summary Report
    print("Testing Midas Sales Summary Report")
    midas_generator.generate_ss_reports(future_dates)

    # Test Tech Report
    print("Testing Midas Tech Report")
    midas_generator.generate_tech_reports(future_dates)

    # Test Timesheet Report
    print("Testing Midas Timesheet Report")
    midas_generator.generate_timesheet_reports(future_dates)

    midas_navigation.close_pos()
    print("Midas Reports Test Completed")


def test_bigo_reports():
    print("Testing Bigo Reports")

    # Generate future dates
    start_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    end_date = (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d')
    future_dates = {store: [start_date] for store in BIGO_STORE_NUMBERS}
    future_dates_list = [start_date]

    bigo_navigation = BigoNavigation()
    bigo_navigation.prepare_pos()

    bigo_generator = BigoReportGenerator()
    bigo_generator.prepare_pos()

    # Test Sales Summary Report
    print("Testing Bigo Sales Summary Report")
    bigo_generator.generate_ss_reports(future_dates)

    # Test Tech Report
    print("Testing Bigo Tech Report")
    bigo_generator.generate_tech_reports(future_dates_list)

    # Test Timesheet Report
    print("Testing Bigo Timesheet Report")
    bigo_generator.generate_timesheet_reports(future_dates_list)

    bigo_navigation.close_pos()
    print("Bigo Reports Test Completed")


if __name__ == "__main__":
    test_midas_reports()
    test_bigo_reports()
