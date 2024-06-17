from .base_reports_navigation import ReportActions
import time
from pywinauto.application import Application
import pygetwindow as gw
from config.app_settings import *
from pywinauto.keyboard import SendKeys
from pywinauto.keyboard import send_keys

class BigoReportActions(ReportActions):
    def __init__(self, app, config):
        super().__init__()
        self.stores = BIGO_POS_CTRL_MAP
        self.config = config
        self.app = app

    def perform_action_with_retry(self, action, retries=3, delay=2):
        for attempt in range(retries):
            try:
                action()
                return
            except Exception as e:
                print(f"Error performing action: {e}. Retrying ({attempt + 1}/{retries})...")
                time.sleep(delay)
        print("Failed to perform action after multiple retries.")

    def select_report(self, report_title):
        def action():
            def find_pos_report_name():
                window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
                reports_combo = window.child_window(title="cboReports", control_type="ComboBox")
                combo_box_items = reports_combo.children()
                for index, item in enumerate(combo_box_items):
                    item_text = item.window_text().strip()
                    if report_title == item_text:
                        return item.window_text()

            def click_item(report_pos_title):
                window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
                reports_combo = window.child_window(title="cboReports", control_type="ComboBox")
                item = reports_combo.child_window(title=report_pos_title, control_type="ListItem")
                if item.exists():
                    item.click_input()
                    print(f"{item} clicked")

            def find_combo_distance(pos_report_name):
                window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
                reports_combo = window.child_window(title="cboReports", control_type="ComboBox")
                combo_box_items = reports_combo.children()
                for index, item in enumerate(combo_box_items):
                    if pos_report_name in item.window_text():
                        return index

            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            window.set_focus()
            reports_combo = window.child_window(title="cboReports", control_type="ComboBox")
            reports_combo.click_input()
            send_keys("a")
            time.sleep(.05)
            send_keys("{ENTER}")
            time.sleep(1)

            reports_combo.click_input()
            pos_report_name = find_pos_report_name()
            print(pos_report_name)
            first_three_letters = report_title[:3]
            send_keys(first_three_letters)
            send_keys("{ENTER}")
            time.sleep(1)

            print("first search completed")

            reports_combo.click_input()
            first_distance = find_combo_distance(pos_report_name)
            if first_distance > 15:
                print("over 15")
                down_presses_needed = (first_distance // 5) * 5  # To move in increments of 5
                for _ in range(down_presses_needed):
                    send_keys("{DOWN}")
                    time.sleep(0.5)
                send_keys("{ENTER}")
            else:
                clicked = False
                while not clicked:
                    send_keys("{ENTER}")
                    time.sleep(0.5)
                    reports_combo.click_input()
                    click_item(pos_report_name)
                    time.sleep(2)
                    reports_combo.click_input()
                    success = find_combo_distance(pos_report_name)
                    print(success)
                    if success == 0:
                        send_keys("{ENTER}")
                        print(f"{report_title} Successfully Selected")
                        break

        self.perform_action_with_retry(action)

    def ts_select_employees(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            all_button = window.child_window(title=">>", control_type="Button", found_index=0)
            all_button.click_input()
            ok_button = window.child_window(title="OK", control_type="Button")
            ok_button.click_input()
        self.perform_action_with_retry(action)

    def select_current_store(self, store_number):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            shop_combobox = window.child_window(title="cboStoreNo", control_type="ComboBox")
            store_code = [key for key, value in self.stores.items() if value == store_number][0]
            shop_combobox.click_input()
            shop_combobox.type_keys(str(store_code))
        self.perform_action_with_retry(action)

    def enter_date_range(self, start_date, end_date):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            combo_box = window.child_window(title="cboReports", control_type="ComboBox")
            combo_box.click_input()

            SendKeys("{ENTER}")
            window.type_keys(start_date)
            time.sleep(0.5)
            window.type_keys("{ENTER}")
            window.type_keys(end_date)
            time.sleep(0.5)
        self.perform_action_with_retry(action)

    def select_generate_report(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            excel_button = window.child_window(title="Excel", control_type="Button")
            excel_button.click()
            time.sleep(0.5)
        self.perform_action_with_retry(action)

    def enter_file_destination(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            save_as_dialog = window.child_window(title_re="Save As")
            # Find the "Save in" combo box in the "Save As" dialog
            save_in_cb = save_as_dialog.child_window(title="Save in:", control_type="ComboBox")
            # Click the "Save in" combo box to open the drop-down list
            save_in_cb.double_click_input()
            save_in_cb.click_input()
            time.sleep(0.5)

            save_in_list = save_in_cb.child_window(title="Save in:", control_type="List")
            documents = save_in_list.child_window(title="Documents", control_type="ListItem")
            documents.click_input()
            folder_output = save_as_dialog.child_window(title="WencoOutputs", control_type="ListItem")
            folder_output.double_click_input()
            time.sleep(0.5)
        self.perform_action_with_retry(action)

    def enter_filename(self, file_name):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            save_as_dialog = window.child_window(title_re="Save As")
            file_name_cb = save_as_dialog.child_window(title="File Name", control_type="ComboBox")
            edit_file_name = file_name_cb.child_window(title="File Name", control_type="Edit")
            edit_file_name.click_input()
            time.sleep(0.5)
            edit_file_name.type_keys(file_name)
        self.perform_action_with_retry(action)

    def save_file(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            save_as_dialog = window.child_window(title_re="Save As")
            save_button = save_as_dialog.child_window(title="Save", control_type="Button")
            save_button.click_input()
            self.check_existing_file()
            time.sleep(0.5)
        self.perform_action_with_retry(action)

    def check_existing_file(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            existing_dialog = window.child_window(title="Confirm Save As", control_type="Window")
            if existing_dialog.exists():
                yes_button = existing_dialog.child_window(title="Yes", control_type="Button")
                yes_button.click_input()
        self.perform_action_with_retry(action)

    def wait_for_report_to_compile(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            timeout_duration = 60
            start_time = time.time()

            while time.time() - start_time < timeout_duration:
                reports_window = window.child_window(title="Reports", control_type="Window")
                home_office_window = window.child_window(title="Home Office", control_type="Window")

                if reports_window.exists():
                    reports_window.child_window(title="OK", control_type="Button").click_input()
                    time.sleep(0.5)
                elif home_office_window.exists():
                    home_office_window.child_window(title="OK", control_type="Button").click_input()
                    time.sleep(1)
                    break  # Exit the loop when either window is found

                time.sleep(1)  # Adjust sleep interval as needed

        self.perform_action_with_retry(action)

    def cleanup_and_close(self, date):
        def action():
            excel_windows = [window for window in gw.getAllTitles() if
                             date in window]

            for window_title in excel_windows:
                print(f"Closing Excel window: {window_title}")
                gw.getWindowsWithTitle(window_title)[0].close()
        self.perform_action_with_retry(action)
