from .base_basic_navigation import BasicNavigation, ReportActionError
from config.pos_config import bigo_config
from pywinauto.application import Application
from pywinauto.keyboard import SendKeys
from pywinauto.timings import wait_until_passes
from config.logging import logger
import time
import psutil

class BigoNavigation(BasicNavigation):
    def __init__(self):
        super().__init__()
        self.set_attributes()

    def set_attributes(self):
        self.config = bigo_config
        self.pos_name = self.config["pos_name"]
        self.executable_path = self.config["executable"]
        self.working_directory = self.config["working_directory"]
        self.running_program_title = self.config["running_program_title"]
        self.main_window_title = self.config["main_window_title"]

    def prepare_pos(self):
        super().prepare_pos()
        self.login()
        self.activant_window()
        self.select_corporate_reports()
        self.security_login()

    def login(self):
        def action():
            app = Application(backend='uia').connect(title='Solera/DST - Big O Home Office 9.5_STD_BGO')
            window = app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            window.set_focus()

            user_id = window.child_window(title="cbouserid", control_type="ComboBox")
            user_id.click_input()
            wait_until_passes(10, 1, lambda: user_id.is_enabled())
            user_id.type_keys(self.config["username"])
            SendKeys("{ENTER}")
            wait_until_passes(10, 1, lambda: window.is_enabled())

            password_edit = window.child_window(title="txtPassword", control_type="Edit")
            password_edit.click_input()
            password_edit.type_keys(self.config["password"])
            SendKeys("{ENTER}")
            logger.info("Credentials Entered")

        self.perform_action_with_retry(action)

    def activant_window(self):
        def action():
            app = Application(backend='uia').connect(title='Solera/DST - Big O Home Office 9.5_STD_BGO')
            window = app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            activant = window.child_window(title="ACTIVANT Catalog Error", control_type="Window")
            activant.child_window(title="OK", auto_id="2", control_type="Button").click_input()
            logger.info("Activant Window Closed")

        self.perform_action_with_retry(action)

    def select_corporate_reports(self):
        def action():
            app = Application(backend='uia').connect(title='Solera/DST - Big O Home Office 9.5_STD_BGO')
            window = app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            window.set_focus()
            wait_until_passes(10, 1, lambda: window.is_enabled())
            SendKeys("%a")
            SendKeys("{ENTER}")
            administration = window.child_window(title="Administration", control_type="Menu")
            corporate_reports = administration.child_window(title="Corporate Reports", control_type="MenuItem")
            corporate_reports.click_input()
            logger.info("Corporate Reports selected")

        self.perform_action_with_retry(action)

    def security_login(self):
        def action():
            app = Application(backend='uia').connect(title='Solera/DST - Big O Home Office 9.5_STD_BGO')
            window = app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            security_login = window.child_window(title="Security Login", control_type="Window")

            user_id = security_login.child_window(title="txtUserid", control_type="Edit")
            user_id.type_keys(self.config["username"])
            SendKeys("{ENTER}")
            wait_until_passes(10, 1, lambda: window.is_enabled())

            password_input = security_login.child_window(title="txtPassword", control_type="Edit")
            password_input.type_keys(self.config["password"])
            SendKeys("{ENTER}")
            logger.info("Security login completed")

        self.perform_action_with_retry(action)

    def close_pos(self):
        def action():
            for process in psutil.process_iter(attrs=['pid', 'name']):
                if "homoff.exe" in process.info['name']:
                    try:
                        process_obj = psutil.Process(process.info['pid'])
                        process_obj.terminate()
                        process_obj.wait(timeout=5)
                        logger.info(f"{self.pos_name} closed")
                    except psutil.NoSuchProcess:
                        logger.warning(f"Process {self.pos_name} not found during close")
                    except Exception as e:
                        logger.error(f"Error closing {self.pos_name}: {e}")
                        raise

        self.perform_action_with_retry(action)