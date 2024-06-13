from .base_basic_navigation import BasicNavigation
from config.pos_config import midas_config
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto import Desktop
# from config.app_config import RO_WORKING_DIRECTORY
import psutil


class MidasNavigation(BasicNavigation):
    def __init__(self):
        super().__init__()
        self.set_attributes()

    def set_attributes(self):
        self.config = midas_config
        self.pos_name = self.config["pos_name"]
        self.working_directory = RO_WORKING_DIRECTORY
        self.executable_path = self.config["executable"]
        self.running_program_title = self.config["running_program_title"]
        self.main_window_title = self.config["main_window_title"]

    def prepare_pos(self):
        super().prepare_pos()

        self.handle_pop_up()
        self.open_reporting_window()
        self.check_store_specific_window()

    def handle_pop_up(self):
        print("Handling Midas-specific pop-ups...")
        popup_window = None
        desktop = Desktop(backend="uia")
        popup_window = desktop.window(title="R.O. Writer Central Service")
        if popup_window.exists():
            # Click the "OK" button
            ok_button = popup_window.child_window(title="OK", control_type="Button")
            ok_button.click_input()
        else:
            print("Pop-up window not found.")
        pass

    def open_reporting_window(self):
        try:
            app = Application(backend="uia").connect(title_re="Point of Sale - R\.O\. Writer.*")
            ro_window = app.window(title_re="Point of Sale - R\.O\. Writer.*")
            print("Successfully connected to RO Writer window")
            ro_window.set_focus()
            reporting_button = ro_window.child_window(auto_id="itemImage", control_type='Image', found_index=8)
            reporting_button.click_input()
        except ElementNotFoundError:
            print("R.O Writer window not found. Make sure it's open and focused.")

    def check_store_specific_window(self):
        app = Application(backend='uia').connect(title='Reporting - R.O. Writer')
        reporting_window = app.window(title="Reporting - R.O. Writer")
        store_specific_window = None
        store_specific_window = reporting_window.child_window(title="Close Store Specific Windows",
                                                              control_type="Window")
        if store_specific_window.exists():
            ok_button = store_specific_window.child_window(title="OK", auto_id="1", control_type="Button")
            ok_button.click_input()
            print("Store Specific Pop-up closed")
        else:
            print("Store Specific Pop-up window not found.")

    def close_pos(self):
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if "rowriter" in process.info['name']:
                try:
                    process_obj = psutil.Process(process.info['pid'])
                    process_obj.terminate()  # Terminate the process
                    process_obj.wait(timeout=5)  # Optionally wait for the process to terminate
                except psutil.NoSuchProcess:
                    pass