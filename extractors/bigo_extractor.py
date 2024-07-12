from .base_extractor import ReportExtractor
from .bigo_sales_summary_extractor import BigoSalesSummaryExtractor
from .bigo_timesheet_extractor import BigoTimesheetExtractor
from .bigo_tech_extractor import BigoTechExtractor
from .bigo_sales_by_category_extractor import BigoSalesByCategoryExtractor
from config.app_settings import (
    BIGO_SS_TABLE,
    BIGO_TIMESHEET_TABLE,
    BIGO_TECH_TABLE,
    BIGO_SBA_TABLE,
    BIGO_SALES_SUMMARIES_DIR,
    BIGO_TIMESHEETS_DIR,
    BIGO_TECH_REPORTS_DIR,
    BIGO_SBA_REPORTS_DIR
)

class BigoExtractor(ReportExtractor):
    def set_report_attributes(self, report_type):
        report_type = report_type.lower()
        if report_type == 'ss':
            self.table_name = BIGO_SS_TABLE
            self.destination_directory = BIGO_SALES_SUMMARIES_DIR
        elif report_type == 'timesheet':
            self.table_name = BIGO_TIMESHEET_TABLE
            self.destination_directory = BIGO_TIMESHEETS_DIR
        elif report_type == 'tech':
            self.table_name = BIGO_TECH_TABLE
            self.destination_directory = BIGO_TECH_REPORTS_DIR
        elif report_type == 'sba':
            self.table_name = BIGO_SBA_TABLE
            self.destination_directory = BIGO_SBA_REPORTS_DIR
        else:
            raise ValueError(f"Unsupported report type: {report_type}")

    def process_file(self, file_path):
        report_type = self.identify_report_type(file_path)
        if report_type == 'ss':
            return BigoSalesSummaryExtractor.extract_ss_data(file_path)
        elif report_type == 'timesheet':
            return BigoTimesheetExtractor.extract_timesheet_data(file_path)
        elif report_type == 'tech':
            return BigoTechExtractor.extract_tech_data(file_path)
        elif report_type == 'sba':
            return BigoSalesByCategoryExtractor.extract_sbc_data(file_path)
        else:
            print(f"Unknown report type for file: {file_path}")
            return None

    def delete_existing_records(self, df, report_type):
        if report_type == 'ss':
            BigoSalesSummaryExtractor.delete_existing_records(df)
        elif report_type == 'timesheet':
            BigoTimesheetExtractor.delete_existing_records(df)
        elif report_type == 'tech':
            BigoTechExtractor.delete_existing_records(df)
