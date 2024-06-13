from .base_basic_navigation import BasicNavigation
from config.pos_config import bigo_config
# from config.app_settings import RO_WORKING_DIRECTORY, NAVEX_WORKING_DIRECTORY
from pywinauto.application import Application
from pywinauto.keyboard import SendKeys
import time
import psutil

class BigoNavigation(BasicNavigation):
    def __init__(self):
        super().__init__()
        self.set_attributes()

    def set_attributes(self):
        self.config = bigo_config
        self.pos_name = self.config["pos_name"]
        self.working_directory = NAVEX_WORKING_DIRECTORY
        self.executable_path = self.config["executable"]
        self.running_program_title = self.config["running_program_title"]
        self.main_window_title = self.config["main_window_title"]

    def prepare_pos(self):
        super().prepare_pos()
        self.login()
        self.activant_window()
        self.select_corporate_reports()
        self.security_login()


    def login(self):
        app = Application(backend='uia').connect(title='Solera/DST - Big O Home Office 9.5_STD_BGO')
        window = app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
        window.set_focus()

        user_id = window.child_window(title="cbouserid", control_type="ComboBox")
        user_id.click_input()
        time.sleep(5)
        user_id.type_keys(self.config["username"])
        SendKeys("{ENTER}")
        time.sleep(2)

        password_edit = window.child_window(title="txtPassword", control_type="Edit")
        password_edit.click_input()
        password_edit.type_keys(self.config["password"])
        SendKeys("{ENTER}")
        print("Credentials Entered")

    def activant_window(self):
        app = Application(backend='uia').connect(title='Solera/DST - Big O Home Office 9.5_STD_BGO')
        window = app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
        activant = window.child_window(title="ACTIVANT Catalog Error", control_type="Window")
        activant.child_window(title="OK", auto_id="2", control_type="Button").click_input()
        print("Activant Window Closed")

    def select_corporate_reports(self):
        app = Application(backend='uia').connect(title='Solera/DST - Big O Home Office 9.5_STD_BGO')
        window = app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
        window.set_focus()
        time.sleep(1)
        SendKeys("%a")
        SendKeys("{ENTER}")
        administration = window.child_window(title="Administration", control_type="Menu")
        corporate_reports = administration.child_window(title="Corporate Reports", control_type="MenuItem")
        corporate_reports.click_input()

    def security_login(self):
        app = Application(backend='uia').connect(title='Solera/DST - Big O Home Office 9.5_STD_BGO')
        window = app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
        security_login = window.child_window(title="Security Login", control_type="Window")

        user_id = security_login.child_window(title="txtUserid", control_type="Edit")
        user_id.type_keys(self.config["username"])
        SendKeys("{ENTER}")
        time.sleep(1)

        password_input = security_login.child_window(title="txtPassword", control_type="Edit")
        password_input.type_keys(self.config["password"])
        SendKeys("{ENTER}")

    def close_pos(self):
        app = Application(backend='uia').connect(title='Solera/DST - Big O Home Office 9.5_STD_BGO')
        window = app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
        window.set_focus()

        for process in psutil.process_iter(attrs=['pid', 'name']):
            if "homoff.exe" in process.info['name']:
                try:
                    process_obj = psutil.Process(process.info['pid'])
                    process_obj.terminate()  # Terminate the process
                    process_obj.wait(timeout=5)  # Optionally wait for the process to terminate
                except psutil.NoSuchProcess:
                    pass





