# config/settings.py
import os
from dotenv import load_dotenv
import configparser

# Load .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Load config.ini file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'crystal_config.ini'))


# Get settings from .env file
OLD_DATABASE_PATH = config['DEFAULT']['OldDatabasePath']

# Get settings from config.ini file
CLEAR_DATABASE_PATH = config['DEFAULT']['ClearDatabasePath']
