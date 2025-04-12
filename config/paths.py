# Here we will list all the paths
import os

######### Create Paths For Data Ingestion ###########

#1. Where do want to store our data?
# We store in artifacts folder inside raw sub folder

RAW_DIR = "artifacts/raw"
# after the data gets extracted, it will come in a whole file as raw, where we want to store it
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

##############################
# We want to read data from config.yaml
CONFIG_PATH = "config/config.yaml"


################## ALL THE PATHS REQUIRED FOR DATA PROCESSING STEP ###################
PROCESSED_DIR = "artifacts/processed"
PROCESSED_TRAIN_DIR = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_DIR = os.path.join(PROCESSED_DIR, "processed_test.csv")

################### MODEL TRAINING ###############
SAVED_MODEL_PATH = "artifacts/models/lgbm_model.pkl"