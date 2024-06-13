from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QLabel, QDateEdit, QComboBox, QTableWidget
from views.data_checkup_view.helpers import run_data_checkup
from views.data_checkup_view.fetch_functions import fetch_all_missing_data
from views.data_checkup_view.display_functions import display_data, display_tech_data, display_timesheet_data
from views.data_checkup_view.fetch_functions import fetch_missing_midas_ss_reports  # Import the new function
from PyQt5.QtCore import QDate, Qt

class DataCheckupView(QWidget):
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add home button
        btn_home = QPushButton('Home')
        btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(btn_home)

        # Store type selection
        self.store_type_combo = QComboBox()
        self.store_type_combo.addItems(["All", "Midas", "Bigo"])
        layout.addWidget(self.store_type_combo)

        # Date range input
        date_layout = QHBoxLayout()
        self.start_date_edit = QDateEdit()
        self.end_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addDays(-7))
        self.end_date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.start_date_edit)
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.end_date_edit)
        layout.addLayout(date_layout)

        # Fetch all missing button
        fetch_all_missing_button = QPushButton("Fetch All Missing Data")
        fetch_all_missing_button.setStyleSheet("background-color: lightgreen; font-weight: bold;")
        fetch_all_missing_button.clicked.connect(self.fetch_all_missing_data)
        layout.addWidget(fetch_all_missing_button)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.all_reports_tab, self.all_reports_results_table = self.create_report_tab("All Reports")
        self.sales_summary_tab, self.sales_summary_results_table = self.create_report_tab("Sales Summary")
        self.tech_tab, self.tech_results_table = self.create_report_tab("Tech Data")
        self.timesheet_tab, self.timesheet_results_table = self.create_report_tab("Timesheet Data")
        if self.store_type_combo.currentText() != "Bigo":
            self.sales_by_category_tab, self.sales_by_category_results_table = self.create_report_tab("Sales By Category")

        self.tab_widget.addTab(self.all_reports_tab, "All Reports")
        self.tab_widget.addTab(self.sales_summary_tab, "Sales Summary")
        self.tab_widget.addTab(self.tech_tab, "Tech Data")
        self.tab_widget.addTab(self.timesheet_tab, "Timesheet Data")
        if self.store_type_combo.currentText() != "Bigo":
            self.tab_widget.addTab(self.sales_by_category_tab, "Sales By Category")

        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

    def create_report_tab(self, report_type):
        widget = QWidget()
        layout = QVBoxLayout()

        # Run checkup button
        run_checkup_button = QPushButton(f"Run {report_type} Data Checkup")
        run_checkup_button.setStyleSheet("background-color: yellow; font-weight bold;")
        run_checkup_button.clicked.connect(lambda: self.run_data_checkup(report_type))
        layout.addWidget(run_checkup_button)

        # Results table
        results_table = QTableWidget()
        layout.addWidget(results_table)

        # Fetch buttons
        fetch_missing_button = QPushButton(f"Fetch Missing {report_type} Data")
        fetch_missing_button.setStyleSheet("background-color: lightgrey; font-weight: bold;")
        fetch_missing_button.clicked.connect(lambda: self.fetch_missing_data(report_type))
        fetch_layout = QHBoxLayout()
        fetch_layout.addWidget(fetch_missing_button)
        layout.addLayout(fetch_layout)

        widget.setLayout(layout)
        return widget, results_table

    def run_data_checkup(self, report_type):
        run_data_checkup(self, report_type)

    def fetch_all_missing_data(self):
        fetch_all_missing_data(self)

    def fetch_missing_data(self, report_type):
        if report_type == "Sales Summary":
            fetch_missing_midas_ss_reports(self)
        # Add more conditions for other report types if needed

