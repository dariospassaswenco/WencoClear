import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QTextEdit
)
from PyQt5.QtCore import QThread
from config.app_settings import CLEAR_DATABASE_PATH
from excel.read_employees import read_employees
from database.employees import insert_employees
from views.fetch_worker import FetchWorker

class UploadTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.worker = None
        self.thread = None

    def initUI(self):
        layout = QVBoxLayout()

        # Add button to upload excel file
        btn_upload = QPushButton('Upload Employee Excel File')
        btn_upload.clicked.connect(self.upload_file)
        layout.addWidget(btn_upload)

        # Add label to display the status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        # Add table to display the employee data
        self.employee_table = QTableWidget()
        layout.addWidget(self.employee_table)

        # Add button to confirm import to database
        self.btn_confirm = QPushButton('Confirm Import to Database')
        self.btn_confirm.setEnabled(False)
        self.btn_confirm.clicked.connect(self.start_import)
        layout.addWidget(self.btn_confirm)

        # Add progress text box
        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        self.progress_text.setFixedHeight(150)
        layout.addWidget(self.progress_text)

        self.setLayout(layout)

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Optional: force use of non-native dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Excel File", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options
        )
        if file_path:
            self.process_excel(file_path)

    def process_excel(self, file_path):
        try:
            # Read the Excel file
            df = read_employees(file_path)

            # Display the data in the table
            self.display_employee_data(df)

            # Enable the confirm button
            self.df = df
            self.btn_confirm.setEnabled(True)
            self.status_label.setText("Data loaded successfully. Please confirm to import to the database.")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")
            print(f"Error: {e}")

    def display_employee_data(self, df):
        self.employee_table.setRowCount(df.shape[0])
        self.employee_table.setColumnCount(df.shape[1])
        self.employee_table.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.employee_table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

    def start_import(self):
        reply = QMessageBox.question(self, 'Confirm Import', 'This will overwrite existing employee data. Are you sure?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.worker = FetchWorker(self.import_data, self)
            self.thread = QThread()
            self.worker.moveToThread(self.thread)
            self.worker.progress.connect(self.append_progress)
            self.worker.finished.connect(self.on_import_finished)
            self.worker.stopped.connect(self.on_import_stopped)
            self.thread.started.connect(self.worker.run)
            self.thread.finished.connect(self.cleanup_thread)
            self.thread.start()

    def import_data(self, view, stop_requested, progress_callback):
        try:
            # Reset auto-increment
            self.reset_autoincrement()

            # Insert data into the database
            insert_employees(view.df)
            progress_callback("Data imported successfully.")
        except Exception as e:
            progress_callback(f"Error: {e}")
            print(f"Error: {e}")

    def reset_autoincrement(self):
        conn = sqlite3.connect(CLEAR_DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='employees'")
        conn.commit()
        conn.close()

    def append_progress(self, message):
        self.progress_text.append(message)
        self.progress_text.verticalScrollBar().setValue(self.progress_text.verticalScrollBar().maximum())

    def on_import_finished(self):
        self.append_progress("Import process completed.")
        self.btn_confirm.setEnabled(False)
        self.cleanup_thread()

    def on_import_stopped(self):
        self.append_progress("Import process stopped.")
        self.cleanup_thread()

    def cleanup_thread(self):
        self.worker = None
        if self.thread is not None:
            self.thread.quit()
            self.thread.wait()
            self.thread = None

