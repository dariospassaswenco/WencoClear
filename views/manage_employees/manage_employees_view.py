from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton
from views.manage_employees.upload_tab import UploadTab
from views.manage_employees.edit_employees_tab import EditEmployeesTab
from views.manage_employees.discrepancy_manager_tab import DiscrepancyManagerTab
from database.employees import get_store_types, get_positions

class ManageEmployeesView(QWidget):
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

        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create tabs
        self.create_discrepancy_manager_tab()
        self.create_edit_employees_tab()
        self.create_upload_tab()

        self.setLayout(layout)

    def create_discrepancy_manager_tab(self):
        store_types = get_store_types()
        positions = get_positions()

        self.discrepancy_manager_tab = DiscrepancyManagerTab(store_types, positions)
        self.tab_widget.addTab(self.discrepancy_manager_tab, "Discrepancy Manager")

    def create_edit_employees_tab(self):
        self.edit_employees_tab = EditEmployeesTab()
        self.tab_widget.addTab(self.edit_employees_tab, "Edit Employees")

    def create_upload_tab(self):
        self.upload_tab = UploadTab()
        self.tab_widget.addTab(self.upload_tab, "Upload Employees")
