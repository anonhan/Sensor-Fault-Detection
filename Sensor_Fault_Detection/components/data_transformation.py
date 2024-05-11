from Sensor_Fault_Detection.app_logging.app_logger import AppLogger
from Sensor_Fault_Detection.exceptions.exceptions import SensorException
import Sensor_Fault_Detection.utils.utils as utils
from Sensor_Fault_Detection.entity.config_entity import DataTransformationConig
from Sensor_Fault_Detection.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from Sensor_Fault_Detection.config.config import TRANSFORMATION_LOG_FILE, RANDOM_STATE
from Sensor_Fault_Detection.constants.traininig_constants import TARGET_COLUMN

from sklearn.preprocessing import RobustScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from imblearn.combine import SMOTETomek
from sklearn.pipeline import Pipeline

import os, sys, logging, pandas as pd, numpy as np

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConig):
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config
        self.logger = AppLogger(open(TRANSFORMATION_LOG_FILE, 'a+'))
    
    
    def read_data(self) -> pd.DataFrame:
        try:
            self.logger.log("Reading train and test files.")
            train_data = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_data = pd.read_csv(self.data_validation_artifact.valid_test_file_path)
            self.logger.log("Data read successfully.")
            return train_data, test_data
        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception
        

    def encode_labels(self, y_train, y_test) -> tuple:
        try:
            self.logger.log("Started encodeing labels.")
            encoder = LabelEncoder()
            y_train_encoded = encoder.fit_transform(y_train)
            y_test_encoded = encoder.transform(y_test)
            # Get the mapping of original labels to encoded values
            label_mapping = dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))
            
            self.logger.log(f"Label encoding completed: {label_mapping}")
            return y_train_encoded, y_test_encoded
        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception
        
    def get_data_transformation_object(self) -> Pipeline:
        try:
            self.logger.log("Running data-transformation pipeline")
            scaler = RobustScaler()
            imputer = SimpleImputer()
            pipeline = Pipeline(steps=[
                ('imputer', imputer),
                ('sclaler', scaler)
            ])
            self.logger.log("Data-transformation pipeline ran successfully.")
            return pipeline
        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            self.logger.log("Started data transformation...")
            train_set, test_set = self.read_data()
            # Spliting data into features and labels
            x_train, y_train = train_set.drop(TARGET_COLUMN, axis=1), train_set[TARGET_COLUMN]
            x_test, y_test = test_set.drop(TARGET_COLUMN, axis=1), test_set[TARGET_COLUMN]

            # Encode labels
            y_train_en, y_test_en = self.encode_labels(y_train, y_test)

            # transform features
            pipeline = self.get_data_transformation_object()
            x_train_tf = pipeline.fit_transform(x_train)
            x_test_tf = pipeline.transform(x_test)

            # handle class imbalance
            smotetomek = SMOTETomek(sampling_strategy='minority', random_state=RANDOM_STATE)
            x_train_cb, y_train_cb = smotetomek.fit_resample(x_train_tf, y_train_en)
            x_test_cb, y_test_cb = smotetomek.fit_resample(x_test_tf, y_test_en)
            self.logger.log("Data imbalance completed.")

            # concatenate into an array
            train_arr = np.c_[x_train_cb, np.array(y_train_cb)]
            test_arr = np.c_[x_test_cb, np.array(y_test_cb)]
            self.logger.log("Concatenated arrays.")

            # Saving arrays
            utils.save_object(file_path=self.data_transformation_config.transformed_object_file, pkl_object=pipeline)
            utils.save_numpy_array(file_path=self.data_transformation_config.transformed_train_data_file, array_object=train_arr)
            utils.save_numpy_array(file_path=self.data_transformation_config.transformed_test_data_file, array_object=test_arr)
            self.logger.log("Saved tranformation data.")

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file,
                transformed_train_file_path=self.data_transformation_config.transformed_train_data_file,
                transformed_test_file_path=self.data_transformation_config.transformed_test_data_file
            )
            self.logger.log("Data transformation completed.")
            return data_transformation_artifact
            
        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception