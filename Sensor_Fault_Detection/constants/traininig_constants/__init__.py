import os
from Sensor_Fault_Detection.config.config import PACKAGE_ROOT

TRAINED_MODELS_DIR = os.path.join(PACKAGE_ROOT,'Trained_Models')

TARGET_COLUMN: str = 'class'
PIPELINE_NAME: str = 'sensor'
ARTIFACT_DIR: str = 'artifacts'
FILE_NAME: str = 'sensor.csv'

TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'

PREPROCESSING_OBJECT_NAME: str = 'preprocessing.pkl'
MODEL_FILE_NAME: str = 'model.pkl'
SCHEMA_FILE_PATH: str = os.path.join(PACKAGE_ROOT, 'schema','schema.yaml')
COLS_TO_DROP = 'drop_columns'

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "aps_readings"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR: str = 'valid'
DATA_VALIDATION_INVALID_DIR: str = 'invalid'
DATA_VALIDATION_DRIFT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'drift_report.yaml'
