# app.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout
from views.main_menu import MainMenu
from views.data_checkup_view.data_checkup_view import DataCheckupView
from views.configure_view import ConfigureView
from views.timesheets_view import TimesheetsView

class DataManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('WencoClear')
        self.setGeometry(200, 200, 2000, 1200)

        self.stacked_widget = QStackedWidget()

        self.main_menu = MainMenu(self.stacked_widget)
        self.data_checkup_view = DataCheckupView(self.stacked_widget)
        self.configure_view = ConfigureView(self.stacked_widget)
        self.timesheets_view = TimesheetsView(self.stacked_widget)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.data_checkup_view)
        self.stacked_widget.addWidget(self.configure_view)
        self.stacked_widget.addWidget(self.timesheets_view)

        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.stacked_widget)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DataManagerGUI()
    ex.show()
    sys.exit(app.exec_())
