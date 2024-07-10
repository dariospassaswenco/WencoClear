from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDateEdit, QTableWidget, QTableWidgetItem, QTextEdit
from PyQt5.QtCore import QDate, QThread
import pandas as pd
from datetime import datetime
import os
from database.timesheet_data import get_midas_timesheet_data, get_bigo_timesheet_data, get_oldest_date_entered
from excel.export_timesheet import export_timesheet_data
from views.fetch_worker import FetchWorker
from config.app_settings import EXCELEXPORT, MIDAS_STORE_NUMBERS
from generators.helpers import generate_midas_reports, generate_bigo_reports

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

        # Warning label and Generate Refreshment button layout
        warning_layout = QHBoxLayout()
        self.warning_label = QLabel("")
        warning_layout.addWidget(self.warning_label)

        generate_refreshment_button = QPushButton("Generate Refreshment")
        generate_refreshment_button.setFixedSize(150, 25)
        generate_refreshment_button.clicked.connect(self.start_fetch_timesheet_data)
        warning_layout.addWidget(generate_refreshment_button)

        layout.addLayout(warning_layout)

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

        # Display Timesheet button
        display_button = QPushButton("Display Timesheet")
        display_button.clicked.connect(self.start_refresh_timesheet_data)
        layout.addWidget(display_button)

        # Table to display results
        self.timesheet_table = QTableWidget()
        layout.addWidget(self.timesheet_table)

        # Export button
        export_button = QPushButton("Export to Excel")
        export_button.clicked.connect(self.start_export_timesheet_data)
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
        self.worker = FetchWorker(self.fetch_missing_timesheet_data, self)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.progress.connect(self.append_progress)
        self.worker.finished.connect(self.on_fetch_finished)
        self.worker.stopped.connect(self.on_fetch_stopped)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.cleanup_thread)
        self.thread.start()

    def start_refresh_timesheet_data(self):
        if self.worker is not None:
            self.append_progress("Refresh already in progress.")
            return
        self.worker = FetchWorker(self.refresh_timesheet_data, self)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.progress.connect(self.append_progress)
        self.worker.finished.connect(self.on_fetch_finished)
        self.worker.stopped.connect(self.on_fetch_stopped)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.cleanup_thread)
        self.thread.start()

    def fetch_missing_timesheet_data(self, view, stop_requested, progress_callback):
        store_type = "All"
        start_date = view.ts_start_date_edit.date().toPyDate()
        end_date = view.ts_end_date_edit.date().toPyDate()
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        if store_type == "All" or store_type == "Midas":
            progress_callback("Fetching Midas Timesheet Data")
            timesheet_midas = {store: [(start_date_str, end_date_str)] for store in MIDAS_STORE_NUMBERS}
            if not any(timesheet_midas.values()):
                progress_callback("Timesheet data for Midas is up to date.")
            else:
                progress_callback(f"Midas Timesheet Data: {timesheet_midas}")
                if stop_requested():
                    progress_callback("Fetch canceled.")
                    return
                generate_midas_reports(None, None, timesheet_midas, stop_requested, progress_callback)

        if store_type == "All" or store_type == "Bigo":
            progress_callback("Fetching Bigo Timesheet Data")
            timesheet_bigo = [(start_date_str, end_date_str)]
            if not timesheet_bigo:
                progress_callback("Timesheet data for Bigo is up to date.")
            else:
                progress_callback(f"Bigo Timesheet Data: {timesheet_bigo}")
                if stop_requested():
                    progress_callback("Fetch canceled.")
                    return
                generate_bigo_reports(None, None, timesheet_bigo, stop_requested, progress_callback)

        progress_callback("Fetching Timesheet data completed.")

    def refresh_timesheet_data(self, view, stop_requested, progress_callback):
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

        # Check the oldest date entered
        oldest_entry = get_oldest_date_entered(start_date, end_date)
        if oldest_entry:
            wenco_id, last_name, first_name, oldest_date_entered = oldest_entry
            oldest_date_entered_dt = datetime.strptime(oldest_date_entered, '%Y-%m-%d %H:%M:%S')
            days_diff = (datetime.now() - oldest_date_entered_dt).days
            if days_diff > 1:
                view.warning_label.setStyleSheet("color: red;")
                view.warning_label.setText(
                    f"Warning: Oldest Timesheet Entry for this Interval is {oldest_date_entered} "
                    f"by {first_name} {last_name} at Shop: {wenco_id}. Recommend to refresh before export."
                )
            else:
                view.warning_label.setStyleSheet("color: green;")
                view.warning_label.setText(
                    f"Oldest Timesheet Entry is {oldest_date_entered} "
                    f"by {first_name} {last_name} at Shop: {wenco_id}. Data is up to date."
                )

    def start_export_timesheet_data(self):
        if self.worker is not None:
            self.append_progress("Export already in progress.")
            return
        self.worker = FetchWorker(self.export_timesheet_data, self)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.progress.connect(self.append_progress)
        self.worker.finished.connect(self.on_export_finished)
        self.worker.stopped.connect(self.on_fetch_stopped)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.cleanup_thread)
        self.thread.start()

    def export_timesheet_data(self, view, stop_requested, progress_callback):
        start_date = view.ts_start_date_edit.date().toPyDate()
        end_date = view.ts_end_date_edit.date().toPyDate()

        progress_callback("Exporting timesheet data to Excel...")
        midas_data = get_midas_timesheet_data(start_date, end_date)
        bigo_data = get_bigo_timesheet_data(start_date, end_date)
        combined_data = pd.concat([midas_data, bigo_data])

        export_timesheet_data(combined_data, start_date, end_date)  # Use the updated function to include path from config

        file_name = f"timesheet_data_{start_date}_{end_date}.xlsx"
        file_path = os.path.join(EXCELEXPORT, file_name)
        progress_callback(f"Timesheet data exported to {file_path}")

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

    def append_progress(self, message):
        self.progress_text.append(message)
        self.progress_text.verticalScrollBar().setValue(self.progress_text.verticalScrollBar().maximum())

    def on_fetch_finished(self):
        self.append_progress("Fetch completed.")
        self.cleanup_thread()

    def on_export_finished(self):
        self.append_progress("Export completed.")
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
