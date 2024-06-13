from database.ss_data import get_missing_ss_dates
from generators.midas_report_generator import MidasReportGenerator
from navigation.ro_basic_navigation import MidasNavigation
from config.app_settings import *

def fetch_missing_midas_ss_reports(view):
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()
    missing_dates_per_store = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)

    if missing_dates_per_store:
        midas_navigation = MidasNavigation()
        midas_generator = MidasReportGenerator()

        try:
            midas_navigation.prepare_pos()
            midas_generator.prepare_pos()
            midas_generator.generate_ss_reports(missing_dates_per_store)
        except Exception as e:
            print(f"Error during Midas SS report generation: {e}. Retrying...")
            try:
                midas_navigation.restart_pos()
                midas_generator.restart_pos()
                midas_generator.generate_ss_reports(missing_dates_per_store)
            except Exception as retry_e:
                print(f"Failed to generate Midas SS reports after retrying: {retry_e}")
        finally:
            midas_navigation.close_pos()
    else:
        print("No missing Midas sales summary reports for the given date range.")

def fetch_all_missing_data(view):
    store_type = view.store_type_combo.currentText()
    if store_type == "All":
        fetch_missing_midas_ss_reports(view)
        view.fetch_tech_data()
        view.fetch_timesheet_data()
        # Add other fetch calls if needed
    elif store_type == "Midas":
        fetch_missing_midas_ss_reports(view)
        view.fetch_tech_data()
        view.fetch_timesheet_data()
        # Add other fetch calls if needed
    elif store_type == "Bigo":
        view.fetch_sales_data()
        view.fetch_tech_data()
        view.fetch_timesheet_data()
        # Add other fetch calls if needed
