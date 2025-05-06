import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
from lightgbm import LGBMClassifier
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score
from src.logger import get_logger
from src.custom_exceptions import CustomException
from config.path_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
import mlflow
import mlflow.sklearn

logger = get_logger(__name__)


class ModelTraining:
    def __init__(self, train_path, test_path, model_output):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output = model_output

        self.param_dist = LIGHTGM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data from {self.test_path}")
            test_df = load_data(self.test_path)

            x_train = train_df.drop(columns="booking_status")
            y_train = train_df["booking_status"]

            x_test = test_df.drop(columns="booking_status")
            y_test = test_df["booking_status"]

            logger.info("Data splitting is successful!!")

            return x_train, y_train, x_test, y_test

        except Exception as e:
            logger.error("Error while loading and splitting data.")
            raise CustomException("Failed to load and split data.", e)

    def train_data(self, train, test):
        try:
            logger.info("Model training started!")

            lgbm = LGBMClassifier(
                random_state=self.random_search_params["random_state"], force_col_wise=True)

            logger.info("Starting hyperparameter tuning")

            random_cv = RandomizedSearchCV(
                estimator=lgbm,
                param_distributions=self.param_dist,
                n_iter=self.random_search_params["n_iter"],
                n_jobs=self.random_search_params["n_jobs"],
                verbose=self.random_search_params["verbose"],
                random_state=self.random_search_params["random_state"],
                scoring=self.random_search_params["scoring"],
            )

            logger.info("Starting Model training")

            random_cv.fit(train, test)

            logger.info("Hyper parameter tuning completed!")

            best_params = random_cv.best_params_
            best_lgbm_model = random_cv.best_estimator_

            logger.info(f"Best parameter for model: \n {best_params}")

            return best_lgbm_model

        except Exception as e:
            logger.error('An exception occurred while model training!')
            raise CustomException("Failed to do model training.", e)

    def model_evaluation(self, model, x_test, y_test):
        try:
            logger.info("Evaluating model.")
            y_pred = model.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f"accuracy: {accuracy}")
            logger.info(f"precision: {precision}")
            logger.info(f"recall: {recall}")
            logger.info(f"f1: {f1}")

            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1
            }

        except Exception as e:
            logger.error('An exception occurred in model evaluation.')
            raise CustomException("Failed to evaluate model.", e)

    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output), exist_ok=True)
            joblib.dump(model, self.model_output)
            logger.info(f"Model saved successfully in {self.model_output}")
        except Exception as e:
            logger.error('An exception occurred in model saving.')
            raise CustomException("Failed to save model", e)

    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting model training pipeline.")

                logger.info("Starting MLFlow experimentation.")

                logger.info(
                    "Logging the training and testing dataset to MLFlow.")

                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                x_train, y_train, x_test, y_test = self.load_and_split_data()

                model = self.train_data(x_train, y_train)

                metrics = self.model_evaluation(model, x_test, y_test)

                self.save_model(model)

                logger.info("Logging the model into MLFlow")
                mlflow.log_artifact(self.model_output)

                mlflow.log_params(model.get_params())

                mlflow.log_metrics(metrics)

                logger.info("Model training successfully completed!")

        except Exception as e:
            print('An exception occurred in model training pipeline')
            raise CustomException("Failed to run model training pipeline.", e)


if __name__ == "__main__":
    model_training = ModelTraining(
        PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    model_training.run()
