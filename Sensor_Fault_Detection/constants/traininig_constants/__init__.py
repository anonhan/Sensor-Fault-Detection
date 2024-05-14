import os
from Sensor_Fault_Detection.config.config import PACKAGE_ROOT

TRAINED_MODELS_DIR = os.path.join(PACKAGE_ROOT,'Trained_Models')

SAVED_MODELS_DIR = os.path.join('saved_models')
TARGET_COLUMN: str = 'class'
PIPELINE_NAME: str = 'sensor'
ARTIFACT_DIR: str = 'artifacts'
FILE_NAME: str = 'sensor.csv'

TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'

PREPROCESSING_OBJECT_NAME: str = 'preprocessing.pkl'
LABEL_ENCODER_OBJECT_NAME: str = 'encoder.pkl'
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

"""
Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME: str = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = 'transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = 'transformed_object'

"""
Model Training related constant start with MODEL_TRAINING VAR NAME
"""
MODEL_TRAINING_DIR_NAME: str = 'model_training'
MODEL_TRAINING_TRAINED_MODELS: str = 'trained_models'
MODEL_TRAINING_EXPECTED_ACCURACY: float = 0.90
MODEL_TRAINING_ACCEPTED_ACCURACY_DIFFERENCE: float = 0.03 
MODEL_TRAINING_MODEL_NAME: str = 'model.pkl'
MODEL_TRAINING_ROC_FIG_NAME: str = 'roc.png'


"""
Model Evaluation Metrics constant start with MODEL_EVALUATION VAR NAME
"""
MODEL_EVALUATION_DIR_NAME: str = "model_evaluation"
MODEL_EVALUATION_REPORT_FILE: str = "evaluation_report.yaml"
MODEL_EVALUATION_ACCURACY_CHANGED_THRESHOLD: float = 0.1


MODEL_PUSHER_DIR_NAME = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR = SAVED_MODELS_DIR