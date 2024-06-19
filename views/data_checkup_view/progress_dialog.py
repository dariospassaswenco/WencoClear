# views/progress_dialog.py
from PyQt5.QtWidgets import QProgressDialog, QVBoxLayout, QLabel

class ProgressDialog(QProgressDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Progress")
        self.setLabelText("Processing...")
        self.setCancelButtonText("Cancel")
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.log_label = QLabel("")
        layout = QVBoxLayout()
        layout.addWidget(self.log_label)
        self.setLayout(layout)

    def log_message(self, message):
        self.log_label.setText(message)
