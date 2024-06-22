import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from views.main_menu import MainMenu
from views.data_checkup_view.data_checkup_view import DataCheckupView
from views.configure.configure_view import ConfigureView
from views.timesheets_view import TimesheetsView
from views.manage_employees.manage_employees_view import ManageEmployeesView
from views.manage_goals.manage_goals_view import ManageGoalsView  # Import the new view
import os

class DataManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Wenco Data Manager')
        self.setGeometry(200, 200, 2000, 1200)

        icon_path = os.path.join(os.path.dirname(__file__), 'views', 'assets', 'logo.ico')
        self.setWindowIcon(QIcon(icon_path))

        self.stacked_widget = QStackedWidget()

        self.main_menu = MainMenu(self.stacked_widget)
        self.data_checkup_view = DataCheckupView(self.stacked_widget)
        self.configure_view = ConfigureView(self.stacked_widget)
        self.timesheets_view = TimesheetsView(self.stacked_widget)
        self.manage_employees_view = ManageEmployeesView(self.stacked_widget)
        self.manage_goals_view = ManageGoalsView(self.stacked_widget)  # Initialize the new view

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.data_checkup_view)
        self.stacked_widget.addWidget(self.configure_view)
        self.stacked_widget.addWidget(self.timesheets_view)
        self.stacked_widget.addWidget(self.manage_employees_view)
        self.stacked_widget.addWidget(self.manage_goals_view)  # Add the new view to the stacked widget

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
