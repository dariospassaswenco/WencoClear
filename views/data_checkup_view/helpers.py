# views/data_checkup_views/helpers
import traceback
from config.app_settings import MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE, BIGO_STORE_NUMBERS, BIGO_SS_TABLE, CLOSED_DAYS
from database.ss_data import get_missing_ss_dates
from database.tech_data import get_missing_midas_tech_dates, get_missing_bigo_tech_dates
from database.timesheet_data import get_missing_timesheet_dates
from .display_functions import display_sales_summary_data, display_tech_data, display_timesheet_data, display_all_data, combine_all_results

def run_data_checkup(view, report_type):
    try:
        store_type = view.store_type_combo.currentText()
        start_date = view.start_date_edit.date().toPyDate()
        end_date = view.end_date_edit.date().toPyDate()

        if report_type == "Sales Summary":
            if store_type == "All":
                midas_results = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
                bigo_results = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
                combined_results = {**midas_results, **bigo_results}
                display_sales_summary_data(view, combined_results, start_date, end_date, view.sales_summary_results_table)
            elif store_type == "Midas":
                results = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
                display_sales_summary_data(view, results, start_date, end_date, view.sales_summary_results_table)
            elif store_type == "Bigo":
                results = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
                display_sales_summary_data(view, results, start_date, end_date, view.sales_summary_results_table)

        elif report_type == "Tech Data":
            if store_type == "All":
                midas_results = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
                bigo_results = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
                combined_tech_results = {"Midas": midas_results, "Bigo": bigo_results}
                display_tech_data(view, combined_tech_results, start_date, end_date, view.tech_results_table)
            elif store_type == "Midas":
                tech_results = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
                display_tech_data(view, {"Midas": tech_results}, start_date, end_date, view.tech_results_table)
            elif store_type == "Bigo":
                tech_results = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
                display_tech_data(view, {"Bigo": tech_results}, start_date, end_date, view.tech_results_table)

        elif report_type == "Timesheet Data":
            if store_type == "All":
                midas_results = get_missing_timesheet_dates(start_date, end_date, 'midas_timesheet', MIDAS_STORE_NUMBERS)
                bigo_results = get_missing_timesheet_dates(start_date, end_date, 'bigo_timesheet', BIGO_STORE_NUMBERS)
                combined_results = {**midas_results, **bigo_results}
                display_timesheet_data(view, combined_results, start_date, end_date, view.timesheet_results_table)
            elif store_type == "Midas":
                results = get_missing_timesheet_dates(start_date, end_date, 'midas_timesheet', MIDAS_STORE_NUMBERS)
                display_timesheet_data(view, results, start_date, end_date, view.timesheet_results_table)
            elif store_type == "Bigo":
                results = get_missing_timesheet_dates(start_date, end_date, 'bigo_timesheet', BIGO_STORE_NUMBERS)
                display_timesheet_data(view, results, start_date, end_date, view.timesheet_results_table)

        elif report_type == "All Reports":
            if store_type == "All":
                midas_ss = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
                bigo_ss = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
                midas_tech = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
                bigo_tech = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
                midas_timesheet = get_missing_timesheet_dates(start_date, end_date, 'midas_timesheet', MIDAS_STORE_NUMBERS)
                bigo_timesheet = get_missing_timesheet_dates(start_date, end_date, 'bigo_timesheet', BIGO_STORE_NUMBERS)

                combined_results = combine_all_results(midas_ss, bigo_ss, midas_tech, bigo_tech, midas_timesheet, bigo_timesheet, start_date, end_date)
                display_all_data(view, combined_results, start_date, end_date, view.all_reports_results_table)
            elif store_type == "Midas":
                ss_results = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
                tech_results = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
                timesheet_results = get_missing_timesheet_dates(start_date, end_date, 'midas_timesheet', MIDAS_STORE_NUMBERS)

                combined_results = combine_all_results(ss_results, {}, tech_results, {}, timesheet_results, {}, start_date, end_date)
                display_all_data(view, combined_results, start_date, end_date, view.all_reports_results_table)
            elif store_type == "Bigo":
                ss_results = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
                tech_results = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
                timesheet_results = get_missing_timesheet_dates(start_date, end_date, 'bigo_timesheet', BIGO_STORE_NUMBERS)

                combined_results = combine_all_results({}, ss_results, {}, tech_results, {}, timesheet_results, start_date, end_date)
                display_all_data(view, combined_results, start_date, end_date, view.all_reports_results_table)
    except Exception as e:
        print(f"Error in run_data_checkup: {e}")
        traceback.print_exc()
