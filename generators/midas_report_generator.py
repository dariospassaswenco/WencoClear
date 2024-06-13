from datetime import datetime, timedelta
from pywinauto.application import Application
from generators.base_report_generator import ReportGenerator
from navigation.ro_report_navigation import MidasReportActions
from config.pos_config import midas_config
from config.app_settings import MIDAS_STORE_NUMBERS, MIDAS_FILENAME_PATTERN

class MidasReportGenerator(ReportGenerator):
    def __init__(self):
        super().__init__()
        self.config = midas_config
        self.stores = MIDAS_STORE_NUMBERS
        self.app = None
        self.actions = None

    def prepare_pos(self):
        self.app = Application(backend="uia").connect(title=self.config["reporting_window_title"])
        self.actions = MidasReportActions(self.app, self.config)

    def restart_pos(self):
        # Close the POS application and restart it
        self.app.kill()
        self.prepare_pos()

    def generate_ss_reports(self, missing_dates_per_store, retry=False):
        try:
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
                self.extractor.extract_reports() # Extract the files for that store along the way
            self.actions.return_to_main_menu()
        except Exception as e:
            if not retry:
                print(f"Error generating SS reports: {e}. Retrying...")
                self.restart_pos()
                self.generate_ss_reports(missing_dates_per_store, retry=True)
            else:
                print(f"Failed to generate SS reports after retrying: {e}")

    def generate_timesheet_reports(self, missing_weeks_per_store):
        self.actions.select_other_reports_menu()
        self.actions.select_initial_store()
        for store_number, weeks in missing_weeks_per_store.items():
            self.actions.select_current_store(store_number)
            for start_date_str, end_date_str in weeks:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                start_date = end_date - timedelta(days=14)  # Adjust start date to be 14 days prior to end date
                file_name = MIDAS_FILENAME_PATTERN.format(store_number=store_number, report_type='ts',date=end_date_str)
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
            self.extractor.extract_reports() # Extract the files for that store along the way # Extract the files for that store along the way



    def generate_tech_reports(self, missing_weeks):
        self.actions.select_sales_reports_menu()
        self.actions.select_initial_store()
        for store_name, store_number in self.stores.items():
            self.actions.select_current_store(store_number)
            for date_range in missing_weeks:  # Assuming missing_weeks is a list of tuples (start_date_str, end_date_str)
                start_date_str, end_date_str = date_range  # Unpack the tuple
                file_name = MIDAS_FILENAME_PATTERN.format(store_number=store_number, report_type='tech', date=end_date_str)
                pos_formatted_start_date = datetime.strptime(start_date_str, '%Y-%m-%d').strftime('%m%d%Y')
                pos_formatted_end_date = datetime.strptime(end_date_str, '%Y-%m-%d').strftime('%m%d%Y')
                self.actions.enter_date_range(pos_formatted_start_date, pos_formatted_end_date)
                self.actions.tech_select_tech_report()
                self.actions.wait_for_report_to_compile()
                self.actions.select_generate_report()
                self.actions.enter_filename(file_name)
                self.actions.enter_file_destination()
                self.actions.cleanup_and_close()
            self.extractor.extract_reports()  # Extract the files for that store along the way
        self.actions.return_to_main_menu()