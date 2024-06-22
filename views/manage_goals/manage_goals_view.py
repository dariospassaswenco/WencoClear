from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTabWidget
from .kpi_shop_goals_tab import create_kpi_shop_goals_tab
from .view_weekly_revenue_goals_tab import ViewWeeklyRevenueGoalsTab
from .upload_weekly_revenue_goals_tab import UploadWeeklyRevenueGoalsTab

class ManageGoalsView(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        btn_home = QPushButton('Home')
        btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(btn_home)

        layout.addWidget(QLabel("Manage your sales and store KPI goals here"))

        # Tab widget
        self.tab_widget = QTabWidget()
        self.kpi_shop_goals_tab = create_kpi_shop_goals_tab(self)
        self.view_weekly_revenue_goals_tab = ViewWeeklyRevenueGoalsTab()
        self.upload_weekly_revenue_goals_tab = UploadWeeklyRevenueGoalsTab()

        self.tab_widget.addTab(self.kpi_shop_goals_tab, "KPI Shop Goals")
        self.tab_widget.addTab(self.view_weekly_revenue_goals_tab, "View Weekly Revenue Goals")
        self.tab_widget.addTab(self.upload_weekly_revenue_goals_tab, "Upload Weekly Revenue Goals")

        layout.addWidget(self.tab_widget)

        self.setLayout(layout)
