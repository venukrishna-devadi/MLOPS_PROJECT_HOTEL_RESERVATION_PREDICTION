
#########
# Trainig Pipeline
########


from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import yaml_file_reader
from config.paths import *

if __name__ == "__main__":
    # when someone runs this file, the things which we want to happen:
    # 1. Data Ingestion
    # create data ingestion class object, read_yaml for reading yaml file
    data_ingestion_obj = DataIngestion(yaml_file_reader(CONFIG_PATH))
    data_ingestion_obj.run()

    # 2. Data Preprocessing
    data_processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    data_processor.process()

    # 3. Model Training
    trainer = ModelTraining(PROCESSED_TRAIN_DIR, PROCESSED_TEST_DIR, SAVED_MODEL_PATH)
    trainer.run()
