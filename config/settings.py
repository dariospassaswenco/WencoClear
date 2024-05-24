import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH')

WENCO_EXCEL_REPORT_NAME = os.getenv('WENCO_REPORT_PATH')