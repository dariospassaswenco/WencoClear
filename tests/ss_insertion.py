# main.py
from data_models.midas import MidasSalesSummary
from data_models.bigo import BigoSalesSummary
from database.insert_midas import insert_midas_sales_summary
from database.insert_bigo import insert_bigo_sales_summary

# Example Midas data
midas_data = MidasSalesSummary(
    wenco_id=2,
    date="2024-01-01",
    car_count=50,
    parts_revenue=5000.0,
    labor_revenue=3000.0,
    tire_revenue=2000.0,
    supplies_revenue=1000.0,
    parts_cost=2500.0,
    labor_cost=1500.0,
    tire_cost=1000.0,
    total_revenue_w_supplies=11000.0,
    parts_gp=2500.0,
    labor_gp=1500.0,
    tire_gp=1000.0,
    gp_w_supplies=5000.0
)

# Example Bigo data
bigo_data = BigoSalesSummary(
    wenco_id=14,
    date="2024-01-01",
    car_count=60,
    tire_count=30,
    alignment_count=20,
    nitrogen_count=10,
    parts_revenue=6000.0,
    labor_quantity=40.0,
    labor_revenue=4000.0,
    supplies_revenue=2000.0,
    total_revenue_w_supplies=12000.0,
    gross_profit_no_supplies=7000.0,
    gross_profit_w_supplies=9000.0
)

# Insert Midas data
insert_midas_sales_summary(midas_data)

# Insert Bigo data
insert_bigo_sales_summary(bigo_data)
