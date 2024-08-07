from .base_reports_navigation import ReportActions, ReportActionError
from config.logging import logger
from config.app_settings import MIDAS_POS_CTRL_MAP
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.keyboard import send_keys
from pywinauto.timings import wait_until_passes, TimeoutError
import time

class MidasReportActions(ReportActions):
    def __init__(self, app, config):
        super().__init__()
        self.stores = MIDAS_POS_CTRL_MAP
        self.config = config
        self.app = app
        logger.info("Initialized MidasReportActions")

    def select_initial_store(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            working_on = window.child_window(control_type="ComboBox", found_index=0)
            working_on.click_input()
            initial_shop = working_on.child_window(control_type="ListItem", found_index=0)
            initial_shop.click_input()
            logger.info("Initial Store Selected")
        self.perform_action_with_retry(action)

    def select_current_store(self, store_number):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            working_on = window.child_window(control_type="ComboBox", found_index=0)
            working_on.click_input()
            store_name = next((key for key, value in self.stores.items() if value == store_number), None)
            if not store_name:
                raise ValueError(f"Store number {store_number} not found in store mapping")
            shop = working_on.child_window(title_re=f".*{store_name}.*", control_type="ListItem")
            shop.click_input()
            logger.info(f"Store {store_name} Selected")
        self.perform_action_with_retry(action)

    def enter_password(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")

            # Check if dialog exists
            dialog = window.child_window(auto_id="PasswordTextBox", control_type="Edit")
            if not dialog.exists():
                logger.info("Password dialog does not exist, continuing...")
                return

            # Type password
            password = self.config["password"]
            dialog.type_keys(password, with_spaces=True)
            logger.info("Password typed")

            # Click OK
            ok_button = window.child_window(title="Ok", auto_id="OkButton", control_type="Button")
            ok_button.click_input()
            logger.info("Password OK button clicked")

            # Verify that the password dialog is closed
            if dialog.exists():
                raise Exception("Password dialog still exists after clicking OK")

        self.perform_action_with_retry(action)

    def select_sales_reports_menu(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            other_reports_button = window.child_window(title='Sales Reports', control_type='Button')
            other_reports_button.click()
            logger.info("Sales Reports Selected")
        self.perform_action_with_retry(action)

    def select_other_reports_menu(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            window.set_focus()
            other_reports_button = window.child_window(title='Other Reports', control_type='Button')
            other_reports_button.click_input()
            logger.info("Other Reports Selected")
        self.perform_action_with_retry(action)

    def ss_select_ss_report(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            technician_report = window.child_window(title="Summary Report", control_type="ListItem")
            technician_report.double_click_input()
            logger.info("Summary Report Selected")
        self.perform_action_with_retry(action)

    def ts_select_timesheet_report(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            window.set_focus()
            time_sheet_report = window.child_window(title="* Employees Time Sheet", control_type="ListItem")
            time_sheet_report.double_click_input()
            logger.info("Employee Time Sheet Report Selected")
        self.perform_action_with_retry(action)

    def tech_select_tech_report(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            technician_report = window.child_window(title="Technician's Sales Report", control_type="ListItem")
            technician_report.double_click_input()
            logger.info("Technician Report Selected")
            self.enter_password()
        self.perform_action_with_retry(action)

    def sba_find_report_in_list(self):
        def action():
            time.sleep(2)  # Consider replacing this with an explicit wait
            send_keys("rev")
            send_keys("{ENTER}")
            logger.info("Typed keys to find report in list")
        self.perform_action_with_retry(action)

    def sba_select_sba_report(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            list_box = window.child_window(auto_id="gtlReports", control_type="List")
            sales_by_category = list_box.child_window(title="Sales by Category", control_type="ListItem")
            sales_by_category.double_click_input()
            logger.info("Sales by Category report selected")
            self.enter_password()
        self.perform_action_with_retry(action)

    def ts_select_employees(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            employee_window = window.child_window(title="Select Employees", control_type="Window")
            ok_button = employee_window.child_window(title="OK", control_type="Button")
            ok_button.click_input()
            logger.info("Employees selected")
        self.perform_action_with_retry(action)

    def enter_date_range(self, start_date, end_date):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            start_date_field = window.child_window(title='Text area', control_type='Edit', found_index=1)
            start_date_field.double_click_input()
            start_date_field.type_keys(start_date)
            end_date_field = window.child_window(title='Text area', control_type='Edit', found_index=0)
            end_date_field.double_click_input()
            end_date_field.type_keys(end_date)
            logger.info(f"Date Range Entered: {start_date} to {end_date}")
        self.perform_action_with_retry(action)

    def select_generate_report(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            output_selection = window.child_window(title="Output Selection", control_type="Window")
            pdf_tab = output_selection.child_window(title="PDF", control_type="TabItem")
            pdf_tab.click_input()
            browse = output_selection.child_window(title="Browse...", control_type="Button")
            browse.click_input()
            logger.info("Generate Report selected")
        self.perform_action_with_retry(action)

    def enter_filename(self, file_name):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            output_dialog = window.child_window(title_re="Output Location")
            file_name_button = output_dialog.child_window(title="File name:", control_type="ComboBox")
            edit_file_name = file_name_button.child_window(title="File name:", control_type="Edit")
            edit_file_name.type_keys(file_name)
            logger.info(f"Filename entered: {file_name}")
        self.perform_action_with_retry(action)

    def enter_file_destination(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            output_dialog = window.child_window(title_re="Output Location")
            split_button = output_dialog.child_window(title="All locations", control_type="SplitButton")
            split_button.click_input()
            address = output_dialog.child_window(title="Address", control_type="Edit")
            address.type_keys(f"{self.output_file}" + "{ENTER}")
            save_button = output_dialog.child_window(title="Save", control_type="Button")
            save_button.click_input()
            self.check_existing_file()
            output_selection = window.child_window(title="Output Selection", control_type="Window")
            pdf_ok = output_selection.child_window(title="OK", control_type="Button")
            pdf_ok.click_input()
            logger.info(f"File destination entered: {self.output_file}")
        self.perform_action_with_retry(action)

    def save_file(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            output_selection = window.child_window(title="Output Selection", control_type="Window")
            pdf_ok = output_selection.child_window(title="OK", control_type="Button")
            pdf_ok.click_input()
            logger.info("File saved")
        self.perform_action_with_retry(action)

    def check_existing_file(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            existing_dialog = window.child_window(title_re="Confirm Save As")
            if existing_dialog.exists():
                yes_button = existing_dialog.child_window(title="Yes", control_type="Button")
                yes_button.click_input()
                logger.info("Existing file overwritten")
        self.perform_action_with_retry(action)

    def wait_for_report_to_compile(self):
        def check_compile_window():
            return not self.app.window(title="Compiling Report Data").exists()

        try:
            wait_until_passes(60, 1, check_compile_window)
            logger.info("Report compilation completed")
        except TimeoutError:
            logger.error("Report compilation timed out")
            raise ReportActionError("Report compilation timed out")

    def cleanup_and_close(self):
        def action():
            window = self.app.window(title="R.O. Writer")
            close_button = window.child_window(title="Close", control_type="Button", auto_id="CloseButton")
            close_button.click_input()
            logger.info("Cleanup completed and window closed")
        self.perform_action_with_retry(action)

    def return_to_main_menu(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            sales_reports_dialog = window.child_window(title="Sales Reports", control_type="Window")
            close_button = sales_reports_dialog.child_window(title="Close", control_type="Button")
            close_button.click_input()
            logger.info("Returned to main menu")
        self.perform_action_with_retry(action)