from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QTextEdit
)
import pandas as pd
from database.goals import update_weekly_revenue_goals

class UploadWeeklyRevenueGoalsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add button to upload excel file
        btn_upload = QPushButton('Upload Weekly Revenue Goals Excel File')
        btn_upload.clicked.connect(self.upload_file)
        layout.addWidget(btn_upload)

        # Add label to display the status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        # Add table to display the weekly revenue goals data
        self.weekly_revenue_goals_table = QTableWidget()
        layout.addWidget(self.weekly_revenue_goals_table)

        # Add button to confirm import to database
        self.btn_confirm = QPushButton('Confirm Import to Database')
        self.btn_confirm.setEnabled(False)
        self.btn_confirm.clicked.connect(self.start_import)
        layout.addWidget(self.btn_confirm)

        # Add progress text box
        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        self.progress_text.setFixedHeight(150)
        layout.addWidget(self.progress_text)

        self.setLayout(layout)

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Excel File", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options
        )
        if file_path:
            self.process_excel(file_path)

    def process_excel(self, file_path):
        try:
            # Read the Excel file
            df = pd.read_excel(file_path, index_col=0)

            # Convert dates to yyyy-mm-dd format
            df.columns = pd.to_datetime(df.columns).strftime('%Y-%m-%d')

            # Display the data in the table
            self.display_weekly_revenue_goals_data(df)

            # Transform the data into the required format for the database
            self.df_for_db = self.transform_for_database(df)

            # Enable the confirm button
            self.df = df
            self.btn_confirm.setEnabled(True)
            self.status_label.setText("Data loaded successfully. Please confirm to import to the database.")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")
            print(f"Error: {e}")

    def display_weekly_revenue_goals_data(self, df):
        self.weekly_revenue_goals_table.setRowCount(df.shape[0])
        self.weekly_revenue_goals_table.setColumnCount(df.shape[1])
        self.weekly_revenue_goals_table.setHorizontalHeaderLabels(df.columns)
        self.weekly_revenue_goals_table.setVerticalHeaderLabels(df.index.astype(str))

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.weekly_revenue_goals_table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

    def transform_for_database(self, df):
        df_reset = df.reset_index()
        df_reset.rename(columns={df_reset.columns[0]: 'wenco_id'}, inplace=True)

        # Convert the DataFrame from pivot format back to long format
        df_long = df_reset.melt(id_vars='wenco_id', var_name='week_end_date', value_name='revenue_goal')

        # Handle NaN values by replacing them with None
        df_long = df_long.where(pd.notnull(df_long), None)

        # Debug output: print the long format DataFrame
        print("Transformed DataFrame to be inserted:\n", df_long)

        return df_long

    def start_import(self):
        reply = QMessageBox.question(self, 'Confirm Import', 'This will overwrite existing revenue goals. Are you sure?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.import_data()
                self.append_progress("Weekly revenue goals updated successfully.")
                self.status_label.setText("Weekly revenue goals updated successfully.")
                self.btn_confirm.setEnabled(False)
            except Exception as e:
                self.append_progress(f"Error: {e}")
                print(f"Error: {e}")

    def import_data(self):
        update_weekly_revenue_goals(self.df_for_db)

    def append_progress(self, message):
        self.progress_text.append(message)
        self.progress_text.verticalScrollBar().setValue(self.progress_text.verticalScrollBar().maximum())
