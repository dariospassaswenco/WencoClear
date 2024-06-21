from .display_functions import display_sales_summary_data, display_tech_data, display_timesheet_data, display_all_data, display_sales_by_category_data

def run_data_checkup(view, report_type):
    start_date = view.start_date_edit.date().toPyDate()
    end_date = view.end_date_edit.date().toPyDate()

    if report_type == "Sales Summary":
        display_sales_summary_data(view, start_date, end_date, view.sales_summary_results_table)
    elif report_type == "Tech Data":
        display_tech_data(view, start_date, end_date, view.tech_results_table)
    elif report_type == "Timesheet Data":
        display_timesheet_data(view, start_date, end_date, view.timesheet_results_table)
    elif report_type == "Sales By Category":
        display_sales_by_category_data(view, start_date, end_date, view.sales_by_category_results_table)
    elif report_type == "All Reports":
        display_all_data(view, start_date, end_date, view.all_reports_results_table)
