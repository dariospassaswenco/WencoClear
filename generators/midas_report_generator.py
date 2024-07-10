from datetime import datetime, timedelta
from pywinauto.application import Application
from generators.base_report_generator import ReportGenerator
from navigation.ro_report_navigation import MidasReportActions
from navigation.ro_basic_navigation import MidasNavigation
from config.pos_config import midas_config
from config.app_settings import *
from database.ss_data import get_missing_ss_dates
from database.tech_data import get_missing_midas_tech_dates
from database.timesheet_data import delete_midas_timesheet_entries

class MidasReportGenerator(ReportGenerator):
    def __init__(self):
        super().__init__()
        self.config = midas_config
        self.stores = MIDAS_STORE_NUMBERS
        self.app = None
        self.actions = None

    def prepare_pos(self):
        navigation = MidasNavigation()
        navigation.prepare_pos()
        self.app = Application(backend="uia").connect(title=self.config["reporting_window_title"])
        self.actions = MidasReportActions(self.app, self.config)

    def restart_pos(self):
        navigation = MidasNavigation()
        navigation.close_pos()
        self.prepare_pos()

    def generate_ss_reports(self, missing_dates_per_store):
        self.actions.select_sales_reports_menu()
        self.actions.select_initial_store()
        for store_number, missing_dates in missing_dates_per_store.items():
            self.actions.select_current_store(store_number)
            for date in missing_dates:
                formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%m%d%Y')
                file_name = MIDAS_FILENAME_PATTERN.format(store_number=store_number, report_type='ss', date=date)
                self.actions.enter_date_range(formatted_date, formatted_date)
                self.actions.ss_select_ss_report()
                self.actions.wait_for_report_to_compile()
                self.actions.select_generate_report()
                self.actions.enter_filename(file_name)
                self.actions.enter_file_destination()
                self.actions.cleanup_and_close()
            self.extractor.extract_reports()  # Extract the files for that store along the way
        self.actions.return_to_main_menu()


    def generate_timesheet_reports(self, missing_dates_per_store):
        self.actions.select_initial_store()
        self.actions.select_other_reports_menu()
        self.actions.enter_password()
        for store_number, missing_dates in missing_dates_per_store.items():
            self.actions.select_current_store(store_number)
            for start_date_str, end_date_str in missing_dates:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                file_name = MIDAS_FILENAME_PATTERN.format(store_number=store_number, report_type='ts', date=end_date_str)
                pos_formatted_start_date = start_date.strftime('%m%d%Y')
                pos_formatted_end_date = end_date.strftime('%m%d%Y')
                self.actions.enter_date_range(pos_formatted_start_date, pos_formatted_end_date)
                self.actions.ts_select_timesheet_report()
                self.actions.ts_select_employees()
                self.actions.wait_for_report_to_compile()
                self.actions.select_generate_report()
                self.actions.enter_filename(file_name)
                self.actions.enter_file_destination()
                self.actions.cleanup_and_close()
                delete_midas_timesheet_entries(store_number, start_date_str, end_date_str)
            self.extractor.extract_reports()


    def generate_tech_reports(self, missing_dates_per_store):
        self.actions.select_sales_reports_menu()
        self.actions.select_initial_store()
        for store_number, missing_dates in missing_dates_per_store.items():
            self.actions.select_current_store(store_number)
            for date_str in missing_dates:
                start_date = datetime.strptime(date_str, '%Y-%m-%d')
                end_date = datetime.strptime(date_str, '%Y-%m-%d')
                file_name = MIDAS_FILENAME_PATTERN.format(store_number=store_number, report_type='tech', date=date_str)
                pos_formatted_start_date = start_date.strftime('%m%d%Y')
                pos_formatted_end_date = end_date.strftime('%m%d%Y')
                self.actions.enter_date_range(pos_formatted_start_date, pos_formatted_end_date)
                self.actions.tech_select_tech_report()
                self.actions.wait_for_report_to_compile()
                self.actions.select_generate_report()
                self.actions.enter_filename(file_name)
                self.actions.enter_file_destination()
                self.actions.cleanup_and_close()
            self.extractor.extract_reports()
        self.actions.return_to_main_menu()

    def generate_sales_by_category_reports(self, missing_dates_per_store):
        self.actions.select_sales_reports_menu()
        self.actions.sba_find_report_in_list()
        self.actions.select_initial_store()
        for store_number, missing_dates in missing_dates_per_store.items():
            self.actions.select_current_store(store_number)
            for date in missing_dates:
                formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%m%d%Y')
                file_name = MIDAS_FILENAME_PATTERN.format(store_number=store_number, report_type='sba', date=date)
                self.actions.enter_date_range(formatted_date, formatted_date)
                self.actions.sba_select_sba_report()
                self.actions.wait_for_report_to_compile()
                self.actions.select_generate_report()
                self.actions.enter_filename(file_name)
                self.actions.enter_file_destination()
                self.actions.cleanup_and_close()
            self.extractor.extract_reports()  # Extract the files for that store along the way
        self.actions.return_to_main_menu()