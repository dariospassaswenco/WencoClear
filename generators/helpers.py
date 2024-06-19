from generators.midas_report_generator import MidasReportGenerator
from generators.bigo_report_generator import BigoReportGenerator

def generate_midas_reports(ss_midas, tech_midas, timesheet_midas):
    midas_generator = MidasReportGenerator()
    midas_generator.prepare_pos()

    # Generate Sales Summary Reports
    if ss_midas:
        for store, dates in ss_midas.items():
            for date in dates:
                print(f"Generating Sales Summary Report for store {store} on date {date}")
                midas_generator.generate_ss_reports({store: [date]})

    # Generate Tech Reports
    if tech_midas:
        for store, dates in tech_midas.items():
            for date in dates:
                print(f"Generating Tech Report for store {store} on date {date}")
                midas_generator.generate_tech_reports({store: [date]})

    # Generate Timesheet Reports
    if timesheet_midas:
        for store, date_ranges in timesheet_midas.items():
            for date_range in date_ranges:
                print(f"Generating Timesheet Report for store {store} from {date_range[0]} to {date_range[1]}")
                midas_generator.generate_timesheet_reports({store: [date_range]})

    midas_generator.actions.app.kill()  # Close POS
    print("Midas Reports Generated.")

def generate_bigo_reports(ss_bigo, tech_bigo, timesheet_bigo):
    bigo_generator = BigoReportGenerator()
    bigo_generator.prepare_pos()

    # Generate Sales Summary Reports
    if ss_bigo:
        for store, dates in ss_bigo.items():
            for date in dates:
                print(f"Generating Sales Summary Report for store {store} on date {date}")
                bigo_generator.generate_ss_reports({store: [date]})

    # Generate Tech Reports
    if tech_bigo:
        for date in tech_bigo:
            print(f"Generating Tech Report for date {date}")
            bigo_generator.generate_tech_reports([{date: [date]}])

    # Generate Timesheet Reports
    if timesheet_bigo:
        for date_range in timesheet_bigo:
            print(f"Generating Timesheet Report from {date_range[0]} to {date_range[1]}")
            bigo_generator.generate_timesheet_reports([date_range])

    bigo_generator.actions.app.kill()  # Close POS
    print("Bigo Reports Generated.")
