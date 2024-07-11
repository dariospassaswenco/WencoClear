import time
import psutil
import subprocess
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.timings import wait_until_passes
import os
from config.logging import logger
from .base_reports_navigation import ReportActionError

class BasicNavigation:
    def __init__(self):
        self.config = None
        self.pos_name = None
        self.working_directory = None
        self.executable_path = None
        self.running_program_title = None
        self.main_window_title = None
        self.backend = 'uia'

    def set_attributes(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def prepare_pos(self):
        self.set_attributes()
        logger.info(f"Preparing {self.pos_name} for automation")
        self.cleanup()
        self.launch_pos()
        self.wait_for_pos_to_launch()

    def cleanup(self):
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if self.running_program_title in process.info['name']:
                try:
                    process_obj = psutil.Process(process.info['pid'])
                    process_obj.terminate()
                    process_obj.wait(timeout=2)
                    logger.info(f"Terminated existing {self.pos_name} process")
                except psutil.NoSuchProcess:
                    logger.warning(f"Process {self.running_program_title} not found during cleanup")
                except Exception as e:
                    logger.error(f"Error during cleanup: {e}")

    def launch_pos(self):
        try:
            os.chdir(self.working_directory)
            subprocess.Popen([self.executable_path])
            logger.info(f"Launching {self.pos_name}")
        except FileNotFoundError:
            logger.error(f"{self.pos_name} executable not found. Please provide a valid path.")
            raise ReportActionError(f"{self.pos_name} executable not found")
        except Exception as e:
            logger.error(f"Error launching {self.pos_name}: {e}")
            raise ReportActionError(f"Error launching {self.pos_name}")

    def wait_for_pos_to_launch(self):
        def check_window():
            app = Application(backend="uia").connect(title_re=self.main_window_title)
            window = app.window(title_re=self.main_window_title)
            if not window.exists():
                raise ElementNotFoundError
            return window

        try:
            window = wait_until_passes(timeout=60, retry_interval=1, func=check_window)
            logger.info(f"{self.pos_name} window is ready.")
            return window
        except TimeoutError:
            logger.error(f"{self.pos_name} window not found within the timeout period.")
            raise ReportActionError(f"{self.pos_name} failed to launch")

    def close_pos(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def perform_action_with_retry(self, action, retries=3, delay=2):
        for attempt in range(retries):
            try:
                return action()
            except Exception as e:
                logger.warning(f"Error performing action: {e}. Attempt {attempt + 1} of {retries}")
                if attempt == retries - 1:
                    logger.error(f"Action failed after {retries} attempts")
                    raise ReportActionError(f"Action failed after {retries} attempts: {e}")
                time.sleep(delay)