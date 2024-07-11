from config.logging import logger
from config.app_settings import OUTPUTS
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.timings import wait_until_passes
from contextlib import contextmanager


class ReportActionError(Exception):
    """Custom exception for report action errors."""
    pass


class ReportActions:
    def __init__(self):
        self.config = None
        self.output_file = OUTPUTS
        self.app = None

    @contextmanager
    def error_handling(self):
        try:
            yield
        except ElementNotFoundError as e:
            logger.error(f"Element not found: {e}")
            raise ReportActionError(f"Element not found: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise ReportActionError(f"Unexpected error: {e}")

    def perform_action_with_retry(self, action, retries=3, timeout=10, retry_interval=1):
        def _retry():
            return wait_until_passes(timeout, retry_interval, action)

        for attempt in range(retries):
            try:
                with self.error_handling():
                    return _retry()
            except ReportActionError as e:
                if attempt == retries - 1:
                    logger.error(f"Action failed after {retries} attempts: {e}")
                    raise
                logger.warning(f"Action failed (attempt {attempt + 1}/{retries}): {e}")

    def select_ss_report(self):
        logger.info("Selecting SS report")
        raise NotImplementedError("This method should be implemented by subclasses.")

    def enter_date_range(self, start_date, end_date):
        logger.info(f"Entering date range: {start_date} to {end_date}")
        raise NotImplementedError("This method should be implemented by subclasses.")

    def select_generate_report(self):
        logger.info("Selecting generate report")
        raise NotImplementedError("This method should be implemented by subclasses.")

    def enter_filename(self, file_name):
        logger.info(f"Entering filename: {file_name}")
        raise NotImplementedError("This method should be implemented by subclasses.")

    def enter_file_destination(self):
        logger.info("Entering file destination")
        raise NotImplementedError("This method should be implemented by subclasses.")

    def save_file(self):
        logger.info("Saving file")
        raise NotImplementedError("This method should be implemented by subclasses.")

    def check_existing_file(self):
        logger.info("Checking for existing file")
        raise NotImplementedError("This method should be implemented by subclasses.")

    def wait_for_report_to_compile(self):
        logger.info("Waiting for report to compile")
        raise NotImplementedError("This method should be implemented by subclasses.")

    def cleanup_and_close(self):
        logger.info("Cleaning up and closing")
        raise NotImplementedError("This method should be implemented by subclasses.")