from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTabWidget, QTextEdit
from .closed_days_tab import create_closed_days_tab

class ConfigureView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        btn_home = QPushButton('Home')
        btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(btn_home)

        layout.addWidget(QLabel("Configure your settings here"))

        # Tab widget
        self.tab_widget = QTabWidget()
        self.closed_days_tab = create_closed_days_tab(self)

        self.tab_widget.addTab(self.closed_days_tab, "Closed Days")

        layout.addWidget(self.tab_widget)

        # Log text edit
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFixedHeight(100)
        layout.addWidget(self.log_text)

        self.setLayout(layout)

    def append_log(self, message):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())
