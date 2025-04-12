import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths import *
from utils.common_functions import yaml_file_reader, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

# Now we will make a class for Data Preprocessing

class DataProcessor:
    
    def __init__(self, train_path, test_path, processed_dir, config_path):
        # train_path - from where to take the train data
        # processed_dir - where to store the processed data, dir is already in paths.py - PROCESSED_DIR
        # config_path - where we have our yaml file with all the configurations

        # now make instance variables
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        #for reading the file passed by config_path
        self.config = yaml_file_reader(config_path)

        # first we need to create a processed_dir in artifacts folder where we save the processed df
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            logger.info("Created Processed Directory")

    def preprocess_data(self, df):

        try:
            logger.info("Starting Data Preprocessing Steps")

            logger.info("Dropping Unnamed and Booking ID Columns and removing duplicates.")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'] , inplace=True)
            df.drop_duplicates(inplace=True)

            # We have to define all the categorical columns and numerical columns that we have 
            # to extract from the yaml file

            cat_cols = self.config["data_preprocessing"]["categorical_columns"]
            num_cols = self.config["data_preprocessing"]["numerical_columns"]

            # next we will do the label encoding
            logger.info("Applying Label Encoding")

            label_encoder = LabelEncoder()
            mappings={}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                 
            mappings[col] = {label:code for label,code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}
            logger.info("Label Mappings are - ")
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            logger.info("Starting Skewness Handling")
            skewness_threshold = self.config["data_preprocessing"]["skewnewss_threshold"]
            skewness = df[num_cols].apply(lambda x:x.skew())

            for column in skewness[skewness > skewness_threshold].index:
                df[column] = np.log1p(df[column])

            return df
        
        except Exception as e:
            logger.error(f"Error during preprocess step {e}")
            raise CustomException("Error occured during preprocessing data - ", e)
        

    def balancing_data(self, df):

        try:
            logger.info("Handling Imbalanced Data")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            smote = SMOTE(random_state=42)
            X_ressampled , y_resampled = smote.fit_resample(X,y)
            balanced_df = pd.DataFrame(X_ressampled , columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Data Balanced Successfully")
            return balanced_df
        
        except Exception as e:
            logger.error(f"Error during perform balancing data {e}")
            raise CustomException("Error occured during balancing data - ", e)
        

    def feature_selection(self, df):

        try:
            logger.info("Starting Feature Selection")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            model =  RandomForestClassifier(random_state=42)
            model.fit(X,y)
            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'feature':X.columns,
                'importance':feature_importance
                })
            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            num_features_to_select = self.config["data_preprocessing"]["no_of_features"]
            top_10_features = top_features_importance_df["feature"].head(num_features_to_select).values
            top_10_df = df[top_10_features.tolist() + ["booking_status"]]
            
            logger.info("Feature Selection Completed Successfully")
            logger.info(f"Top 10 features are - {top_10_features}")

            return top_10_df
        
        except Exception as e:
            logger.error(f"Error during perform feature selection {e}")
            raise CustomException("Error occured during feature selection step - ", e)
        

    # now we have our data in df format, we want to save it in csv format

    def save_data_in_csv(self,df, file_path):
        try:
            logger.info("Saving our data from dataframe format to csv format in processed folder")

            df.to_csv(file_path, index = False)

            logger.info("Data Saved Successfully to given file path")

        except Exception as e:
            logger.error(f"Error while saving data to given path {e}")
            raise CustomException("Error occured during saving data - ", e)
        

    # just like how we combined all the step using def run(self), we will do the same here

    def process(self):
        try:
            logger.info("Loading the data from raw directory")
            
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balancing_data(train_df)

            train_df = self.feature_selection(train_df)
            # there can be different important features for train and test df
            # we will use the same df which are important for train_df
            test_df = test_df[train_df.columns]

            self.save_data_in_csv(train_df, PROCESSED_TRAIN_DIR)
            self.save_data_in_csv(test_df, PROCESSED_TEST_DIR)

            logger.info("Data Processing completed successfully.")

        except Exception as e:
            logger.error(f"Error during preprocessing {e}")
            raise CustomException("Error during preprocessing pipeline - ", e)



# Checking if our data preprocessing pipeline is working correctly or not
if __name__ == "__main__":

    data_processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    data_processor.process()


