import logging
import os
from datetime import datetime
from config.app_settings import LOGGING_DIR

# Specify the exact log directory
log_dir = LOGGING_DIR

# Create the logs directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Create a unique log file name with timestamp
log_file = os.path.join(log_dir, f'report_actions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # This will also print logs to console
    ]
)

# Create a logger for this module
logger = logging.getLogger(__name__)