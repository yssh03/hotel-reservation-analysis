import os
import numpy as np
import pandas as pd
from src.logger import get_logger
from src.custom_exceptions import CustomException
from config.path_config import *
from utils.common_functions import load_data, read_yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)


class DataPreprocessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        os.makedirs(processed_dir, exist_ok=True)

    def data_preprocessing(self, data):
        try:
            logger.info("data_preprocessing started!")

            logger.info("Dropping unnecessary columns!")
            data.drop(labels=["Unnamed: 0", "Booking_ID"],
                      axis=1, inplace=True)

            logger.info("Dropping duplicate columns!")
            data.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            logger.info("Label encoding started!")
            le = LabelEncoder()

            mapping = {}

            for column in cat_cols:
                data[column] = le.fit_transform(data[column])
                mapping[column] = {label: code for label, code in zip(
                    le.classes_, le.transform(le.classes_))}

            logger.info("Label Mappings are: ")
            for col, map in mapping.items():
                logger.info(f"{col} - {map}")

            logger.info("Skewness handling started!")
            skewness_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = data[num_cols].apply(lambda x: x.skew())

            for col in skewness[skewness > skewness_threshold].index:
                data[col] = np.log1p(data[col])

            return data
        except Exception as e:
            logger.error("Error in data processing!")
            raise CustomException("Failed to do data preprocessing", e)

    def imbalance_data_handling(self, data):
        try:

            logger.info("Handling data imbalancing!")
            X = data.drop(columns="booking_status")
            Y = data["booking_status"]

            smote = SMOTE(sampling_strategy="minority", random_state=7)

            x_resampled, y_resampled = smote.fit_resample(X, Y)

            balanced_df = pd.DataFrame(x_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Handled data imbalancing!")

            return balanced_df

        except Exception as e:
            logger.error("Error in imbalanced data handling!")
            raise CustomException("Failed to do imbalanced data handling.", e)

    def feature_selections(self, data):
        try:
            logger.info("Starting feature selection.")
            X = data.drop(columns="booking_status")
            Y = data["booking_status"]
            model = RandomForestClassifier()
            model.fit(X, Y)
            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                "feature": X.columns,
                "importance": feature_importance
            })
            no_of_feature = self.config["data_processing"]["top_feature_selection"]
            top_features_df = feature_importance_df.sort_values(
                by="importance", ascending=False)
            top_features = top_features_df["feature"].head(
                no_of_feature).values
            top_features_df = data[top_features.tolist() + ["booking_status"]]
            logger.info("Feature selection is done successfully!")
            return top_features_df
        except Exception as e:
            logger.error("Error in feature selection!")
            raise CustomException("Failed to do feature selection.", e)

    def save_data(self, data, path):
        try:
            logger.info("Saving data in processed directory.")
            data.to_csv(path, index=False)
            logger.info(f"Data is been saved in {path}")

        except Exception as e:
            logger.error("Error in data saving!")
            raise CustomException("Failed to do data saving.", e)

    def process(self):
        try:
            logger.info("Loading data from Raw Directory!")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.data_preprocessing(train_df)
            test_df = self.data_preprocessing(test_df)

            train_df = self.imbalance_data_handling(train_df)
            test_df = self.imbalance_data_handling(test_df)

            train_df = self.feature_selections(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)
        except Exception as e:
            logger.error("Error in Data Preprocessing Pipeline!")
            raise CustomException(
                "Failed to do Data Preprocessing Pipeline.", e)


if __name__ == "__main__":
    dp = DataPreprocessor(TRAIN_FILE_PATH, TEST_FILE_PATH,
                          PROCESSED_DIR, CONFIG_PATH)
    
    dp.process()