import os
from src.logger import get_logger
from src.custom_exceptions import CustomException
import yaml
import pandas as pd

logger = get_logger(__name__)


def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError("File is not in the given path.")
        else:
            with open(file_path, "r") as yaml_file:
                config = yaml.safe_load(yaml_file)
                logger.info("Successfully read yaml file.")
                return config
    except Exception as e:
        logger.error("An exception occurred while reading yaml file")
        raise CustomException("Failed to read yaml file", e)


def load_data(path):
    try:
        logger.info("Data loading started!")
        data = pd.read_csv(path)
        logger.info("Data loading successful!")
        return data
    except Exception as e:
        logger.error("Error in data loading.")
        raise CustomException("Fail to load data", e)
