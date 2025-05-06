import os

# path for data ingestion
RAW_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")
CONFIG_PATH = "config/config.yaml"


# path for data processing
PROCESSED_DIR = "artifacts/processed"
PROCESSED_TRAIN_DATA_PATH = os.path.join(
    PROCESSED_DIR, "processed_train_data.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(
    PROCESSED_DIR, "processed_test_data.csv")


# path for model training
MODEL_OUTPUT_PATH = "artifacts/models/lgbm.pkl"
