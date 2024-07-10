#extractors/base_extractor
import os
import shutil
from config.app_settings import (
    CLEAR_DATABASE_PATH, OUTPUTS,
)
from .factory_extractor import get_extractor
from sqlalchemy import create_engine

class ReportExtractor:
    def __init__(self):
        self.database_path = CLEAR_DATABASE_PATH
        self.folder_path = OUTPUTS
        self.file_name_format = None
        self.table_name = None
        self.destination_directory = None

    def set_report_attributes(self, report_type):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def extract_reports(self):
        file_list = os.listdir(self.folder_path)
        for file_name in file_list:
            extractor = get_extractor(file_name)
            if extractor:
                report_type = extractor.identify_report_type(file_name)
                if report_type:
                    print(f"Processing: {file_name}")
                    extractor.set_report_attributes(report_type)
                    df = extractor.process_file(os.path.join(self.folder_path, file_name))
                    print(df)
                    if df is not None and not df.empty:
                        cleaned_df = extractor.clean_data_frame(df)
                        extractor.delete_existing_records(cleaned_df, report_type)
                        extractor.store_data_frame(cleaned_df)
                        # extractor.move_processed_file(file_name)
                else:
                    print(f"{file_name} Not Valid!")
            else:
                print(f"Extractor not found for file: {file_name}")

    def identify_report_type(self, file_name):
        file_name = file_name.lower()
        if "_ss_" in file_name:
            return 'ss'
        elif "_ts_" in file_name:
            return 'timesheet'
        elif "_tech_" in file_name:
            return 'tech'
        elif "_sba_" in file_name:
            return 'sba'
        return None

    def clean_data_frame(self, df):
        cleaned_df = df.drop_duplicates()
        return cleaned_df

    def store_data_frame(self, df):
        engine = create_engine(f'sqlite:///{self.database_path}')
        df.to_sql(self.table_name, engine, if_exists='append', index=False)
        print("Dataframe stored")

    def move_processed_file(self, file_name):
        source_path = os.path.join(self.folder_path, file_name)
        destination_path = os.path.join(self.destination_directory, file_name)
        shutil.move(source_path, destination_path)
        print(f"Moved: {file_name} to {self.destination_directory}")

    def delete_existing_records(self, df, report_type):
        raise NotImplementedError("This method should be implemented by subclasses.")
