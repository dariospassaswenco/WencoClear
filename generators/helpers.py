from datetime import datetime
from generators.midas_report_generator import MidasReportGenerator
from generators.bigo_report_generator import BigoReportGenerator
from database.ss_data import get_missing_ss_dates
from database.tech_data import get_missing_midas_tech_dates, get_missing_bigo_tech_dates
from database.timesheet_data import get_missing_timesheet_dates

def generate_midas_reports(ss_midas, tech_midas, timesheet_midas):
    midas_generator = MidasReportGenerator()
    midas_generator.prepare_pos()

    try:
        # Generate Sales Summary Reports
        if ss_midas:
            for store, dates in ss_midas.items():
                for date in dates:
                    print(f"Generating Sales Summary Report for store {store} on date {date}")
            midas_generator.generate_ss_reports(ss_midas)

        # Generate Tech Reports
        if tech_midas:
            for store, dates in tech_midas.items():
                for date in dates:
                    print(f"Generating Tech Report for store {store} on date {date}")
            midas_generator.generate_tech_reports(tech_midas)

        # Generate Timesheet Reports
        if timesheet_midas:
            for store, date_ranges in timesheet_midas.items():
                for date_range in date_ranges:
                    print(f"Generating Timesheet Report for store {store} from {date_range[0]} to {date_range[1]}")
            midas_generator.generate_timesheet_reports(timesheet_midas)
    except Exception as e:
        print(f"Error generating Midas reports: {e}. Retrying...")
        midas_generator.restart_pos()
        generate_midas_reports(ss_midas, tech_midas, timesheet_midas)

    midas_generator.actions.app.kill()  # Close POS
    print("Midas Reports Generated.")

def generate_bigo_reports(ss_bigo, tech_bigo, timesheet_bigo):
    bigo_generator = BigoReportGenerator()
    bigo_generator.prepare_pos()

    try:
        # Generate Sales Summary Reports
        if ss_bigo:
            for store, dates in ss_bigo.items():
                for date in dates:
                    print(f"Generating Sales Summary Report for store {store} on date {date}")
            bigo_generator.generate_ss_reports(ss_bigo)

        # Generate Tech Reports
        if tech_bigo:
            for date in tech_bigo:
                print(f"Generating Tech Report for date {date}")
            bigo_generator.generate_tech_reports(tech_bigo)

        # Generate Timesheet Reports
        if timesheet_bigo:
            for date_range in timesheet_bigo:
                print(f"Generating Timesheet Report from {date_range[0]} to {date_range[1]}")
            bigo_generator.generate_timesheet_reports(timesheet_bigo)
    except Exception as e:
        print(f"Error generating Bigo reports: {e}. Retrying...")
        bigo_generator.restart_pos()
        generate_bigo_reports(ss_bigo, tech_bigo, timesheet_bigo)

    bigo_generator.actions.app.kill()  # Close POS
    print("Bigo Reports Generated.")
