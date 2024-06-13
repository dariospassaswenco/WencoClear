from datetime import datetime, timedelta
from pywinauto.application import Application
from .base_report_generator import ReportGenerator
from navigation.navex_report_navigation import BigoReportActions
from config.pos_config import bigo_config
from config.app_settings import BIGO_STORE_NUMBERS
from config.app_settings import BIGO_FILENAME_PATTERN

class BigoReportGenerator(ReportGenerator):
    def __init__(self):
        super().__init__()
        self.config = bigo_config
        self.stores = BIGO_STORE_NUMBERS
        self.app = Application(backend="uia").connect(title=self.config["reporting_window_title"])
        self.actions = BigoReportActions(self.app, self.config)

    def generate_ss_reports(self, missing_dates_per_store):
        self.actions.select_report(self.config["ss_report_title"])
        for store_number, missing_dates in missing_dates_per_store.items():
            self.actions.select_current_store(store_number)
            for date in missing_dates:
                formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%m%d%Y')
                file_name = BIGO_FILENAME_PATTERN.format(store_number=store_number, report_type='ss', date=date)
                self.actions.enter_date_range(formatted_date, formatted_date)
                self.actions.select_generate_report()  # Clicking Excel button
                self.actions.enter_file_destination()
                self.actions.enter_filename(file_name)
                self.actions.save_file()
                self.actions.wait_for_report_to_compile()
                self.actions.cleanup_and_close(date)
            self.extractor.extract_reports()  # Extract the files for that store along the way

    def generate_timesheet_reports(self, missing_weeks_per_store):
        unique_weeks = set()
        for weeks in missing_weeks_per_store.values():
            unique_weeks.update(weeks)
        end_dates = [datetime.strptime(pair[1], '%Y-%m-%d') for pair in unique_weeks]
        self.actions.select_report(self.config["timesheet_report_title"])
        for end_date in end_dates:
            end_date_str = end_date.strftime('%Y-%m-%d')
            start_date = end_date - timedelta(days=7)
            file_name = BIGO_FILENAME_PATTERN.format(store_number='TS', report_type='ts', date=end_date_str)
            pos_formatted_start_date = start_date.strftime('%m%d%Y')
            pos_formatted_end_date = end_date.strftime('%m%d%Y')
            self.actions.enter_date_range(pos_formatted_start_date, pos_formatted_end_date)
            self.actions.select_generate_report() # Click excel button
            self.actions.enter_file_destination()
            self.actions.enter_filename(file_name)
            self.actions.save_file()
            self.actions.ts_select_employees()
            self.actions.wait_for_report_to_compile()
            self.actions.cleanup_and_close(end_date_str)
        self.extractor.extract_reports()

    def generate_tech_reports(self, missing_weeks):
        self.actions.select_report(self.config["tech_report_title"])
        for date_range in missing_weeks:
            start_date_str, end_date_str = date_range
            file_name = BIGO_FILENAME_PATTERN.format(store_number="TECH", report_type='tech', date=end_date_str)
            pos_formatted_start_date = datetime.strptime(start_date_str, '%Y-%m-%d').strftime('%m%d%Y')
            pos_formatted_end_date = datetime.strptime(end_date_str, '%Y-%m-%d').strftime('%m%d%Y')
            self.actions.enter_date_range(pos_formatted_start_date, pos_formatted_end_date)
            self.actions.select_generate_report() # Click excel button
            self.actions.enter_file_destination()
            self.actions.enter_filename(file_name)
            self.actions.save_file()
            self.actions.ts_select_employees()
            self.actions.wait_for_report_to_compile()
            self.actions.cleanup_and_close(end_date_str)
        self.extractor.extract_reports()



