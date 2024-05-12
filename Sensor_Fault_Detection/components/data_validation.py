from Sensor_Fault_Detection.app_logging.app_logger import AppLogger
from Sensor_Fault_Detection.exceptions.exceptions import SensorException
from Sensor_Fault_Detection.entity.config_entity import DataValidationConfig
from Sensor_Fault_Detection.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import Sensor_Fault_Detection.utils.utils as utils
from Sensor_Fault_Detection.config.config import VALIDATION_LOG_FILE, RANDOM_STATE, PACKAGE_ROOT
from Sensor_Fault_Detection.constants.traininig_constants import SCHEMA_FILE_PATH

from scipy.stats import ks_2samp
import sys, os, logging, pandas as pd, numpy as np
class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self.logger = AppLogger(open(file=VALIDATION_LOG_FILE, mode='a+'))
    
    def read_data(self) -> pd.DataFrame:
        '''
        Method to read the data saved by the data ingestion pipeline as train and test.
        '''
        try:
            self.logger.log("Reading train and test files.")
            train_data = pd.read_csv(self.data_ingestion_artifact.trained_file_path)
            test_data = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            self.logger.log("Data read successfully.")
            return train_data, test_data
        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception

    def validate_number_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            df_cols = dataframe.shape[1]
            schema_cols = len(utils.read_yaml_file(SCHEMA_FILE_PATH)['columns'])
            self.logger.log(f"Dataframe has columns [{df_cols}] and schema has columns [{schema_cols}]")
            if schema_cols == (df_cols):
                self.logger.log("Dataframe columns matched with schema columns.")
                return True
            else:
                return False
        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception
    
    def is_numerical_cols_exist(self, dataframe:pd.DataFrame) -> bool:
        try:
            df_cols = set(dataframe.columns)
            schema_cols = set(utils.read_yaml_file(SCHEMA_FILE_PATH)['numerical_columns'])
            missing_cols = schema_cols-df_cols
            is_missing = not missing_cols
            return is_missing, missing_cols
        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception
    
    def drop_std_zero_columns(self, train_data: pd.DataFrame, test_data: pd.DataFrame):
        try:
            train_df = train_data.copy()
            test_df = test_data.copy()
            
            # Select only numeric columns for both train and test sets
            train_numeric_cols = train_df.select_dtypes(include=[np.number])
            test_numeric_cols = test_df.select_dtypes(include=[np.number])

            # Calculate standard deviation for numeric columns in both sets
            train_st_dev = train_numeric_cols.std().to_dict()
            test_st_dev = test_numeric_cols.std().to_dict()

            train_constant_columns = [col for col in train_numeric_cols.columns if train_numeric_cols[col].nunique() == 1]
            test_constant_columns = [col for col in test_numeric_cols.columns if test_numeric_cols[col].nunique() == 1]

            # Find columns with zero standard deviation in both sets
            all_st_dev_zero = list(set([col for col, val in train_st_dev.items() if val == 0] +
                                       [col for col, val in test_st_dev.items() if val == 0]+
                                       train_constant_columns + test_constant_columns))
            # Drop zero standard deviation columns from both sets
            train_df.drop(columns=all_st_dev_zero, axis=1, inplace=True)
            test_df.drop(columns=all_st_dev_zero, axis=1, inplace=True)

            # Logging
            if all_st_dev_zero:
                self.logger.log(f"Dropped zero standard-deviation columns from both train and test sets: {all_st_dev_zero}.")
            else:
                self.logger.log('No columns to drop with zero standard-deviation in both train and test sets.')

            return train_df, test_df

        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception



    def detect_data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, threshold=0.05) -> bool:
        try:
            drift_detected = False
            drift_result = {}
            for feature in base_df.columns:
                ks_stat, p_val = ks_2samp(base_df[feature], current_df[feature])
                if p_val <= threshold:
                    drift_detected = True
                    drift_result[feature] = {'ks_statistic': ks_stat, 'p_value': p_val}
            
            drift_report_file_path = self.data_validation_config.data_drift_file_path
            data_drift_path = os.path.dirname(drift_report_file_path)
            os.makedirs(data_drift_path, exist_ok=True)
            utils.write_yaml_file(drift_report_file_path, drift_result)

            return drift_detected

        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            # Reading train and test data
            train_set, test_set = self.read_data()

            # Vars to track status of data validation
            self.logger.log("Validating number of columns.")
            status_message = ""
            train_invalid_problems = 0
            test_invalid_problems = 0

            # Validating number of columns in 
            status = self.validate_number_of_columns(train_set)
            if not status:
                train_invalid_problems += 1
                status_message = status_message+f"Error: the number of columns are different in Train Data.\n"
            status = self.validate_number_of_columns(test_set)
            if not status:
                test_invalid_problems += 1
                status_message = status_message + f"Error: the number of columns are different in Test Data.\n"

            # Validating numerical columns
            status = self.is_numerical_cols_exist(train_set)
            if not status:
                train_invalid_problems += 1
                status_message = status_message + f"Error: Some columns are missing in Train Data.\n"
            status = self.is_numerical_cols_exist(test_set)
            if not status:
                test_invalid_problems += 1
                status_message = status_message + f"Error: Some columns are missing in Test Data.\n"

            if (train_invalid_problems>0) or (test_invalid_problems>0):
                self.logger.log(status_message, logging.CRITICAL)
                raise status_message
        
            if train_invalid_problems>0:
                utils.save_csv(self.data_validation_config.invalid_train_dir, train_set)
            else:
                utils.save_csv(self.data_validation_config.valid_train_dir, train_set)
            
            if test_invalid_problems>0:
                utils.save_csv(self.data_validation_config.invalid_test_dir, test_set)
            else:
                utils.save_csv(self.data_validation_config.valid_test_dir, test_set)


            # Drop the columns with zero standard-deviation
            train_set, test_set = self.drop_std_zero_columns(train_set, test_set)
            self.logger.log(f"[{train_set.shape}], [{test_set.shape}]", logging.WARNING)
            # test_set = self.drop_std_zero_columns(test_set)
            
            # Detect the data drift
            status = self.detect_data_drift(train_set, test_set)
            if status:
                self.logger.log("Data Drift detected!!", logging.WARNING)
            
            data_validation_artifact = DataValidationArtifact(validation_status=status,
                                                              valid_train_file_path=self.data_validation_config.valid_train_dir,
                                                              valid_test_file_path=self.data_validation_config.valid_test_dir,
                                                              invalid_train_file_path=self.data_validation_config.invalid_train_dir,
                                                              invalid_test_file_path=self.data_validation_config.invalid_test_dir,
                                                              data_drift_report_file_path=self.data_validation_config.data_drift_file_path
                                                              )
            self.logger.log("End of data validation.")
            self.logger.log(f"Data Validation Artifact [{data_validation_artifact}]")
            return data_validation_artifact

        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception