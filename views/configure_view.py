from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


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

        self.setLayout(layout)
