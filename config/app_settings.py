import os
import configparser
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

# Load .env file
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))
print(f"Loading .env file from: {env_path}")

# Load config.ini file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

# Get settings from config.ini file
CLEAR_DATABASE_PATH = config['DEFAULT']['databasepath']

# Check if the database file exists
if os.path.exists(CLEAR_DATABASE_PATH):
    print(f"The database file {CLEAR_DATABASE_PATH} exists.")
else:
    print(f"The database file {CLEAR_DATABASE_PATH} does not exist.")

# App Executables
ROWRITER_EXECUTABLE = config['EXECUTABLES']['ROWriter']
NAVEX_EXECUTABLE = config['EXECUTABLES']['Navex']

# Credentials
RO_PASSWORD=os.getenv('RO_PASSWORD')
NAVEX_USERNAME=os.getenv('NAVEX_USERNAME')
NAVEX_PASSWORD=os.getenv('NAVEX_PASSWORD')

# Outputs Folder
OUTPUTS = config['OUTPUTS']['processingoutputs']
EXCELEXPORT = config['OUTPUTS']['excelexportpath']

# Storage directories
MIDAS_SALES_SUMMARIES_DIR = config['Midas']['salessummariesdir']
MIDAS_TIMESHEETS_DIR = config['Midas']['timesheetsdir']
MIDAS_TECH_REPORTS_DIR = config['Midas']['techreportsdir']

BIGO_SALES_SUMMARIES_DIR = config['Bigo']['salessummariesdir']
BIGO_TIMESHEETS_DIR = config['Bigo']['timesheetsdir']
BIGO_TECH_REPORTS_DIR = config['Bigo']['techreportsdir']

# ------------- File names -------------
MIDAS_FILENAME_PATTERN = 'mid_{store_number}_{report_type}_{date}.pdf'
BIGO_FILENAME_PATTERN = 'BGO_{store_number}_{report_type}_{date}.XLS'

# ------------- Database -------------
MIDAS_SS_TABLE = "midas_sales_summary"
MIDAS_TIMESHEET_TABLE = "midas_timesheet"
MIDAS_TECH_TABLE = "midas_tech_summary"

BIGO_SS_TABLE = "bigo_sales_summary"
BIGO_TIMESHEET_TABLE = "bigo_timesheet"
BIGO_TECH_TABLE = "bigo_tech_summary"

# Create a SQLAlchemy engine
ENGINE = create_engine(f'sqlite:///{CLEAR_DATABASE_PATH}')

# Fetch store numbers and address/pos_ctrl_id maps dynamically
def fetch_store_data():
    try:
        with ENGINE.connect() as conn:
            result = conn.execute(text('''
                SELECT s.wenco_id, s.address, s.pos_ctrl_id, st.type_name 
                FROM stores s
                JOIN store_types st ON s.type_id = st.type_id
            '''))
            midas_store_numbers = []
            bigo_store_numbers = []
            midas_address_map = {}
            bigo_address_map = {}
            midas_pos_ctrl_map = {}
            bigo_pos_ctrl_map = {}
            for row in result:
                wenco_id, address, pos_ctrl_id, type_name = row
                if type_name == 'Midas':
                    midas_store_numbers.append(wenco_id)
                    midas_address_map[address] = wenco_id
                    midas_pos_ctrl_map[pos_ctrl_id] = wenco_id
                elif type_name == 'Bigo':
                    bigo_store_numbers.append(wenco_id)
                    bigo_address_map[address] = wenco_id
                    bigo_pos_ctrl_map[pos_ctrl_id] = wenco_id
            return midas_store_numbers, bigo_store_numbers, midas_address_map, bigo_address_map, midas_pos_ctrl_map, bigo_pos_ctrl_map
    except Exception as e:
        print(f"Error fetching store data: {e}")
        return [], [], {}, {}, {}, {}

def get_closed_days():
    try:
        query = "SELECT date FROM closed_days"
        closed_days_df = pd.read_sql_query(query, ENGINE)
        closed_days = closed_days_df['date'].tolist()
        return closed_days
    except Exception as e:
        print(f"Error fetching closed days: {e}")
        return []

MIDAS_STORE_NUMBERS, BIGO_STORE_NUMBERS, MIDAS_ADDRESS_MAP, BIGO_ADDRESS_MAP, MIDAS_POS_CTRL_MAP, BIGO_POS_CTRL_MAP = fetch_store_data()
CLOSED_DAYS = get_closed_days()

print(MIDAS_STORE_NUMBERS)
print(BIGO_STORE_NUMBERS)
print(MIDAS_ADDRESS_MAP)
print(BIGO_ADDRESS_MAP)
print(MIDAS_POS_CTRL_MAP)
print(BIGO_POS_CTRL_MAP)
print(CLOSED_DAYS)

print(RO_PASSWORD)
print(NAVEX_USERNAME)
print(NAVEX_PASSWORD)
