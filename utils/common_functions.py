# Here we will be creating function to read the yaml file
# we will be using yaml file at multiple steps - 1. Data Ingestion, 2. Data Processing

import os
import pandas
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml
import pandas as pd

logger = get_logger(__name__)

def yaml_file_reader(yaml_file_path):
    # here we pass the yaml file path from paths.py where we have the config yaml file
    try:
        if not os.path.exists(yaml_file_path):
            raise FileNotFoundError(f"FIle is not found at the given path")

        with open(yaml_file_path, "r") as yaml_file:
            yaml_config_contents = yaml.safe_load(yaml_file)
            logger.info("Succesfully Read yaml config file")
            return yaml_config_contents
    except Exception as e:
        logger.error("Error while reading yaml file")
        raise CustomException("Failed to load yaml file", e)

# we will create a new function to load the data. For data preprocessing and model training we 
# have to load the data and also during model training we have to load the data

def load_data(file_path):
    try:
        logger.info(f"Loading the data from the path-{file_path}")
        return pd.read_csv(file_path)
    except Exception as e:
        logger.error("Error occured during loading of the data")
        raise CustomException(f"Failed to load the data. Error - {e}")
