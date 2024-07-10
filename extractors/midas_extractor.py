#extractors/midas_extractor
from .base_extractor import ReportExtractor
from .midas_sales_summary_extractor import MidasSalesSummaryExtractor
from .midas_tech_extractor import MidasTechExtractor
from .midas_timesheet_extractor import MidasTimesheetExtractor
from .midas_sales_by_category_extractor import MidasSalesByCategoryExtractor
from config.app_settings import (
    MIDAS_SS_TABLE,
    MIDAS_TIMESHEET_TABLE,
    MIDAS_TECH_TABLE,
    MIDAS_SBA_TABLE,
    MIDAS_SALES_SUMMARIES_DIR,
    MIDAS_TECH_REPORTS_DIR,
    MIDAS_TIMESHEETS_DIR,
    MIDAS_SBA_REPORTS_DIR
)


class MidasExtractor(ReportExtractor):
    def set_report_attributes(self, report_type):
        report_type = report_type.lower()
        if report_type == 'ss':
            self.table_name = MIDAS_SS_TABLE
            self.destination_directory = MIDAS_SALES_SUMMARIES_DIR
        elif report_type == 'timesheet':
            self.table_name = MIDAS_TIMESHEET_TABLE
            self.destination_directory = MIDAS_TIMESHEETS_DIR
        elif report_type == 'tech':
            self.table_name = MIDAS_TECH_TABLE
            self.destination_directory = MIDAS_TECH_REPORTS_DIR
        elif report_type == 'sba':
            self.table_name = MIDAS_SBA_TABLE
            self.destination_directory = MIDAS_SBA_REPORTS_DIR
        else:
            raise ValueError(f"Unsupported report type: {report_type}")

    def process_file(self, file_path):
        report_type = self.identify_report_type(file_path)
        if report_type == 'ss':
            return MidasSalesSummaryExtractor.extract_ss_data(file_path)
        elif report_type == 'timesheet':
            return MidasTimesheetExtractor.extract_timesheet_data(file_path)
        elif report_type == 'tech':
            return MidasTechExtractor.extract_tech_data(file_path)
        elif report_type == 'sba':
            return MidasSalesByCategoryExtractor.extract_sales_by_category_data(file_path)
        else:
            print(f"Unknown report type for file: {file_path}")
            return None

    def delete_existing_records(self, df, report_type):
        if report_type == 'ss':
            MidasSalesSummaryExtractor.delete_existing_records(df)
        elif report_type == 'timesheet':
            MidasTimesheetExtractor.delete_existing_records(df)
        elif report_type == 'tech':
            MidasTechExtractor.delete_existing_records(df)
