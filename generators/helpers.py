from datetime import datetime, timedelta
from generators.midas_report_generator import MidasReportGenerator
from generators.bigo_report_generator import BigoReportGenerator


def break_into_payroll_periods(timesheet_bigo):
    def next_sunday(date):
        days_ahead = 6 - date.weekday()
        return date + timedelta(days=days_ahead + 1)

    new_timesheet_bigo = []

    for start_date_str, end_date_str in timesheet_bigo:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        current_start = start_date
        while current_start <= end_date:
            current_end = next_sunday(current_start)
            if current_end > end_date:
                current_end = end_date + timedelta(days=1)  # Include the end date
            if current_start.weekday() != 6:  # Skip Sundays
                new_timesheet_bigo.append((current_start.strftime('%Y-%m-%d'), (current_end - timedelta(days=1)).strftime('%Y-%m-%d')))
            current_start = current_end

    return new_timesheet_bigo

def generate_midas_reports(ss_midas, tech_midas, timesheet_midas, sba_midas, stop_requested, progress_callback):
    midas_generator = MidasReportGenerator()
    progress_callback("Preparing Midas POS...")
    midas_generator.prepare_pos()

    try:
        # Generate Sales Summary Reports
        if ss_midas:
            for store, dates in ss_midas.items():
                for date in dates:
                    if stop_requested():
                        progress_callback("Fetch canceled.")
                        return
                    progress_callback(f"Generating Sales Summary Report for store {store} on date {date}")
            midas_generator.generate_ss_reports(ss_midas)

        # Generate Tech Reports
        if tech_midas:
            for store, dates in tech_midas.items():
                for date in dates:
                    if stop_requested():
                        progress_callback("Fetch canceled.")
                        return
                    progress_callback(f"Generating Tech Report for store {store} on date {date}")
            midas_generator.generate_tech_reports(tech_midas)

        # Generate Timesheet Reports
        if timesheet_midas:
            for store, date_ranges in timesheet_midas.items():
                for date_range in date_ranges:
                    if stop_requested():
                        progress_callback("Fetch canceled.")
                        return
                    progress_callback(f"Generating Timesheet Report for store {store} from {date_range[0]} to {date_range[1]}")
            midas_generator.generate_timesheet_reports(timesheet_midas)

        if sba_midas:
            for store, dates in ss_midas.items():
                for date in dates:
                    if stop_requested():
                        progress_callback("Fetch canceled.")
                        return
                    progress_callback(f"Generating Sales By Category Report for store {store} on date {date}")
            midas_generator.generate_sales_by_category_reports(sba_midas)

    except Exception as e:
        progress_callback(f"Error generating Midas reports: {e}. Retrying...")
        midas_generator.restart_pos()
        generate_midas_reports(ss_midas, tech_midas, timesheet_midas, sba_midas, stop_requested, progress_callback)

    midas_generator.actions.app.kill()  # Close POS
    progress_callback("Midas Reports Generated.")

def generate_bigo_reports(ss_bigo, tech_bigo, timesheet_bigo, sbc_bigo, stop_requested, progress_callback):
    bigo_generator = BigoReportGenerator()
    progress_callback("Preparing Bigo POS...")
    bigo_generator.prepare_pos()

    if timesheet_bigo:
        timesheet_bigo = break_into_payroll_periods(timesheet_bigo)

    try:
        # Generate Sales Summary Reports
        if ss_bigo:
            for store, dates in ss_bigo.items():
                for date in dates:
                    if stop_requested():
                        progress_callback("Fetch canceled.")
                        return
                    progress_callback(f"Generating Sales Summary Report for store {store} on date {date}")
            bigo_generator.generate_ss_reports(ss_bigo)

        # Generate Tech Reports
        if tech_bigo:
            for date in tech_bigo:
                if stop_requested():
                    progress_callback("Fetch canceled.")
                    return
                progress_callback(f"Generating Tech Report for date {date}")
            bigo_generator.generate_tech_reports(tech_bigo)

        # Generate Timesheet Reports
        if timesheet_bigo:
            for date_range in timesheet_bigo:
                if stop_requested():
                    progress_callback("Fetch canceled.")
                    return
                progress_callback(f"Generating Timesheet Report from {date_range[0]} to {date_range[1]}")
            bigo_generator.generate_timesheet_reports(timesheet_bigo)

        if sbc_bigo:
            for store, dates in sbc_bigo.items():
                for date in dates:
                    if stop_requested():
                        progress_callback("Fetch canceled.")
                        return
                    progress_callback(f"Generating Sales Summary Report BETA SBC for store {store} on date {date}")
            bigo_generator.generate_sbc_reports(sbc_bigo)

    except Exception as e:
        progress_callback(f"Error generating Bigo reports: {e}. Retrying...")
        bigo_generator.restart_pos()
        generate_bigo_reports(ss_bigo, tech_bigo, timesheet_bigo, sbc_bigo, stop_requested, progress_callback)

    bigo_generator.actions.app.kill()  # Close POS
    progress_callback("Bigo Reports Generated.")

# Test the break_into_payroll_periods function
# Test the break_into_payroll_periods function
if __name__ == "__main__":
    test_timesheet_bigo = [
        ('2024-06-09', '2024-06-20'),  # spans multiple periods
        ('2024-06-05', '2024-06-06'),  # within a single period
        ('2024-06-17', '2024-06-20'),  # spans multiple periods
    ]

    broken_timesheet_bigo = break_into_payroll_periods(test_timesheet_bigo)
    for start_date, end_date in broken_timesheet_bigo:
        print(f"From {start_date} to {end_date}")
