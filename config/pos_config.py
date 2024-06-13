from .app_settings import NAVEX_EXECUTABLE, ROWRITER_EXECUTABLE, RO_PASSWORD, NAVEX_USERNAME, NAVEX_PASSWORD

# Configuration for Midas POS system
midas_config = {
    "pos_name": "RO Writer",
    "executable": ROWRITER_EXECUTABLE,
    "running_program_title": "rowriter",
    "password": RO_PASSWORD,
    "login_window_title": "R.O. Writer Central Service",
    "main_window_title": r"Point of Sale - R\.O\. Writer.*",
    "reporting_window_title": "Reporting - R.O. Writer",
    "username_field": {"title": "cbouserid", "control_type": "ComboBox"},
    "password_field": {"title": "txtPassword", "control_type": "Edit"},
    # Add more UI elements as neede19d
}

# Configuration for Bigo POS system
bigo_config = {
    "pos_name": "Navex",
    "executable": NAVEX_EXECUTABLE,
    "running_program_title": "homoff.exe",
    "username": NAVEX_USERNAME,
    "password": NAVEX_PASSWORD,
    "main_window_title": "Solera/DST - Big O Home Office 9.5_STD_BGO",
    "reporting_window_title": "Solera/DST - Big O Home Office 9.5_STD_BGO",
    "ss_report_title": "SALES SUMMARY BY GROUP CODE",
    "tech_report_title": "MECHANIC SALES SUMMARY BY GROUP CODE",
    "timesheet_report_title": "EMPLOYEE TIME-CLOCK HOURS",
}

