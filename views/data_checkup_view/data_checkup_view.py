from PyQt5.QtCore import QDate, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QLabel, QDateEdit, QComboBox, QTableWidget, QTextEdit
from .helpers import run_data_checkup
from views.fetch_worker import FetchWorker
from .fetch_functions import fetch_all_missing_data, fetch_missing_ss_data, fetch_missing_tech_data, fetch_missing_timesheet_data
from .display_functions import display_sales_summary_data, display_tech_data, display_timesheet_data, display_all_data
from config.app_settings import CLOSED_DAYS

class DataCheckupView(QWidget):
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

        # Store type selection
        self.store_type_combo = QComboBox()
        self.store_type_combo.addItems(["All", "Midas", "Bigo"])
        layout.addWidget(self.store_type_combo)

        # Date range input
        date_layout = QHBoxLayout()
        self.start_date_edit = self.create_date_edit()
        self.end_date_edit = self.create_date_edit()
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.start_date_edit)
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.end_date_edit)
        layout.addLayout(date_layout)

        # Set default week range
        self.set_default_week_range()

        # Fetch all missing button
        self.fetch_all_missing_button = QPushButton("Fetch All Missing Data")
        self.fetch_all_missing_button.setStyleSheet("background-color: lightgreen; font-weight: bold;")
        self.fetch_all_missing_button.clicked.connect(self.start_fetch_all_missing_data)
        layout.addWidget(self.fetch_all_missing_button)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.all_reports_tab, self.all_reports_results_table = self.create_report_tab("All Reports")
        self.sales_summary_tab, self.sales_summary_results_table = self.create_report_tab("Sales Summary")
        self.tech_tab, self.tech_results_table = self.create_report_tab("Tech Data")
        self.timesheet_tab, self.timesheet_results_table = self.create_report_tab("Timesheet Data")
        self.sales_by_category_tab, self.sales_by_category_results_table = self.create_report_tab("Sales By Category")

        self.tab_widget.addTab(self.all_reports_tab, "All Reports")
        self.tab_widget.addTab(self.sales_summary_tab, "Sales Summary")
        self.tab_widget.addTab(self.tech_tab, "Tech Data")
        self.tab_widget.addTab(self.timesheet_tab, "Timesheet Data")
        self.tab_widget.addTab(self.sales_by_category_tab, "Sales By Category")

        layout.addWidget(self.tab_widget)

        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        self.progress_text.setFixedHeight(150)  # Set the height of the progress text box
        layout.addWidget(self.progress_text)

        self.setLayout(layout)

        self.tab_widget.currentChanged.connect(self.on_tab_change)
        self.update_calendar()

    def create_date_edit(self):
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        return date_edit

    def set_default_week_range(self):
        today = QDate.currentDate()
        start_of_week = today.addDays(-(today.dayOfWeek() - 1))  # Monday
        end_of_week = start_of_week.addDays(6)  # Sunday
        self.start_date_edit.setDate(start_of_week)
        self.end_date_edit.setDate(end_of_week)

    def update_calendar(self):
        for date_edit in [self.start_date_edit, self.end_date_edit]:
            calendar_widget = date_edit.calendarWidget()
            for closed_day in CLOSED_DAYS:
                qdate = QDate.fromString(closed_day, 'yyyy-MM-dd')
                calendar_widget.setDateTextFormat(qdate, self.create_format(Qt.black))

            # Gray out Sundays
            for day in range(1, 32):  # Assuming max 31 days in a month
                date = QDate(date_edit.date().year(), date_edit.date().month(), day)
                if date.dayOfWeek() == Qt.Sunday:
                    calendar_widget.setDateTextFormat(date, self.create_format(Qt.gray))

    def create_format(self, color):
        format = QTextCharFormat()
        format.setForeground(color)
        return format

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
        if report_type != "All Reports":
            fetch_missing_button = QPushButton(f"Fetch Missing {report_type} Data")
            fetch_missing_button.setStyleSheet("background-color: lightgrey; font-weight: bold;")
            fetch_missing_button.clicked.connect(lambda: self.start_fetch_missing_data(report_type))
            fetch_layout = QHBoxLayout()
            fetch_layout.addWidget(fetch_missing_button)
            layout.addLayout(fetch_layout)

        widget.setLayout(layout)
        return widget, results_table

    def start_fetch_all_missing_data(self):
        if self.worker is not None:
            self.append_progress("Fetch already in progress.")
            return
        self.worker = FetchWorker(fetch_all_missing_data, self)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.progress.connect(self.append_progress)
        self.worker.finished.connect(self.on_fetch_finished)
        self.worker.stopped.connect(self.on_fetch_stopped)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.cleanup_thread)
        self.thread.start()

    def start_fetch_missing_data(self, report_type):
        if self.worker is not None:
            self.append_progress("Fetch already in progress.")
            return
        if report_type == "Sales Summary":
            fetch_function = fetch_missing_ss_data
        elif report_type == "Tech Data":
            fetch_function = fetch_missing_tech_data
        elif report_type == "Timesheet Data":
            fetch_function = fetch_missing_timesheet_data
        else:
            self.append_progress(f"Unknown report type: {report_type}")
            return
        self.worker = FetchWorker(fetch_function, self)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.progress.connect(self.append_progress)
        self.worker.finished.connect(self.on_fetch_finished)
        self.worker.stopped.connect(self.on_fetch_stopped)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.cleanup_thread)
        self.thread.start()

    def stop_fetch(self):
        if self.worker is not None:
            self.worker.stop()
        if self.thread is not None:
            self.thread.quit()
            self.thread.wait()
        self.append_progress("Fetch canceled.")
        self.cleanup_thread()

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

    def append_progress(self, message):
        self.progress_text.append(message)
        self.progress_text.verticalScrollBar().setValue(self.progress_text.verticalScrollBar().maximum())

    def run_data_checkup(self, report_type):
        run_data_checkup(self, report_type)

    def on_tab_change(self, index):
        current_tab = self.tab_widget.tabText(index)
        if current_tab == "All Reports":
            self.store_type_combo.hide()
        else:
            self.store_type_combo.show()
