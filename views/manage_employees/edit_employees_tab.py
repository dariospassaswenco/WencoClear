import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView, QPushButton, QApplication, QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt
from database.employees import get_store_types, get_positions, get_all_employees
from config.app_settings import CLEAR_DATABASE_PATH

class EditEmployeesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.df = None
        self.store_types = [''] + get_store_types()
        self.positions = [''] + get_positions()
        self.combo_boxes = {}  # Dictionary to store the combo boxes
        self.load_employee_data()

    def initUI(self):
        layout = QVBoxLayout()

        # Add refresh button
        btn_refresh = QPushButton('Refresh Data')
        btn_refresh.clicked.connect(self.refresh_data)
        layout.addWidget(btn_refresh)

        # Add table to display the employee data
        self.table_view = QTableWidget()
        layout.addWidget(self.table_view)

        # Add button to add a new employee
        btn_add = QPushButton('Add New Employee')
        btn_add.clicked.connect(self.add_employee)
        layout.addWidget(btn_add)

        # Add commit changes button
        btn_commit = QPushButton('Commit Changes')
        btn_commit.clicked.connect(self.commit_changes)
        layout.addWidget(btn_commit)

        # Add progress text box
        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        self.progress_text.setFixedHeight(150)
        layout.addWidget(self.progress_text)

        self.setLayout(layout)

    def load_employee_data(self):
        try:
            self.df = get_all_employees()
            self.df['wenco_id'] = self.df['wenco_id'].apply(lambda x: str(int(x)) if pd.notna(x) and x != '' else '')
            self.df.sort_values(by='last_name', inplace=True)
            self.display_employee_data(self.df)
        except Exception as e:
            self.progress_text.append(f"Error loading data: {e}")
            print(f"Error loading data: {e}")

    def display_employee_data(self, df):
        self.table_view.setRowCount(df.shape[0])
        self.table_view.setColumnCount(5)
        self.table_view.setHorizontalHeaderLabels(['First Name', 'Last Name', 'Store Type', 'Position Title', 'Wenco ID'])

        self.combo_boxes.clear()
        for i in range(df.shape[0]):
            self.table_view.setItem(i, 0, QTableWidgetItem(str(df.iloc[i, 0])))
            self.table_view.setItem(i, 1, QTableWidgetItem(str(df.iloc[i, 1])))
            wenco_id_item = QTableWidgetItem(df.iloc[i, 4])
            wenco_id_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self.table_view.setItem(i, 4, wenco_id_item)  # 'wenco_id' already converted to string

            store_type_combo = QComboBox()
            store_type_combo.addItems(self.store_types)
            store_type_combo.setCurrentText(str(df.iloc[i, 2]))
            self.table_view.setCellWidget(i, 2, store_type_combo)
            self.combo_boxes[(i, 2)] = store_type_combo

            position_combo = QComboBox()
            position_combo.addItems(self.positions)
            position_combo.setCurrentText(str(df.iloc[i, 3]))
            self.table_view.setCellWidget(i, 3, position_combo)
            self.combo_boxes[(i, 3)] = position_combo

        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def refresh_data(self):
        self.load_employee_data()
        self.progress_text.append("Data refreshed successfully.")

    def commit_changes(self):
        try:
            conn = sqlite3.connect(CLEAR_DATABASE_PATH)
            cursor = conn.cursor()

            # Iterate through the table and update each row in the database
            for row in range(self.table_view.rowCount()):
                first_name = self.table_view.item(row, 0).text()
                last_name = self.table_view.item(row, 1).text()
                wenco_id = self.table_view.item(row, 4).text()
                store_type_combo = self.combo_boxes.get((row, 2))
                position_combo = self.combo_boxes.get((row, 3))

                if store_type_combo and position_combo:
                    store_type = store_type_combo.currentText()
                    position_title = position_combo.currentText()

                    if store_type and position_title:
                        # Get type_id and position_id from their respective tables
                        type_id = cursor.execute("SELECT type_id FROM store_types WHERE type_name=?", (store_type,)).fetchone()[0]
                        position_id = cursor.execute("SELECT position_id FROM positions WHERE title=?", (position_title,)).fetchone()[0]

                        # Check if the employee exists in the database
                        cursor.execute("""
                            SELECT COUNT(*)
                            FROM employees
                            WHERE first_name=? AND last_name=?
                        """, (first_name, last_name))
                        employee_exists = cursor.fetchone()[0]

                        if employee_exists:
                            # Update the employee in the database
                            cursor.execute("""
                                UPDATE employees
                                SET type_id=?, position_id=?, wenco_id=?
                                WHERE first_name=? AND last_name=?
                            """, (type_id, position_id, wenco_id, first_name, last_name))
                        else:
                            # Insert the new employee into the database
                            cursor.execute("""
                                INSERT INTO employees (first_name, last_name, wenco_id, type_id, position_id)
                                VALUES (?, ?, ?, ?, ?)
                            """, (first_name, last_name, wenco_id, type_id, position_id))

            conn.commit()
            conn.close()
            self.progress_text.append("Changes committed successfully.")
            self.refresh_data()  # Reload data after committing changes
        except Exception as e:
            self.progress_text.append(f"Error committing changes: {e}")
            print(f"Error committing changes: {e}")

    def add_employee(self):
        row_position = 0  # Add the new employee to the top
        self.table_view.insertRow(row_position)

        # Create empty QTableWidgetItems for the new row
        self.table_view.setItem(row_position, 0, QTableWidgetItem(""))
        self.table_view.setItem(row_position, 1, QTableWidgetItem(""))
        self.table_view.setItem(row_position, 4, QTableWidgetItem(""))

        # Create combo boxes for the new row
        store_type_combo = QComboBox()
        store_type_combo.addItems(self.store_types)
        self.table_view.setCellWidget(row_position, 2, store_type_combo)
        self.combo_boxes[(row_position, 2)] = store_type_combo

        position_combo = QComboBox()
        position_combo.addItems(self.positions)
        self.table_view.setCellWidget(row_position, 3, position_combo)
        self.combo_boxes[(row_position, 3)] = position_combo

# Main application (for testing purposes)
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Create the main widget
    main_widget = EditEmployeesTab()

    # Show the main widget
    main_widget.show()

    # Execute the application
    sys.exit(app.exec_())
