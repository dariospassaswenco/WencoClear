from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDateEdit, QTableWidget, QTableWidgetItem, QTextEdit
from PyQt5.QtCore import QDate, QThread, pyqtSignal
import pandas as pd
from datetime import timedelta

from database.timesheet_data import get_midas_timesheet_data, get_bigo_timesheet_data
from excel.export_timesheet import export_timesheet_data
from views.fetch_worker import FetchWorker
from config.app_settings import EXCELEXPORT

class TimesheetsView(QWidget):
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.worker = None
        self.thread = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add home button
        btn_home = QPushButton('Home')
        btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(btn_home)

        # Date range input
        date_layout = QHBoxLayout()
        self.ts_start_date_edit = self.create_date_edit()
        self.ts_end_date_edit = self.create_date_edit()
        self.set_default_date_range()
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.ts_start_date_edit)
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.ts_end_date_edit)
        layout.addLayout(date_layout)

        # Fetch data button
        fetch_button = QPushButton("Fetch Timesheet Data")
        fetch_button.clicked.connect(self.start_fetch_timesheet_data)
        layout.addWidget(fetch_button)

        # Table to display results
        self.timesheet_table = QTableWidget()
        layout.addWidget(self.timesheet_table)

        # Export button
        export_button = QPushButton("Export to Excel")
        export_button.clicked.connect(self.export_timesheet_data)
        layout.addWidget(export_button)

        # Progress text box
        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        self.progress_text.setFixedHeight(150)
        layout.addWidget(self.progress_text)

        self.setLayout(layout)

    def create_date_edit(self):
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        return date_edit

    def set_default_date_range(self):
        today = QDate.currentDate()
        end_of_week = today.addDays(6 - today.dayOfWeek())  # Next Sunday
        start_of_week = end_of_week.addDays(-13)  # Two weeks prior to the end of the week
        self.ts_start_date_edit.setDate(start_of_week)
        self.ts_end_date_edit.setDate(end_of_week)

    def start_fetch_timesheet_data(self):
        if self.worker is not None:
            self.append_progress("Fetch already in progress.")
            return
        self.worker = FetchWorker(self.fetch_timesheet_data, self)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.progress.connect(self.append_progress)
        self.worker.finished.connect(self.on_fetch_finished)
        self.worker.stopped.connect(self.on_fetch_stopped)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.cleanup_thread)
        self.thread.start()

    def fetch_timesheet_data(self, view, stop_requested, progress_callback):
        start_date = view.ts_start_date_edit.date().toPyDate()
        end_date = view.ts_end_date_edit.date().toPyDate()

        progress_callback("Fetching Midas timesheet data...")
        midas_data = get_midas_timesheet_data(start_date, end_date)
        progress_callback("Fetching Bigo timesheet data...")
        bigo_data = get_bigo_timesheet_data(start_date, end_date)
        combined_data = pd.concat([midas_data, bigo_data])

        combined_data.sort_values(by=['last_name', 'first_name'], inplace=True)
        pivot_data = combined_data.pivot_table(index=['last_name', 'first_name'], columns='date', values='hours', fill_value=0)

        view.display_timesheet_data(pivot_data)
        progress_callback("Timesheet data fetched.")

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

        progress_callback = self.append_progress

        progress_callback("Exporting timesheet data to Excel...")
        midas_data = get_midas_timesheet_data(start_date, end_date)
        bigo_data = get_bigo_timesheet_data(start_date, end_date)
        combined_data = pd.concat([midas_data, bigo_data])

        progress_callback(f"Timesheet data exported to {EXCELEXPORT}")

    def append_progress(self, message):
        self.progress_text.append(message)
        self.progress_text.verticalScrollBar().setValue(self.progress_text.verticalScrollBar().maximum())

    def on_fetch_finished(self):
        self.append_progress("Fetch completed.")
        self.cleanup_thread()

    def on_fetch_stopped(self):
        self.append_progress("Fetch canceled.")
        self.cleanup_thread()

    def cleanup_thread(self):
        self.worker = None
        if self.thread is not None:
            self.thread.quit()
            self.thread.wait()
            self.thread = None
