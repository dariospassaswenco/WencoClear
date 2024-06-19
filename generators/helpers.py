from generators.midas_report_generator import MidasReportGenerator
from generators.bigo_report_generator import BigoReportGenerator

def generate_midas_reports(ss_midas, tech_midas, timesheet_midas, log_dialog):
    midas_generator = MidasReportGenerator()
    midas_generator.prepare_pos()

    # Generate Sales Summary Reports
    if ss_midas:
        for store, dates in ss_midas.items():
            for date in dates:
                log_dialog.log_message(f"Generating Sales Summary Report for store {store} on date {date}")
                midas_generator.generate_ss_reports({store: [date]})

    # Generate Tech Reports
    if tech_midas:
        for store, dates in tech_midas.items():
            for date in dates:
                log_dialog.log_message(f"Generating Tech Report for store {store} on date {date}")
                midas_generator.generate_tech_reports({store: [date]})

    # Generate Timesheet Reports
    if timesheet_midas:
        for store, date_range in timesheet_midas.items():
            log_dialog.log_message(f"Generating Timesheet Report for store {store} from {date_range[0]} to {date_range[1]}")
            midas_generator.generate_timesheet_reports({store: [date_range]})

    midas_generator.actions.app.kill()  # Close POS
    log_dialog.log_message("Midas Reports Generated.")

def generate_bigo_reports(ss_bigo, tech_bigo, timesheet_bigo, log_dialog):
    bigo_generator = BigoReportGenerator()
    bigo_generator.prepare_pos()

    # Generate Sales Summary Reports
    if ss_bigo:
        for store, dates in ss_bigo.items():
            for date in dates:
                log_dialog.log_message(f"Generating Sales Summary Report for store {store} on date {date}")
                bigo_generator.generate_ss_reports({store: [date]})

    # Generate Tech Reports
    if tech_bigo:
        for store, dates in tech_bigo.items():
            for date in dates:
                log_dialog.log_message(f"Generating Tech Report for store {store} on date {date}")
                bigo_generator.generate_tech_reports({store: [date]})

    # Generate Timesheet Reports
    if timesheet_bigo:
        for store, date_range in timesheet_bigo.items():
            log_dialog.log_message(f"Generating Timesheet Report for store {store} from {date_range[0]} to {date_range[1]}")
            bigo_generator.generate_timesheet_reports({store: [date_range]})

    bigo_generator.actions.app.kill()  # Close POS
    log_dialog.log_message("Bigo Reports Generated.")