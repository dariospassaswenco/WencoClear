from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDateEdit, QTableWidget, QTableWidgetItem
from database.timesheet_data import get_midas_timesheet_data, get_bigo_timesheet_data
from excel.export_timesheet import export_timesheet_data
from PyQt5.QtCore import QDate
import pandas as pd

class TimesheetsView(QWidget):
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

        # Date range input
        date_layout = QHBoxLayout()
        self.ts_start_date_edit = QDateEdit()
        self.ts_end_date_edit = QDateEdit()
        self.ts_start_date_edit.setDate(QDate.currentDate().addDays(-14))
        self.ts_end_date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.ts_start_date_edit)
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.ts_end_date_edit)
        layout.addLayout(date_layout)

        # Fetch data button
        fetch_button = QPushButton("Fetch Timesheet Data")
        fetch_button.clicked.connect(self.fetch_timesheet_data)
        layout.addWidget(fetch_button)

        # Table to display results
        self.timesheet_table = QTableWidget()
        layout.addWidget(self.timesheet_table)

        # Export button
        export_button = QPushButton("Export to Excel")
        export_button.clicked.connect(self.export_timesheet_data)
        layout.addWidget(export_button)

        layout.addWidget(QLabel("Manage timesheets here"))
        self.setLayout(layout)

    def fetch_timesheet_data(self):
        start_date = self.ts_start_date_edit.date().toPyDate()
        end_date = self.ts_end_date_edit.date().toPyDate()

        midas_data = get_midas_timesheet_data(start_date, end_date)
        bigo_data = get_bigo_timesheet_data(start_date, end_date)
        combined_data = pd.concat([midas_data, bigo_data])

        combined_data.sort_values(by=['last_name', 'first_name'], inplace=True)
        pivot_data = combined_data.pivot_table(index=['last_name', 'first_name'], columns='date', values='hours', fill_value=0)

        self.display_timesheet_data(pivot_data)

    def display_timesheet_data(self, data):
        self.timesheet_table.clear()

        # Set table dimensions
        self.timesheet_table.setRowCount(len(data))
        self.timesheet_table.setColumnCount(len(data.columns) + 2)  # +2 for first name and last name

        # Set table headers
        self.timesheet_table.setHorizontalHeaderLabels(['Last Name', 'First Name'] + list(data.columns))

        # Fill the table
        for row_idx, (index, row) in enumerate(data.iterrows()):
            self.timesheet_table.setItem(row_idx, 0, QTableWidgetItem(index[0]))  # Last name
            self.timesheet_table.setItem(row_idx, 1, QTableWidgetItem(index[1]))  # First name
            for col_idx, value in enumerate(row):
                self.timesheet_table.setItem(row_idx, col_idx + 2, QTableWidgetItem(str(value)))

    def export_timesheet_data(self):
        start_date = self.ts_start_date_edit.date().toPyDate()
        end_date = self.ts_end_date_edit.date().toPyDate()

        midas_data = get_midas_timesheet_data(start_date, end_date)
        bigo_data = get_bigo_timesheet_data(start_date, end_date)
        combined_data = pd.concat([midas_data, bigo_data])

        export_timesheet_data(combined_data, start_date, end_date)  # Use the updated function to include path from config
