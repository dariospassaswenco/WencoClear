from dataclasses import dataclass

@dataclass
class BigoSalesSummary:
    wenco_id: int
    date: str
    car_count: int
    tire_count: float
    alignment_count: float
    nitrogen_count: float
    parts_revenue: float
    billed_labor_quantity: float
    billed_labor_revenue: float
    supplies: int
    total_revenue_w_supplies: float
    gross_profit_no_supplies: int
    gross_profit_w_supplies: float

@dataclass
class BigoTechSummary:
    wenco_id: int
    employee_id: int
    first_name: str
    last_name: str
    start_date: str
    end_date: str
    car_count: int
    tire_count: float
    alignment_count: float
    nitrogen_count: float
    parts_revenue: float
    billed_labor_quantity: float
    billed_labor_revenue: float
    total_revenue: float
    gross_profit: float

@dataclass
class BigoTimesheet:
    wenco_id: int
    employee_id: int
    first_name: str
    last_name: str
    date: str
    hours: float

@dataclass
class MidasSalesSummary:
    wenco_id: int
    date: str
    car_count: int
    parts_revenue: float
    labor_revenue: float
    tire_revenue: float
    supplies_revenue: float
    parts_cost: float
    labor_cost: float
    tire_cost: float
    total_revenue_w_supplies: float
    parts_gp: float
    labor_gp: float
    tire_gp: float
    gp_w_supplies: float

@dataclass
class MidasTechSummary:
    wenco_id: int
    employee_id: int
    first_name: str
    last_name: str
    start_date: str
    end_date: str
    store_number: int
    time: float
    labor_sales: float
    part_sales: float
    no_of_ros: int
    total_sales: float

@dataclass
class MidasTimesheet:
    wenco_id: int
    employee_id: int
    first_name: str
    last_name: str
    date: str
    hours: float
