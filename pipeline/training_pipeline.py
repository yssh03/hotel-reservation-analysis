from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml
from config.path_config import *

if __name__ == "__main__":
    # data ingestion
    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()

    # data preprocessing
    data_preprocessing = DataPreprocessor(TRAIN_FILE_PATH, TEST_FILE_PATH,
                                          PROCESSED_DIR, CONFIG_PATH)

    data_preprocessing.process()

    # model training
    model_training = ModelTraining(
        PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    model_training.run()
