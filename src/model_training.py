import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths import *
from config.model_params import *
from utils.common_functions import yaml_file_reader, load_data
from scipy.stats import randint

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:
    
    def __init__(self, train_path, test_path, model_save_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_save_path = model_save_path

        # here we are also initializing our lighgbm params and random search params
        self.params_dist = LIGHGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_split_data(self):
        
        try:
            logger.info(f"Loading Data from {self.train_path} and {self.test_path}")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Data Splitted Successfully for model training")

            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error(f"Error occured during loading and splitting data - {e}")
            raise CustomException("Failed to load data", e)
        

    def train_lgbm(self, X_train, y_train):

        try:
            logger.info("Initializing the model")

            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])
            logger.info("Starting Hyper Parameter Fine-Tuning")
            
            random_search = RandomizedSearchCV(
                estimator= lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                n_jobs = self.random_search_params["n_jobs"],
                verbose= self.random_search_params["verbose"],
                random_state= self.random_search_params["random_state"],
                scoring= self.random_search_params["scoring"]
            )

            logger.info("Starting Hyper Parameter Fine-Tuning")
            random_search.fit(X_train, y_train)

            logger.info("Hyper Parameter Fine-Tuning Completed")
            best_params = random_search.best_params_
            best_model = random_search.best_estimator_

            logger.info(f"Best Params are: {best_params}")
            logger.info(f"Best Model is: {best_model}")

            return best_model
        
        except Exception as e:
            logger.error(f"Error while training the model - {e}")
            raise CustomException("Failed to train the model", e)
        

    def evaluate_model(self, model, X_test, y_test):

        try:
            logger.info("Starting Model Evaluation")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)

            logger.info(f"Accuracy Score: {accuracy}")
            logger.info(f"Precision Score: {precision}")
            logger.info(f"Recall Score: {recall}")
            logger.info(f"F1 Score: {f1}")

            return {
                "Accuracy": accuracy,
                "Precision": precision,
                "Recall" : recall,
                "F1 Score": f1
            }
        
        except Exception as e:
            logger.error(f"Error while evaluating the model - {e}")
            raise CustomException("Failed to evaluating the model", e)

    def save_model(self, model):

        try:
            # Check if the output directory exists to save the model
            os.makedirs(os.path.dirname(self.model_save_path), exist_ok= True)
            logger.info("Saving the model.")

            joblib.dump(model, self.model_save_path)
            logger.info(f"Model Saved to {self.model_save_path}")

        except Exception as e:
            logger.error(f"Error while Saving the model - {e}")
            raise CustomException("Failed to Saving the model", e)
        
    def run(self):

        try:
            with mlflow.start_run():
                # whenever run method is called our mlflow will start
                


                logger.info("Starting MLFLOW Experimentation")


                logger.info("Starting our model training pipeline.")

                # First we want to log our the dataset - Which dataset was used to train the model
                # Later we could see that, this data was trained to get this version of the model
                # example - we got version 1 model by using 1000 rows of data
                logger.info("Logging the Training and Testing Dataset to MLFLOW")
                mlflow.log_artifact(local_path=self.train_path, artifact_path="datasets")
                mlflow.log_artifact(local_path=self.test_path,artifact_path="datasets")


                # first we will proceed with the load and split
                X_train, y_train, X_test, y_test = self.load_split_data()
                best_lgbm_model = self.train_lgbm(X_train, y_train)
                model_evaluation_metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)
                self.save_model(best_lgbm_model)

                # after we save the model, we want to log the model and metrics also in mlflow
                logger.info("Logging the model into MLFLOW")
                mlflow.log_artifact(self.model_save_path)
                logger.info("Logging the Params into MLFLOW")
                mlflow.log_params(params= best_lgbm_model.get_params())
                logger.info("Logging the Metrics into MLFLOW")
                mlflow.log_metrics(model_evaluation_metrics)


                logger.info("Model Training Completed Successfully")

        except Exception as e:
            logger.error(f"Error in Training Pipeline - {e}")
            raise CustomException("Failed during Training Pipeline", e)
        
if __name__ == "__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_DIR, PROCESSED_TEST_DIR, SAVED_MODEL_PATH)
    trainer.run()

