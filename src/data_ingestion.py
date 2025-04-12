import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common_functions import yaml_file_reader
from config.paths import *

logger = get_logger(__name__)

# here we do the data ingestion

class DataIngestion:
    # this will be the constructor methos
    def __init__(self, config):# here we pass the config file here -> this should be our config.yaml file
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]
        
        # we want to store our return data from DataIngestion to raw directory in artifacts folder
        os.makedirs(RAW_DIR, exist_ok = True)
        logger.info(f"Data ingestion started with bucket name - {self.bucket_name} and file name is {self.bucket_file_name}")

    # We need to create another method which downloads data from GCP
    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            #blob means file name
            blob = bucket.blob(self.bucket_file_name)

            # now we want the file to downloaded to raw_file_path
            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"Raw CSV file is downloaded to {RAW_FILE_PATH}")

        except Exception as e:
            logger.error("Error while downloading the csv file")
            raise CustomException("Failed to download the csv file", e)

    # another method to split the data
    def split_data(self):
        try:
            logger.info("Starting to split the data")
            data = pd.read_csv(RAW_FILE_PATH)

            train_data, test_data = train_test_split(data, test_size = 1-self.train_ratio, random_state = 99)

            # convert them to csv format
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            logger.info(f"Train data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Test data saved to {TEST_FILE_PATH}")

        except Exception as e:
            logger.error("Error while splitting the csv file")
            raise CustomException("Failed splitting the csv file into train and test", e)

            # usually how we create the object for the above class - 
            # obj = DataIngestion()
            # obj.download_csv_from_gcp()
            # obj.split_data()

            # # Instead how we can call is
            # obj.run()

    def run(self):

        try:
            logger.info("Starting data ingestion process")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data Ingestion completed successfully")

        except CustomException as ce:
            logger.error(f"CustomException : {str(ce)}")

        finally:
            logger.info("Data Ingestion Completed")


# when we run the file in terminal python run xyz.py, what ever under if __name__ == "__main__" gets executed
if __name__ == "__main__":

    # create data ingestion class object, read_yaml for reading yaml file
    data_ingestion_obj = DataIngestion(yaml_file_reader(CONFIG_PATH))
    data_ingestion_obj.run()