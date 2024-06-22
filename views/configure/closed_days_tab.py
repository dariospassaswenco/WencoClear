from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import pandas as pd
from database.closed_days import get_all_closed_days, update_closed_days  # Replace 'your_query_module' with the actual module name

def create_closed_days_tab(configure_view):
    widget = QWidget()
    layout = QVBoxLayout()

    # Label and instructions
    layout.addWidget(QLabel("Manage Closed Days"))

    # Table to display closed days
    closed_days_table = QTableWidget()
    closed_days_table.setColumnCount(2)
    closed_days_table.setHorizontalHeaderLabels(["Date", "Reason"])
    layout.addWidget(closed_days_table)

    # Load data into the table
    load_closed_days_data(closed_days_table)

    # Button to add a new closed day
    add_closed_day_button = QPushButton("Add Closed Day")
    add_closed_day_button.clicked.connect(lambda: add_closed_day(closed_days_table))
    layout.addWidget(add_closed_day_button)

    # Button to save changes
    save_changes_button = QPushButton("Save Changes")
    save_changes_button.clicked.connect(lambda: save_closed_days(closed_days_table, configure_view))
    layout.addWidget(save_changes_button)

    widget.setLayout(layout)
    return widget

def load_closed_days_data(closed_days_table):
    df = get_all_closed_days()
    closed_days_table.setRowCount(len(df))

    for row_index, row in df.iterrows():
        closed_days_table.setItem(row_index, 0, QTableWidgetItem(row['date']))
        closed_days_table.setItem(row_index, 1, QTableWidgetItem(row['reason']))

def add_closed_day(closed_days_table):
    row_position = closed_days_table.rowCount()
    closed_days_table.insertRow(row_position)
    closed_days_table.setItem(row_position, 0, QTableWidgetItem("YYYY-MM-DD"))
    closed_days_table.setItem(row_position, 1, QTableWidgetItem("Reason"))

def save_closed_days(closed_days_table, configure_view):
    rows = closed_days_table.rowCount()
    cols = closed_days_table.columnCount()

    data = []
    for row in range(rows):
        row_data = []
        for col in range(cols):
            item = closed_days_table.item(row, col)
            row_data.append(item.text() if item else "")
        data.append(row_data)

    df = pd.DataFrame(data, columns=["date", "reason"])
    update_closed_days(df)
    configure_view.append_log("Closed days updated successfully.")
