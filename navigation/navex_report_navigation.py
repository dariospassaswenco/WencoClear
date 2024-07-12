from .base_reports_navigation import ReportActions, ReportActionError
from config.logging import logger
from config.app_settings import BIGO_POS_CTRL_MAP
from pywinauto.application import Application
from pywinauto.timings import wait_until_passes, TimeoutError
from pywinauto.keyboard import send_keys, SendKeys
import pygetwindow as gw
import time

class BigoReportActions(ReportActions):
    def __init__(self, app, config):
        super().__init__()
        self.stores = BIGO_POS_CTRL_MAP
        self.config = config
        self.app = app
        logger.info("Initialized BigoReportActions")

    def select_report(self, report_title):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            window.set_focus()
            reports_combo = window.child_window(title="cboReports", control_type="ComboBox")

            def find_pos_report_name():
                combo_box_items = reports_combo.children()
                return next((item.window_text() for item in combo_box_items if item.window_text().strip() == report_title), None)

            def click_item(report_pos_title):
                item = reports_combo.child_window(title=report_pos_title, control_type="ListItem")
                if item.exists():
                    item.click_input()
                    logger.info(f"{item} clicked")

            def find_combo_distance(pos_report_name):
                combo_box_items = reports_combo.children()
                return next((index for index, item in enumerate(combo_box_items) if pos_report_name in item.window_text()), None)

            reports_combo.click_input()
            send_keys("a{ENTER}")
            wait_until_passes(10, 1, lambda: reports_combo.is_enabled())

            reports_combo.click_input()
            pos_report_name = find_pos_report_name()
            logger.info(f"POS report name: {pos_report_name}")
            send_keys(f"{report_title[:3]}{{ENTER}}")
            wait_until_passes(10, 1, lambda: reports_combo.is_enabled())

            logger.info("First search completed")

            reports_combo.click_input()
            first_distance = find_combo_distance(pos_report_name)
            if first_distance and first_distance > 15:
                logger.info("Over 15 items, scrolling")
                down_presses_needed = (first_distance // 5) * 5
                for _ in range(down_presses_needed):
                    send_keys("{DOWN}")
                    time.sleep(0.5)
                send_keys("{ENTER}")
            else:
                while True:
                    send_keys("{ENTER}")
                    wait_until_passes(10, 1, lambda: reports_combo.is_enabled())
                    reports_combo.click_input()
                    click_item(pos_report_name)
                    wait_until_passes(10, 1, lambda: reports_combo.is_enabled())
                    reports_combo.click_input()
                    success = find_combo_distance(pos_report_name)
                    logger.info(f"Combo distance: {success}")
                    if success == 0:
                        send_keys("{ENTER}")
                        logger.info(f"{report_title} Successfully Selected")
                        break

        self.perform_action_with_retry(action)

    def ts_select_employees(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            all_button = window.child_window(title=">>", control_type="Button", found_index=0)
            all_button.click_input()
            ok_button = window.child_window(title="OK", control_type="Button")
            ok_button.click_input()
            logger.info("All employees selected")
        self.perform_action_with_retry(action)

    def select_current_store(self, store_number):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            shop_combobox = window.child_window(title="cboStoreNo", control_type="ComboBox")
            store_code = next((key for key, value in self.stores.items() if value == store_number), None)
            if not store_code:
                raise ValueError(f"Store number {store_number} not found in store mapping")
            shop_combobox.click_input()
            shop_combobox.type_keys(str(store_code))
            logger.info(f"Store {store_number} selected")
        self.perform_action_with_retry(action)

    def enter_date_range(self, start_date, end_date):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            combo_box = window.child_window(title="cboReports", control_type="ComboBox")
            combo_box.click_input()
            SendKeys("{ENTER}")
            window.type_keys(start_date)
            wait_until_passes(10, 1, lambda: window.is_enabled())
            window.type_keys("{ENTER}")
            window.type_keys(end_date)
            wait_until_passes(10, 1, lambda: window.is_enabled())
            logger.info(f"Date range entered: {start_date} to {end_date}")
        self.perform_action_with_retry(action)

    def select_generate_report(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            excel_button = window.child_window(title="Excel", control_type="Button")
            excel_button.click()
            wait_until_passes(10, 1, lambda: window.is_enabled())
            logger.info("Generate report selected")
        self.perform_action_with_retry(action)

    def enter_file_destination(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            save_as_dialog = window.child_window(title_re="Save As")
            save_in_cb = save_as_dialog.child_window(title="Save in:", control_type="ComboBox")
            save_in_cb.double_click_input()
            save_in_cb.click_input()
            wait_until_passes(10, 1, lambda: save_in_cb.is_enabled())

            save_in_list = save_in_cb.child_window(title="Save in:", control_type="List")
            documents = save_in_list.child_window(title="Documents", control_type="ListItem")
            documents.click_input()
            folder_output = save_as_dialog.child_window(title="WencoClearOutputs", control_type="ListItem")
            folder_output.double_click_input()
            logger.info("File destination entered")
        self.perform_action_with_retry(action)

    def enter_filename(self, file_name):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            save_as_dialog = window.child_window(title_re="Save As")
            file_name_cb = save_as_dialog.child_window(title="File Name", control_type="ComboBox")
            edit_file_name = file_name_cb.child_window(title="File Name", control_type="Edit")
            edit_file_name.click_input()
            wait_until_passes(10, 1, lambda: edit_file_name.is_enabled())
            edit_file_name.type_keys(file_name)
            logger.info(f"Filename entered: {file_name}")
        self.perform_action_with_retry(action)

    def save_file(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            save_as_dialog = window.child_window(title_re="Save As")
            save_button = save_as_dialog.child_window(title="Save", control_type="Button")
            save_button.click_input()
            self.check_existing_file()
            wait_until_passes(10, 1, lambda: window.is_enabled())
            logger.info("File saved")
        self.perform_action_with_retry(action)

    def check_existing_file(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            existing_dialog = window.child_window(title="Confirm Save As", control_type="Window")
            if existing_dialog.exists():
                yes_button = existing_dialog.child_window(title="Yes", control_type="Button")
                yes_button.click_input()
                logger.info("Existing file overwritten")
        self.perform_action_with_retry(action)

    def wait_for_report_to_compile(self):
        def action():
            window = self.app.window(title="Solera/DST - Big O Home Office 9.5_STD_BGO", control_type="Window")
            def check_completion():
                reports_window = window.child_window(title="Reports", control_type="Window")
                home_office_window = window.child_window(title="Home Office", control_type="Window")
                if reports_window.exists():
                    reports_window.child_window(title="OK", control_type="Button").click_input()
                    return False
                elif home_office_window.exists():
                    home_office_window.child_window(title="OK", control_type="Button").click_input()
                    return True
                return False

            try:
                wait_until_passes(60, 1, check_completion)
                logger.info("Report compilation completed")
            except TimeoutError:
                logger.error("Report compilation timed out")
                raise ReportActionError("Report compilation timed out")

        self.perform_action_with_retry(action)

    def cleanup_and_close(self):
        def action():
            excel_windows = [window for window in gw.getAllTitles() if "Excel" in window]
            for window_title in excel_windows:
                logger.info(f"Closing Excel window: {window_title}")
                gw.getWindowsWithTitle(window_title)[0].close()
        self.perform_action_with_retry(action)
