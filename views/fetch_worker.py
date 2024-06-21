import pandas as pd
import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QDateEdit, QTextEdit, QMessageBox
)
from PyQt5.QtCore import QDate, QThread, QObject, pyqtSignal
import traceback
from database.employees import get_employee_discrepancies
from config.app_settings import CLEAR_DATABASE_PATH

class FetchWorker(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, fetch_function, view):
        super().__init__()
        self.fetch_function = fetch_function
        self.view = view
        self._is_running = True

    def run(self):
        try:
            self.fetch_function(self.view, self.stop_requested, self.progress.emit)
        except Exception as e:
            self.progress.emit(f"Error: {e}")
            traceback.print_exc()
        finally:
            if self._is_running:
                self.finished.emit()
            else:
                self.stopped.emit()

    def stop(self):
        self._is_running = False

    def stop_requested(self):
        return not self._is_running
