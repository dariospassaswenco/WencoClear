from database.ss_data import get_missing_ss_dates
from database.tech_data import get_missing_midas_tech_dates, get_missing_bigo_tech_dates
from config.app_settings import MIDAS_STORE_NUMBERS, BIGO_STORE_NUMBERS, MIDAS_SS_TABLE, BIGO_SS_TABLE
from generators.helpers import generate_midas_reports, generate_bigo_reports

def fetch_all_missing_data(view):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    if store_type == "All" or store_type == "Midas":
        print("Fetching Midas Data")
        ss_midas = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
        tech_midas = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
        timesheet_midas = {store: [(start_date_str, end_date_str)] for store in MIDAS_STORE_NUMBERS}
        print(f"Midas Sales Summary: {ss_midas}")
        print(f"Midas Tech Data: {tech_midas}")
        print(f"Midas Timesheet Data: {timesheet_midas}")
        generate_midas_reports(ss_midas, tech_midas, timesheet_midas)

    if store_type == "All" or store_type == "Bigo":
        print("Fetching Bigo Data")
        ss_bigo = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
        tech_bigo = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
        timesheet_bigo = [(start_date_str, end_date_str)]
        print(f"Bigo Sales Summary: {ss_bigo}")
        print(f"Bigo Tech Data: {tech_bigo}")
        print(f"Bigo Timesheet Data: {timesheet_bigo}")
        generate_bigo_reports(ss_bigo, tech_bigo, timesheet_bigo)

    print("Fetching all missing data completed.")

def fetch_missing_ss_data(view):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        ss_midas = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
        generate_midas_reports(ss_midas, None, None)
        print("Midas Sales Summary:", ss_midas)

    if store_type == "All" or store_type == "Bigo":
        ss_bigo = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
        generate_bigo_reports(ss_bigo, None, None)
        print("Bigo Sales Summary:", ss_bigo)

    print("Fetching Sales Summary data completed.")

def fetch_missing_tech_data(view):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        tech_midas = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
        generate_midas_reports(None, tech_midas, None)
        print("Midas Tech Data:", tech_midas)

    if store_type == "All" or store_type == "Bigo":
        tech_bigo = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
        generate_bigo_reports(None, tech_bigo, None)
        print("Bigo Tech Data:", tech_bigo)

    print("Fetching Tech data completed.")

def fetch_missing_timesheet_data(view):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    if store_type == "All" or store_type == "Midas":
        print("Fetching Midas Timesheet Data")
        timesheet_midas = {store: [(start_date_str, end_date_str)] for store in MIDAS_STORE_NUMBERS}
        generate_midas_reports(None, None, timesheet_midas)
        print("Midas Timesheet Data:", timesheet_midas)

    if store_type == "All" or store_type == "Bigo":
        print("Fetching Bigo Timesheet Data")
        timesheet_bigo = [(start_date_str, end_date_str)]
        generate_bigo_reports(None, None, timesheet_bigo)
        print("Bigo Timesheet Data:", timesheet_bigo)

    print("Fetching Timesheet data completed.")
