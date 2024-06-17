from .base_reports_navigation import ReportActions
import time
from pywinauto.application import Application
from config.app_settings import MIDAS_STORE_NUMBERS

class MidasReportActions(ReportActions):
    def __init__(self, app, config):
        super().__init__()
        self.stores = MIDAS_STORE_NUMBERS
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

    def select_initial_store(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            working_on = window.child_window(control_type="ComboBox", found_index=0)
            working_on.click_input()
            initial_shop = working_on.child_window(control_type="ListItem", found_index=0)
            initial_shop.click_input()
            print("Initial Store Selected")
        self.perform_action_with_retry(action)

    def select_current_store(self, store_number):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            working_on = window.child_window(control_type="ComboBox", found_index=0)
            working_on.click_input()
            store_name = [key for key, value in self.stores.items() if value == store_number][0]
            shop = working_on.child_window(title_re=f".*{store_name}.*", control_type="ListItem")
            shop.click_input()
            print(f"Store {store_name} Selected")
        self.perform_action_with_retry(action)

    def enter_password(self):
        def type_password():
            password = self.config["password"]
            window = self.app.window(title="Reporting - R.O. Writer")
            dialog = window.child_window(auto_id="PasswordTextBox", control_type="Edit")
            dialog.type_keys(password, with_spaces=True)
            print("Password Typed")
        def ok():
            window = self.app.window(title="Reporting - R.O. Writer")
            ok_button = window.child_window(title="Ok", auto_id="OkButton", control_type="Button")
            ok_button.click_input()
            print("Password Entered")
        self.perform_action_with_retry(type_password)
        self.perform_action_with_retry(ok)

    def select_sales_reports_menu(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            other_reports_button = window.child_window(title='Sales Reports', control_type='Button')
            other_reports_button.click()
            print("Sales Reports Selected")
        self.perform_action_with_retry(action)

    def select_other_reports_menu(self):
        def action():
            app = Application(backend="uia").connect(title="Reporting - R.O. Writer")
            window = app.window(title="Reporting - R.O. Writer")
            window.set_focus()
            other_reports_button = window.child_window(title='Other Reports', control_type='Button')
            other_reports_button.click_input()
            print("Other Reports Selected")
        self.perform_action_with_retry(action)

    def ss_select_ss_report(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            technician_report = window.child_window(title="Summary Report", control_type="ListItem")
            technician_report.double_click_input()
            print("Summary Report Selected")
        self.perform_action_with_retry(action)

    def ts_select_timesheet_report(self):
        def action():
            app = Application(backend="uia").connect(title="Reporting - R.O. Writer")
            window = app.window(title="Reporting - R.O. Writer")
            window.set_focus()
            time_sheet_report = window.child_window(title="* Employees Time Sheet", control_type="ListItem")
            time_sheet_report.double_click_input()
            print("Employee Time Sheet Report Selected")
        self.perform_action_with_retry(action)

    def tech_select_tech_report(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            technician_report = window.child_window(title="Technician's Sales Report", control_type="ListItem")
            technician_report.double_click_input()
            print("Technician Report Selected")
            self.enter_password()
        self.perform_action_with_retry(action)

    def ts_select_employees(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            employee_window = window.child_window(title="Select Employees", control_type="Window")
            ok_button = employee_window.child_window(title="OK", control_type="Button")
            ok_button.click_input()
        self.perform_action_with_retry(action)

    def enter_date_range(self, start_date, end_date):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")

            # Establish Start Date
            start_date_field = window.child_window(title='Text area', control_type='Edit', found_index=1)
            start_date_field.double_click_input()
            start_date_field.type_keys(start_date)

            # Establish End Date
            end_date_field = window.child_window(title='Text area', control_type='Edit', found_index=0)
            end_date_field.double_click_input()
            end_date_field.type_keys(end_date)
            print("Date Range Entered")
        self.perform_action_with_retry(action)

    def select_generate_report(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            output_selection = window.child_window(title="Output Selection", control_type="Window")
            pdf_tab = output_selection.child_window(title="PDF", control_type="TabItem")
            pdf_tab.click_input()
            browse = output_selection.child_window(title="Browse...", control_type="Button")
            browse.click_input()
        self.perform_action_with_retry(action)

    def enter_filename(self, file_name):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            output_dialog = window.child_window(title_re="Output Location")
            file_name_button = output_dialog.child_window(title="File name:", control_type="ComboBox")
            edit_file_name = file_name_button.child_window(title="File name:", control_type="Edit")
            time.sleep(0.25)
            edit_file_name.type_keys(file_name)
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
            time.sleep(0.25)
            self.check_existing_file()

            output_selection = window.child_window(title="Output Selection", control_type="Window")
            pdf_ok = output_selection.child_window(title="OK", control_type="Button")
            pdf_ok.click_input()
        self.perform_action_with_retry(action)

    def save_file(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            output_selection = window.child_window(title="Output Selection", control_type="Window")
            pdf_ok = output_selection.child_window(title="OK", control_type="Button")
            pdf_ok.click_input()
        self.perform_action_with_retry(action)

    def check_existing_file(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            existing_dialog = window.child_window(title_re="Confirm Save As")
            if existing_dialog.exists():
                yes_button = existing_dialog.child_window(title="Yes", control_type="Button")
                yes_button.click_input()
        self.perform_action_with_retry(action)

    def wait_for_report_to_compile(self):
        timeout_duration = 60
        start_time = time.time()
        while time.time() - start_time < timeout_duration:
            compiling_report_window = self.app.window(title="Compiling Report Data")
            if compiling_report_window.exists():
                time.sleep(1)
            else:
                break

    def cleanup_and_close(self):
        def action():
            window = self.app.window(title="R.O. Writer")
            close_button = window.child_window(title="Close", control_type="Button", auto_id="CloseButton")
            close_button.click_input()
            print("Confirmation closed")
        self.perform_action_with_retry(action)

    def return_to_main_menu(self):
        def action():
            window = self.app.window(title="Reporting - R.O. Writer")
            sales_reports_dialog = window.child_window(title="Sales Reports", control_type="Window")
            close_button = sales_reports_dialog.child_window(title="Close", control_type="Button")
            close_button.click_input()
        self.perform_action_with_retry(action)
