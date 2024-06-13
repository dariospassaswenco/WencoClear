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

    def perform_action_with_retry(self, action, action_args=(), max_attempts=3, retry_interval=2):
        attempts = 0
        while attempts < max_attempts:
            try:
                action(*action_args)
                print(f"{action.__name__} succeeded.")
                return True
            except ElementNotFoundError as e:
                print(f"Attempt {attempts + 1}: {action.__name__} failed with error: {e}. Retrying...")
                time.sleep(retry_interval)
                attempts += 1
        print(f"Action {action.__name__} failed after {max_attempts} attempts.")
        return False

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




