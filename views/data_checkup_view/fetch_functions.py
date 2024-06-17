# fetch_functions.py
from database.ss_data import get_missing_ss_dates
from database.tech_data import get_missing_midas_tech_dates, get_missing_bigo_tech_dates
from database.timesheet_data import get_missing_timesheet_dates
from config.app_settings import MIDAS_STORE_NUMBERS, BIGO_STORE_NUMBERS, MIDAS_SS_TABLE, BIGO_SS_TABLE

def fetch_all_missing_data(view):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        print("Fetching Midas Data")
        ss_midas = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
        tech_midas = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
        timesheet_midas = get_missing_timesheet_dates(start_date, end_date, 'midas_timesheet', MIDAS_STORE_NUMBERS)
        print("Midas Sales Summary:", ss_midas)
        print("Midas Tech Data:", tech_midas)
        print("Midas Timesheet Data:", timesheet_midas)

    if store_type == "All" or store_type == "Bigo":
        print("Fetching Bigo Data")
        ss_bigo = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
        tech_bigo = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
        timesheet_bigo = get_missing_timesheet_dates(start_date, end_date, 'bigo_timesheet', BIGO_STORE_NUMBERS)
        print("Bigo Sales Summary:", ss_bigo)
        print("Bigo Tech Data:", tech_bigo)
        print("Bigo Timesheet Data:", timesheet_bigo)

    print("Fetching all missing data.")

def fetch_missing_ss_data(view):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        print("Fetching Midas Sales Summary Data")
        ss_midas = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
        print("Midas Sales Summary:", ss_midas)

    if store_type == "All" or store_type == "Bigo":
        print("Fetching Bigo Sales Summary Data")
        ss_bigo = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
        print("Bigo Sales Summary:", ss_bigo)

    print("Fetching SS data.")

def fetch_missing_tech_data(view):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        print("Fetching Midas Tech Data")
        tech_midas = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
        print("Midas Tech Data:", tech_midas)

    if store_type == "All" or store_type == "Bigo":
        print("Fetching Bigo Tech Data")
        tech_bigo = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
        print("Bigo Tech Data:", tech_bigo)

    print("Fetching Tech data.")

def fetch_missing_timesheet_data(view):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        print("Fetching Midas Timesheet Data")
        timesheet_midas = get_missing_timesheet_dates(start_date, end_date, 'midas_timesheet', MIDAS_STORE_NUMBERS)
        print("Midas Timesheet Data:", timesheet_midas)

    if store_type == "All" or store_type == "Bigo":
        print("Fetching Bigo Timesheet Data")
        timesheet_bigo = get_missing_timesheet_dates(start_date, end_date, 'bigo_timesheet', BIGO_STORE_NUMBERS)
        print("Bigo Timesheet Data:", timesheet_bigo)

    print("Fetching Timesheet data.")
