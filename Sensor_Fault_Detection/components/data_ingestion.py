from Sensor_Fault_Detection.exceptions.exceptions import SensorException
from Sensor_Fault_Detection.app_logging.app_logger import AppLogger
from Sensor_Fault_Detection.entity.config_entity import DataIngestionConfig
from Sensor_Fault_Detection.entity.artifact_entity import DataIngestionArtifact
from Sensor_Fault_Detection.data_access.sensor_data import SensorData
import Sensor_Fault_Detection.utils.utils as utils
from Sensor_Fault_Detection.config.config import LOG_FILE, RANDOM_STATE, PACKAGE_ROOT
from Sensor_Fault_Detection.constants.traininig_constants import COLS_TO_DROP

import logging

import sys, os
from pandas import DataFrame
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.logger = AppLogger(file_object=open(LOG_FILE, 'a+'))

    def export_data_into_featre_store(self) -> DataFrame:
        '''
        Export Mongodb collection record as dataframe into feature store.
        '''
        try:
            sensor_data_obj = SensorData()
            self.logger.log("Exporting the data from mongodb")
            dataframe = sensor_data_obj.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            # Saving dataframe
            features_store_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(features_store_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(features_store_path, header=True, index=False)
            self.logger.log("Saved data successfully!")
            return dataframe

        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()
        
    def split_data_into_train_test(self, dataframe:DataFrame) -> DataFrame:
        '''
        Split feature store data into train test split
        '''
        try:
            train, test = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=RANDOM_STATE)
            self.logger.log("Splited data into train and test.")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train.to_csv(self.data_ingestion_config.training_file_path, index=False)
            test.to_csv(self.data_ingestion_config.test_file_path, index=False)
            self.logger.log("Saved train and test files.")

        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            df = self.export_data_into_featre_store()
            schema = utils.read_yaml_file(os.path.join(PACKAGE_ROOT,'schema','schema.yaml'))
            cols_to_drop = schema[COLS_TO_DROP]
            df.drop(columns=cols_to_drop, axis=1, inplace=True)
            self.split_data_into_train_test(df)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.test_file_path)
            return data_ingestion_artifact
        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()