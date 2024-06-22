from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from database.goals import get_weekly_revenue_goals, transpose_weekly_revenue_goals

class ViewWeeklyRevenueGoalsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label and instructions
        layout.addWidget(QLabel("View Weekly Revenue Goals"))

        # Table to display weekly revenue goals
        self.weekly_revenue_goals_table = QTableWidget()
        layout.addWidget(self.weekly_revenue_goals_table)

        # Button to refresh data
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_weekly_revenue_goals_data)
        layout.addWidget(refresh_button)

        # Load data into the table
        self.load_weekly_revenue_goals_data()

        self.setLayout(layout)

    def load_weekly_revenue_goals_data(self):
        df = get_weekly_revenue_goals()
        df_transposed = transpose_weekly_revenue_goals(df)

        # Print the transposed DataFrame for debugging
        print("Transposed DataFrame:\n", df_transposed)

        self.weekly_revenue_goals_table.setRowCount(len(df_transposed))
        self.weekly_revenue_goals_table.setColumnCount(len(df_transposed.columns))

        self.weekly_revenue_goals_table.setHorizontalHeaderLabels(df_transposed.columns)
        self.weekly_revenue_goals_table.setVerticalHeaderLabels(df_transposed.index.astype(str))

        for row_index, row in enumerate(df_transposed.index):
            for col_index, col in enumerate(df_transposed.columns):
                value = df_transposed.at[row, col]
                item = QTableWidgetItem(str(value))
                self.weekly_revenue_goals_table.setItem(row_index, col_index, item)
                # Debugging output to ensure correct data setting
                print(f"Setting item at row {row_index}, col {col_index}: {value}")

        # Debugging output to check the table contents
        for row in range(self.weekly_revenue_goals_table.rowCount()):
            for col in range(self.weekly_revenue_goals_table.columnCount()):
                item = self.weekly_revenue_goals_table.item(row, col)
                if item is not None:
                    print(f"Table item at row {row}, col {col}: {item.text()}")

