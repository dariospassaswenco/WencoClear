# main_menu.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class MainMenu(QWidget):
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        btn_data_checkup = QPushButton('Data Checkup')
        btn_configure = QPushButton('Configure')
        btn_timesheets = QPushButton('Timesheets')

        btn_data_checkup.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        btn_configure.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        btn_timesheets.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        layout.addWidget(btn_data_checkup)
        layout.addWidget(btn_configure)
        layout.addWidget(btn_timesheets)

        self.setLayout(layout)
