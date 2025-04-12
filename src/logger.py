"""
The logger.py file in an ML Ops project is typically used to configure logging for 
tracking and debugging different stages of the ML pipeline, such as data processing, 
model training, and deployment. Instead of using print statements, logging provides a 
structured and configurable way to capture important runtime information.
"""

import logging # used for logging purpose
import os 
from datetime import datetime

# create logs dir
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok= True)
# Now we created the folder for the logs directory

# Now we have to create log files for particular date in the logs dir
# This will be path file name
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime("%Y-%m-%d")}.log")

# Configuration of logging
# param - 1 - filename
#       -2 - format(what time it is created, level name, message)level - info, warning, error
#       when we set level to logging.info() only info and levels above it will be shown, all other levels will not be shown
#    -3 message
logging.basicConfig(
    filename= LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def get_logger(name):
    logger = logging.getLogger(name)
    # This will create logging with the given name by the user
    logger.setLevel(logging.INFO)
    return logger
