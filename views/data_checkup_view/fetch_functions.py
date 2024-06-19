from database.ss_data import get_missing_ss_dates
from database.tech_data import get_missing_midas_tech_dates, get_missing_bigo_tech_dates
from database.timesheet_data import get_missing_timesheet_dates
from config.app_settings import MIDAS_STORE_NUMBERS, BIGO_STORE_NUMBERS, MIDAS_SS_TABLE, BIGO_SS_TABLE
from generators.helpers import generate_midas_reports, generate_bigo_reports

def fetch_all_missing_data(view, progress_dialog):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    progress_dialog.setMaximum(6)  # Set based on the number of operations
    current_step = 0

    if store_type == "All" or store_type == "Midas":
        progress_dialog.log_message("Fetching Midas Data")
        ss_midas = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
        tech_midas = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
        timesheet_midas = get_missing_timesheet_dates(start_date, end_date, 'midas_timesheet', MIDAS_STORE_NUMBERS)
        progress_dialog.log_message(f"Midas Sales Summary: {ss_midas}")
        progress_dialog.log_message(f"Midas Tech Data: {tech_midas}")
        progress_dialog.log_message(f"Midas Timesheet Data: {timesheet_midas}")
        progress_dialog.setValue(current_step)
        generate_midas_reports(ss_midas, tech_midas, timesheet_midas, progress_dialog)

    if store_type == "All" or store_type == "Bigo":
        progress_dialog.log_message("Fetching Bigo Data")
        ss_bigo = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
        tech_bigo = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
        timesheet_bigo = get_missing_timesheet_dates(start_date, end_date, 'bigo_timesheet', BIGO_STORE_NUMBERS)
        progress_dialog.log_message(f"Bigo Sales Summary: {ss_bigo}")
        progress_dialog.log_message(f"Bigo Tech Data: {tech_bigo}")
        progress_dialog.log_message(f"Bigo Timesheet Data: {timesheet_bigo}")
        progress_dialog.setValue(current_step + 3)
        generate_bigo_reports(ss_bigo, tech_bigo, timesheet_bigo, progress_dialog)

    progress_dialog.log_message("Fetching all missing data.")

def fetch_missing_ss_data(view, progress_dialog):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        progress_dialog.log_message("Fetching Midas Data")
        ss_midas = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
        generate_midas_reports(ss_midas, None, None, progress_dialog)
        print("Midas Sales Summary:", ss_midas)

    if store_type == "All" or store_type == "Bigo":
        progress_dialog.log_message("Fetching Bigo Data")
        ss_bigo = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
        generate_bigo_reports(ss_bigo, None, None, progress_dialog)
        print("Bigo Sales Summary:", ss_bigo)

    print("Fetching SS data.")

def fetch_missing_tech_data(view, progress_dialog):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        progress_dialog.log_message("Fetching Midas Tech Data")
        tech_midas = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
        generate_midas_reports(None, tech_midas, None, progress_dialog)
        print("Midas Tech Data:", tech_midas)

    if store_type == "All" or store_type == "Bigo":
        progress_dialog.log_message("Fetching Bigo Tech Data")
        tech_bigo = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
        generate_bigo_reports(None, tech_bigo, None, progress_dialog)
        print("Bigo Tech Data:", tech_bigo)

    print("Fetching Tech data.")

def fetch_missing_timesheet_data(view, progress_dialog):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        progress_dialog.log_message("Fetching Midas Timesheet Data")
        timesheet_midas = get_missing_timesheet_dates(start_date, end_date, 'midas_timesheet', MIDAS_STORE_NUMBERS)
        generate_midas_reports(None, None, timesheet_midas, progress_dialog)
        print("Midas Timesheet Data:", timesheet_midas)

    if store_type == "All" or store_type == "Bigo":
        progress_dialog.log_message("Fetching Bigo Timesheet Data")
        timesheet_bigo = get_missing_timesheet_dates(start_date, end_date, 'bigo_timesheet', BIGO_STORE_NUMBERS)
        generate_bigo_reports(None, None, timesheet_bigo, progress_dialog)
        print("Bigo Timesheet Data:", timesheet_bigo)

    print("Fetching Timesheet data.")
