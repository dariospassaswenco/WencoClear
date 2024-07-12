from datetime import datetime
from config.app_settings import BIGO_STORE_NUMBERS, BIGO_SBA_TABLE
from database.sales_by_category_data import get_missing_sales_by_category_dates
from generators.bigo_report_generator import BigoReportGenerator

def progress_callback(message):
    print(message)

def stop_requested():
    # In a real application, this would be a flag or check to see if the user requested to stop the operation.
    return False

def test_generate_bigo_sbc_reports():
    start_date = datetime.strptime('2024-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2024-06-30', '%Y-%m-%d')

    progress_callback("Fetching missing SBC data for Bigo stores...")

    sbc_bigo = get_missing_sales_by_category_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SBA_TABLE)

    if not sbc_bigo:
        progress_callback("All SBC data for Bigo is up to date.")
        return

    progress_callback(f"Missing SBC data for Bigo: {sbc_bigo}")

    bigo_generator = BigoReportGenerator()
    bigo_generator.prepare_pos()

    try:
        bigo_generator.generate_sbc_reports(sbc_bigo)
    except Exception as e:
        progress_callback(f"Error generating Bigo SBC reports: {e}. Retrying...")
        bigo_generator.restart_pos()
        bigo_generator.generate_sbc_reports(sbc_bigo)

    bigo_generator.actions.app.kill()  # Close POS
    progress_callback("Bigo SBC Reports Generated.")

if __name__ == '__main__':
    test_generate_bigo_sbc_reports()
