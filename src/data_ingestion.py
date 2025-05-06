import os
import pandas as pd
import boto3
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exceptions import CustomException
from utils.common_functions import read_yaml
from config.path_config import *

logger = get_logger(__name__)


class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.test_ratio = self.config["test_ratio"]
        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(
            f"Data ingestion started with {self.bucket_name}/{self.bucket_file_name}")

    def download_csv_from_aws(self):
        try:
            s3 = boto3.client("s3")
            s3.download_file(self.bucket_name,
                             self.bucket_file_name, RAW_FILE_PATH)
            logger.info("File has been loaded successfully!!")
        except Exception as e:
            logger.error("An unexpected error occurred while downloading file")
            raise CustomException(
                "An unexpected error occurred while downloading file", e)

    def split_data(self):
        try:
            data = pd.read_csv(RAW_FILE_PATH)

            train_data, test_data = train_test_split(data, test_size=self.test_ratio,
                                                     random_state=36)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"Train data has been save to {TRAIN_FILE_PATH}")
            logger.info(f"Test data has been saved to {TEST_FILE_PATH}")
        except Exception as e:
            logger.error("An unexpected error occurred while splitting data.")
            raise CustomException("Failed to split data", e)

    def run(self):
        try:
            logger.info("Data Ingestion started successfully!!")

            self.download_csv_from_aws()
            self.split_data()

            logger.info("Data Ingestion completed successfully!!")

        except Exception as e:
            logger.error("An unexpected error occurred while Data Ingestion.")
            raise CustomException("Failed to do Data Ingestion", e)


if __name__ == "__main__":
    config = read_yaml(CONFIG_PATH)
    obj = DataIngestion(config)
    obj.run()
