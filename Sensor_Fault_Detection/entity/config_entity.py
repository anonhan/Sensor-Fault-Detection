import os 
from datetime import datetime
import Sensor_Fault_Detection.constants.traininig_constants as tc

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%d_%m_%Y_%H_%M_%S")
        self.pipeline_name: str = tc.PIPELINE_NAME
        self.artifact_dir: str = os.path.join(tc.ARTIFACT_DIR, timestamp)
        self.timestamp: str = timestamp

class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, tc.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir, tc.DATA_INGESTION_FEATURE_STORE_DIR, tc.FILE_NAME)
        self.training_file_path: str = os.path.join(self.data_ingestion_dir, tc.DATA_INGESTION_INGESTED_DIR, tc.TRAIN_FILE_NAME)
        self.test_file_path: str = os.path.join(self.data_ingestion_dir, tc.DATA_INGESTION_INGESTED_DIR, tc.TEST_FILE_NAME)
        self.train_test_split_ratio: float = tc.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = tc.DATA_INGESTION_COLLECTION_NAME

class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir, tc.DATA_VALIDATION_DIR_NAME)
        self.valid_data_file_path:str = os.path.join(self.data_validation_dir, tc.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_file_path: str = os.path.join(self.data_validation_dir, tc.DATA_VALIDATION_INVALID_DIR)
        self.data_drift_file_path: str = os.path.join(self.data_validation_dir, tc.DATA_VALIDATION_DRIFT_DIR, tc.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        # Train and Test of Valid and Invalid data
        self.valid_train_dir: str = os.path.join(self.valid_data_file_path, tc.TRAIN_FILE_NAME)
        self.invalid_train_dir: str = os.path.join(self.invalid_data_file_path, tc.TRAIN_FILE_NAME)
        self.valid_test_dir: str = os.path.join(self.valid_data_file_path, tc.TEST_FILE_NAME)
        self.invalid_test_dir: str = os.path.join(self.invalid_data_file_path, tc.TEST_FILE_NAME)

class DataTransformationConig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str = os.path.join(training_pipeline_config.artifact_dir, tc.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_data_file: str = os.path.join(self.data_transformation_dir, 
                                                             tc.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                             tc.TRAIN_FILE_NAME.replace('.csv', '.npy'))
        self.transformed_test_data_file: str = os.path.join(self.data_transformation_dir,
                                                            tc.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                            tc.TEST_FILE_NAME.replace('.csv', '.npy'))
        self.transformed_object_file: str = os.path.join(self.data_transformation_dir,
                                                         tc.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                         tc.PREPROCESSING_OBJECT_NAME)

class ModelTrainingConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_training_dir:str = os.path.join(training_pipeline_config.artifact_dir, tc.MODEL_TRAINING_DIR_NAME)
        self.trained_models_file_path: str = os.path.join(self.model_training_dir, tc.MODEL_TRAINING_TRAINED_MODELS)
        self.trained_model_name: str = os.path.join(self.trained_models_file_path, tc.MODEL_TRAINING_MODEL_NAME)
        self.roc_curve_fig: str = os.path.join(self.trained_models_file_path, tc.MODEL_TRAINING_ROC_FIG_NAME)
        self.expected_accuracy: float = tc.MODEL_TRAINING_EXPECTED_ACCURACY
