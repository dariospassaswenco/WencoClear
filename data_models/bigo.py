from dataclasses import dataclass

@dataclass
class BigoSalesSummary:
    wenco_id: int = 0
    date: str = ""
    car_count: int = 0
    tire_count: float = 0.0
    alignment_count: float = 0.0
    nitrogen_count: float = 0.0
    parts_revenue: float = 0.0
    labor_quantity: float = 0.0
    labor_revenue: float = 0.0
    supplies_revenue: int = 0
    total_revenue_w_supplies: float = 0.0
    gross_profit_no_supplies: int = 0
    gross_profit_w_supplies: float = 0.0

@dataclass
class BigoTimesheet:
    wenco_id: int = 0
    date: str = ""
    date_entered: str = ""
    first_name: str = ""
    last_name: str = ""
    hours: float = 0.0

@dataclass
class BigoTechSummary:
    first_name: str = ""
    last_name: str = ""
    date: str = ""
    car_count: int = 0
    tire_count: float = 0.0
    alignment_count: float = 0.0
    nitrogen_count: float = 0.0
    parts_revenue: float = 0.0
    tech_hours_flagged: float = 0.0
    labor_revenue: float = 0.0
    total_revenue: float = 0.0
    gross_profit: float = 0.0

@dataclass
class BigoSalesByCategory:
    wenco_id: int = 0
    date: str = ""
    sales_category: str = ""
    parts_quantity: float = 0.0
    parts_sales: float = 0.0
    labor_quantity: float = 0.0
    labor_sales: float = 0.0
    discounts_quantity: float = 0.0
    discounts_amount: float = 0.0
    ext_cost: float = 0.0
    gross_profit_percent: float = 0.0
    gross_profit: float = 0.0
    total_sales: float = 0.0



