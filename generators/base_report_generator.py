from extractors.base_extractor import ReportExtractor

class ReportGenerator:
    def __init__(self):
        self.config = None
        self.stores = None
        self.app = None
        self.extractor = ReportExtractor()

    def generate_ss_reports(self, missing_dates_per_store):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def generate_timesheet_reports(self, missing_weeks):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def generate_tech_reports(self, missing_weeks_per_store):
        raise NotImplementedError("This method should be implemented by subclasses.")

