from dataclasses import dataclass

@dataclass
class MidasSalesSummary:
    wenco_id: int = 0
    date: str = ""
    car_count: int = 0
    parts_revenue: float = 0.0
    labor_revenue: float = 0.0
    tire_revenue: float = 0.0
    supplies_revenue: float = 0.0
    parts_cost: float = 0.0
    labor_cost: float = 0.0
    tire_cost: float = 0.0
    total_revenue_w_supplies: float = 0.0
    parts_gp: float = 0.0
    labor_gp: float = 0.0
    tire_gp: float = 0.0
    gp_w_supplies: float = 0.0

@dataclass
class MidasTimesheet:
    wenco_id: int = 0
    date: str = ""
    date_entered: str = ""
    first_name: str = ""
    last_name: str = ""
    hours: float = 0.0

@dataclass
class MidasTechSummary:
    wenco_id: int = 0
    first_name: str = ""
    last_name: str = ""
    date: str = ""
    tech_hours_flagged: float = 0.0
    labor_revenue: float = 0.0
    part_revenue: float = 0.0
    car_count: int = 0
    total_revenue: float = 0.0

