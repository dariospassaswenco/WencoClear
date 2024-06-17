from config.app_settings import (
    OUTPUTS,
)
from pywinauto.findwindows import ElementNotFoundError
import time

class ReportActions():
    def __init__(self):
        self.config = None
        self.output_file = OUTPUTS
        self.app = None

    def perform_action_with_retry(self, action, retries=3, delay=2):
        for attempt in range(retries):
            try:
                action()
                return
            except Exception as e:
                print(f"Error performing action: {e}. Retrying ({attempt + 1}/{retries})...")
                time.sleep(delay)
        print("Failed to perform action after multiple retries.")

    def select_ss_report(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def enter_date_range(self, start_date, end_date):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def select_generate_report(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def enter_filename(self, file_name):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def enter_file_destination(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def save_file(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def check_existing_file(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def wait_for_report_to_compile(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def cleanup_and_close(self, date):
        raise NotImplementedError("This method should be implemented by subclasses.")




