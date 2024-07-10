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

    future_dates_sba = {store: [test_date] for store in limited_midas_store_numbers}

    print("Midas SBA Summary Data to be passed:")
    print(future_dates_sba)

    midas_generator = MidasReportGenerator()
    midas_generator.prepare_pos()

    # Test Sales Summary Report
    print("Testing Midas Sales Summary Report")
    midas_generator.generate_sales_by_category_reports(future_dates_sba)

    midas_generator.actions.app.kill()  # Close POS
    print("Midas Reports Test Completed")


if __name__ == "__main__":
    test_midas_reports()
