from database.ss_data import get_missing_ss_dates
from database.tech_data import get_missing_midas_tech_dates, get_missing_bigo_tech_dates
from database.sales_by_category_data import get_missing_sales_by_category_dates
from config.app_settings import MIDAS_STORE_NUMBERS, BIGO_STORE_NUMBERS, MIDAS_SS_TABLE, BIGO_SS_TABLE, MIDAS_SBA_TABLE, BIGO_SBA_TABLE
from generators.helpers import generate_midas_reports, generate_bigo_reports

def fetch_all_missing_data(view, stop_requested, progress_callback):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    if store_type == "All" or store_type == "Midas":
        progress_callback("Fetching Midas Data")
        ss_midas = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
        tech_midas = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
        timesheet_midas = {store: [(start_date_str, end_date_str)] for store in MIDAS_STORE_NUMBERS}
        sales_by_category_midas = get_missing_sales_by_category_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SBA_TABLE)

        if not ss_midas and not tech_midas and not any(timesheet_midas.values()):
            progress_callback("Midas data is all up to date.")
        else:
            progress_callback(f"Midas Sales Summary: {ss_midas}")
            progress_callback(f"Midas Tech Data: {tech_midas}")
            progress_callback(f"Midas Timesheet Data: {timesheet_midas}")
            progress_callback(f"Midas Sales By Category Data: {sales_by_category_midas}")
            if stop_requested():
                progress_callback("Fetch canceled.")
                return
            generate_midas_reports(ss_midas, tech_midas, timesheet_midas, sales_by_category_midas, stop_requested, progress_callback)

    if store_type == "All" or store_type == "Bigo":
        progress_callback("Fetching Bigo Data")
        ss_bigo = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
        tech_bigo = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
        sales_by_category_bigo = get_missing_sales_by_category_dates(start_date, end_date, BIGO_STORE_NUMBERS,
                                                                     BIGO_SBA_TABLE)
        timesheet_bigo = [(start_date_str, end_date_str)]


        if not ss_bigo and not tech_bigo and not timesheet_bigo:
            progress_callback("Bigo data is all up to date.")
        else:
            progress_callback(f"Bigo Sales Summary: {ss_bigo}")
            progress_callback(f"Bigo Tech Data: {tech_bigo}")
            progress_callback(f"Bigo Timesheet Data: {timesheet_bigo}")
            if stop_requested():
                progress_callback("Fetch canceled.")
                return
            generate_bigo_reports(ss_bigo, tech_bigo, timesheet_bigo, sales_by_category_bigo, stop_requested, progress_callback)

    progress_callback("Fetching all missing data completed.")

def fetch_missing_ss_data(view, stop_requested, progress_callback):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        ss_midas = get_missing_ss_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SS_TABLE)
        if not ss_midas:
            progress_callback("Sales Summary data for Midas is up to date.")
        else:
            progress_callback(f"Fetching Midas Sales Summary: {ss_midas}")
            if stop_requested():
                progress_callback("Fetch canceled.")
                return
            generate_midas_reports(ss_midas, None, None, None, stop_requested, progress_callback)

    if store_type == "All" or store_type == "Bigo":
        ss_bigo = get_missing_ss_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SS_TABLE)
        if not ss_bigo:
            progress_callback("Sales Summary data for Bigo is up to date.")
        else:
            progress_callback(f"Fetching Bigo Sales Summary: {ss_bigo}")
            if stop_requested():
                progress_callback("Fetch canceled.")
                return
            generate_bigo_reports(ss_bigo, None, None, None, stop_requested, progress_callback)

    progress_callback("Fetching Sales Summary data completed.")

def fetch_missing_tech_data(view, stop_requested, progress_callback):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        tech_midas = get_missing_midas_tech_dates(start_date, end_date, MIDAS_STORE_NUMBERS, 'midas_tech_summary')
        if not tech_midas:
            progress_callback("Tech data for Midas is up to date.")
        else:
            progress_callback(f"Fetching Midas Tech Data: {tech_midas}")
            if stop_requested():
                progress_callback("Fetch canceled.")
                return
            generate_midas_reports(None, tech_midas, None, None, stop_requested, progress_callback)

    if store_type == "All" or store_type == "Bigo":
        tech_bigo = get_missing_bigo_tech_dates(start_date, end_date, 'bigo_tech_summary')
        if not tech_bigo:
            progress_callback("Tech data for Bigo is up to date.")
        else:
            progress_callback(f"Fetching Bigo Tech Data: {tech_bigo}")
            if stop_requested():
                progress_callback("Fetch canceled.")
                return
            generate_bigo_reports(None, tech_bigo, None, None, stop_requested, progress_callback)

    progress_callback("Fetching Tech data completed.")

def fetch_missing_timesheet_data(view, stop_requested, progress_callback):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    if store_type == "All" or store_type == "Midas":
        progress_callback("Fetching Midas Timesheet Data")
        timesheet_midas = {store: [(start_date_str, end_date_str)] for store in MIDAS_STORE_NUMBERS}
        if not any(timesheet_midas.values()):
            progress_callback("Timesheet data for Midas is up to date.")
        else:
            progress_callback(f"Midas Timesheet Data: {timesheet_midas}")
            if stop_requested():
                progress_callback("Fetch canceled.")
                return
            generate_midas_reports(None, None, timesheet_midas, None, stop_requested, progress_callback)

    if store_type == "All" or store_type == "Bigo":
        progress_callback("Fetching Bigo Timesheet Data")
        timesheet_bigo = [(start_date_str, end_date_str)]
        if not timesheet_bigo:
            progress_callback("Timesheet data for Bigo is up to date.")
        else:
            progress_callback(f"Bigo Timesheet Data: {timesheet_bigo}")
            if stop_requested():
                progress_callback("Fetch canceled.")
                return
            generate_bigo_reports(None, None, timesheet_bigo, None, stop_requested, progress_callback)

    progress_callback("Fetching Timesheet data completed.")

def fetch_missing_sales_by_category_data(view, stop_requested, progress_callback):
    store_type = view.store_type_combo.currentText()
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if store_type == "All" or store_type == "Midas":
        sba_midas = get_missing_sales_by_category_dates(start_date, end_date, MIDAS_STORE_NUMBERS, MIDAS_SBA_TABLE)
        print(sba_midas)
        if not sba_midas:
            progress_callback("Sales By Category data for Midas is up to date.")
        else:
            progress_callback(f"Fetching Midas Sales By Category Data: {sba_midas}")
            if stop_requested():
                progress_callback("Fetch canceled.")
                return
            generate_midas_reports(None, None, None, sba_midas, stop_requested, progress_callback)

    if store_type == "All" or store_type == "Bigo":
        sbc_bigo = get_missing_sales_by_category_dates(start_date, end_date, BIGO_STORE_NUMBERS, BIGO_SBA_TABLE)
        print(sbc_bigo)
        if not sbc_bigo:
            progress_callback("Sales By Category data for Bigo is up to date.")
        else:
            progress_callback(f"Fetching Bigo Sales By Category Data: {sbc_bigo}")
            if stop_requested():
                progress_callback("Fetch canceled.")
                return
            generate_bigo_reports(None, None, None, sbc_bigo, stop_requested, progress_callback)