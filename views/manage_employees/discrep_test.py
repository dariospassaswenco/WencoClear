import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QComboBox, QTextEdit, QDateEdit, QApplication, QMessageBox
)
from PyQt5.QtCore import QDate
from database.employees import get_employee_discrepancies, get_store_types, get_positions, insert_discrepancy_employees

class DiscrepancyManagerTab(QWidget):
    def __init__(self, store_types, positions):
        super().__init__()
        print("Initializing DiscrepancyManagerTab...")
        self.store_types = [''] + store_types
        self.positions = [''] + positions
        self.initUI()
        self.df = None
        self.load_data()
        print("DiscrepancyManagerTab initialized.")

    def initUI(self):
        print("Setting up UI...")
        layout = QVBoxLayout()

        date_layout = QHBoxLayout()
        self.start_date_edit = self.create_date_edit()
        self.end_date_edit = self.create_date_edit()
        self.set_default_date_range()
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.start_date_edit)
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.end_date_edit)
        layout.addLayout(date_layout)

        btn_refresh = QPushButton('Refresh Data')
        btn_refresh.clicked.connect(self.load_data)
        layout.addWidget(btn_refresh)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.discrepancy_table = QTableWidget()
        layout.addWidget(self.discrepancy_table)

        btn_export = QPushButton('Export to Employees')
        btn_export.clicked.connect(self.start_export)
        layout.addWidget(btn_export)

        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        self.progress_text.setFixedHeight(150)
        layout.addWidget(self.progress_text)

        self.setLayout(layout)
        print("UI setup complete.")

    def create_date_edit(self):
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        return date_edit

    def set_default_date_range(self):
        today = QDate.currentDate()
        end_of_week = today.addDays(6 - today.dayOfWeek())
        start_of_week = end_of_week.addDays(-13)
        self.start_date_edit.setDate(start_of_week)
        self.end_date_edit.setDate(end_of_week)

    def load_data(self):
        print("Loading data...")
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()
        self.df = get_employee_discrepancies(start_date, end_date)
        if self.df.empty:
            self.status_label.setStyleSheet("color: green;")
            self.status_label.setText("There are no timesheet discrepancies for the period.")
        else:
            self.status_label.setStyleSheet("color: red;")
            self.status_label.setText(f"There are {self.df.shape[0]} timesheet discrepancies for the period.")
        self.display_discrepancy_data(self.df)
        self.append_progress("Data loaded successfully.")
        print("Data loaded.")

    def display_discrepancy_data(self, df):
        self.discrepancy_table.setRowCount(df.shape[0])
        self.discrepancy_table.setColumnCount(5)
        self.discrepancy_table.setHorizontalHeaderLabels(['First Name', 'Last Name', 'Wenco ID', 'Store Type', 'Position Title'])
        for i in range(df.shape[0]):
            self.discrepancy_table.setItem(i, 0, QTableWidgetItem(df.iloc[i, 0]))
            self.discrepancy_table.setItem(i, 1, QTableWidgetItem(df.iloc[i, 1]))
            self.discrepancy_table.setItem(i, 2, QTableWidgetItem(df.iloc[i, 2] if pd.notna(df.iloc[i, 2]) else ""))
            store_type_combo = QComboBox()
            store_type_combo.addItems(self.store_types)
            self.discrepancy_table.setCellWidget(i, 3, store_type_combo)
            position_combo = QComboBox()
            position_combo.addItems(self.positions)
            self.discrepancy_table.setCellWidget(i, 4, position_combo)

    def start_export(self):
        reply = QMessageBox.question(self, 'Confirm Export', 'Are you sure you want to export the filled records?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.export_data()

    def export_data(self):
        filled_df = self.get_filled_rows()
        insert_discrepancy_employees(filled_df)
        self.load_data()
        self.append_progress("Data exported successfully.")

    def get_filled_rows(self):
        filled_rows = []
        for i in range(self.discrepancy_table.rowCount()):
            first_name = self.discrepancy_table.item(i, 0).text()
            last_name = self.discrepancy_table.item(i, 1).text()
            wenco_id = self.discrepancy_table.item(i, 2).text()
            type_name = self.discrepancy_table.cellWidget(i, 3).currentText()
            position_name = self.discrepancy_table.cellWidget(i, 4).currentText()
            if type_name and position_name:
                filled_rows.append([first_name, last_name, wenco_id, type_name, position_name])
        return pd.DataFrame(filled_rows, columns=['first_name', 'last_name', 'wenco_id', 'type_name', 'position_name'])

    def append_progress(self, message):
        self.progress_text.append(message)
        self.progress_text.verticalScrollBar().setValue(self.progress_text.verticalScrollBar().maximum())

# Main application (for testing purposes)
if __name__ == "__main__":
    app = QApplication([])

    # Fetch the necessary data for the dropdowns once when the application starts
    store_types = get_store_types()
    positions = get_positions()

    # Create the main widget with the fetched data
    main_widget = DiscrepancyManagerTab(store_types, positions)

    # Show the main widget
    main_widget.show()

    # Execute the application
    app.exec_()
