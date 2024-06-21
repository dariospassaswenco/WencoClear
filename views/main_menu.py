from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os

class MainMenu(QWidget):
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Title bar layout
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setAlignment(Qt.AlignCenter)

        # Add logo
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.', 'assets', 'logo.png')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            title_bar_layout.addWidget(logo_label)
        else:
            print(f"Logo not found at {logo_path}")

        # Add title
        title_label = QLabel("WencoClear")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_bar_layout.addWidget(title_label)

        main_layout.addLayout(title_bar_layout)

        # Main buttons layout
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(20)

        btn_data_checkup = QPushButton('Data Checkup')
        btn_configure = QPushButton('Configure')
        btn_timesheets = QPushButton('Timesheets')

        btn_data_checkup.setIcon(QIcon.fromTheme("view-refresh"))
        btn_configure.setIcon(QIcon.fromTheme("configure"))
        btn_timesheets.setIcon(QIcon.fromTheme("document-save"))

        btn_data_checkup.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        btn_configure.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        btn_timesheets.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")

        btn_data_checkup.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        btn_configure.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        btn_timesheets.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        buttons_layout.addWidget(btn_data_checkup)
        buttons_layout.addWidget(btn_configure)
        buttons_layout.addWidget(btn_timesheets)

        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()  # Add stretch to push buttons up

        self.setLayout(main_layout)
