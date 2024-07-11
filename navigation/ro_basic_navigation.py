from .base_basic_navigation import BasicNavigation, ReportActionError
from config.pos_config import midas_config
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto import Desktop
from pywinauto.timings import wait_until_passes
from config.logging import logger
import psutil

class MidasNavigation(BasicNavigation):
    def __init__(self):
        super().__init__()
        self.set_attributes()

    def set_attributes(self):
        self.config = midas_config
        self.pos_name = self.config["pos_name"]
        self.executable_path = self.config["executable"]
        self.working_directory = self.config["working_directory"]
        self.running_program_title = self.config["running_program_title"]
        self.main_window_title = self.config["main_window_title"]

    def prepare_pos(self):
        super().prepare_pos()
        self.handle_pop_up()
        self.open_reporting_window()
        self.check_store_specific_window()

    def handle_pop_up(self):
        def action():
            logger.info("Handling Midas-specific pop-ups...")
            desktop = Desktop(backend="uia")
            popup_window = desktop.window(title="R.O. Writer Central Service")
            if popup_window.exists():
                ok_button = popup_window.child_window(title="OK", control_type="Button")
                ok_button.click_input()
                logger.info("Pop-up handled successfully")
            else:
                logger.info("Pop-up window not found.")

        self.perform_action_with_retry(action)

    def open_reporting_window(self):
        def action():
            app = Application(backend="uia").connect(title_re="Point of Sale - R\.O\. Writer.*")
            ro_window = app.window(title_re="Point of Sale - R\.O\. Writer.*")
            logger.info("Successfully connected to RO Writer window")
            ro_window.set_focus()
            reporting_button = ro_window.child_window(auto_id="itemImage", control_type='Image', found_index=8)
            reporting_button.click_input()
            logger.info("Reporting window opened")

        try:
            self.perform_action_with_retry(action)
        except ReportActionError:
            logger.error("Failed to open reporting window. Make sure R.O Writer is open and focused.")
            raise

    def check_store_specific_window(self):
        def action():
            app = Application(backend='uia').connect(title='Reporting - R.O. Writer')
            reporting_window = app.window(title="Reporting - R.O. Writer")
            store_specific_window = reporting_window.child_window(title="Close Store Specific Windows",
                                                                  control_type="Window")
            if store_specific_window.exists():
                ok_button = store_specific_window.child_window(title="OK", auto_id="1", control_type="Button")
                ok_button.click_input()
                logger.info("Store Specific Pop-up closed")
            else:
                logger.info("Store Specific Pop-up window not found.")

        self.perform_action_with_retry(action)

    def close_pos(self):
        def action():
            closed = False
            for process in psutil.process_iter(attrs=['pid', 'name']):
                if "rowriter" in process.info['name']:
                    try:
                        process_obj = psutil.Process(process.info['pid'])
                        process_obj.terminate()
                        process_obj.wait(timeout=5)
                        closed = True
                        logger.info(f"{self.pos_name} closed")
                    except psutil.NoSuchProcess:
                        logger.warning(f"Process {self.pos_name} not found during close")
                    except Exception as e:
                        logger.error(f"Error closing {self.pos_name}: {e}")
                        raise
            if not closed:
                logger.warning(f"No {self.pos_name} processes found to close")

        self.perform_action_with_retry(action)

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