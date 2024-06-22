from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QTextEdit
import pandas as pd
from database.goals import get_kpi_goals_by_shop, update_kpi_goals_by_shop

def create_kpi_shop_goals_tab(manage_goals_view):
    widget = QWidget()
    layout = QVBoxLayout()

    # Label and instructions
    layout.addWidget(QLabel("Manage KPI Shop Goals"))

    # Table to display KPI goals
    kpi_goals_table = QTableWidget()
    kpi_goals_table.setColumnCount(9)
    kpi_goals_table.setHorizontalHeaderLabels([
        "Wenco ID", "Avg Cars/Day", "Avg Repair Order", "Gross Profit Margin",
        "Tech Efficiency", "Tech OT/Vehicle", "Alignments/Day",
        "Tires/Day", "Nitrogen/Tire"
    ])
    layout.addWidget(kpi_goals_table)

    # Load data into the table
    load_kpi_goals_data(kpi_goals_table)

    # Buttons
    button_layout = QHBoxLayout()

    # Save changes button
    save_changes_button = QPushButton("Save Changes")
    save_changes_button.clicked.connect(lambda: save_kpi_goals(kpi_goals_table, widget))
    button_layout.addWidget(save_changes_button)

    # Refresh button
    refresh_button = QPushButton("Refresh")
    refresh_button.clicked.connect(lambda: refresh_kpi_goals(kpi_goals_table, widget))
    button_layout.addWidget(refresh_button)

    layout.addLayout(button_layout)

    # Log text edit
    log_text = QTextEdit()
    log_text.setReadOnly(True)
    log_text.setFixedHeight(100)
    layout.addWidget(log_text)

    widget.setLayout(layout)
    widget.log_text = log_text  # Attach the log_text to the widget for later use
    return widget

def load_kpi_goals_data(kpi_goals_table):
    df = get_kpi_goals_by_shop()
    kpi_goals_table.setRowCount(len(df))

    for row_index, row in df.iterrows():
        for col_index, value in enumerate(row):
            kpi_goals_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

def save_kpi_goals(kpi_goals_table, widget):
    rows = kpi_goals_table.rowCount()
    cols = kpi_goals_table.columnCount()

    data = []
    for row in range(rows):
        row_data = []
        for col in range(cols):
            item = kpi_goals_table.item(row, col)
            row_data.append(item.text() if item else "")
        data.append(row_data)

    df = pd.DataFrame(data, columns=[
        "wenco_id", "avg_cars_per_day_goal", "average_repair_order_goal", "gross_profit_margin_goal",
        "tech_efficiency_goal", "tech_ot_per_vehicle_goal", "alignments_per_day_goal",
        "tires_per_day_goal", "nitrogen_per_tire_goal"
    ])
    update_kpi_goals_by_shop(df)
    append_log(widget, "KPI goals updated successfully.")
    refresh_kpi_goals(kpi_goals_table, widget)

def refresh_kpi_goals(kpi_goals_table, widget):
    kpi_goals_table.clearContents()
    load_kpi_goals_data(kpi_goals_table)
    append_log(widget, "KPI goals data refreshed.")

def append_log(widget, message):
    widget.log_text.append(message)
    widget.log_text.verticalScrollBar().setValue(widget.log_text.verticalScrollBar().maximum())
