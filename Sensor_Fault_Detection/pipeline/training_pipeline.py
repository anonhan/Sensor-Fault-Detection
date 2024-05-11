from Sensor_Fault_Detection.entity.config_entity import (TrainingPipelineConfig, 
                                                         DataIngestionConfig, 
                                                         DataValidationConfig,
                                                         DataTransformationConig)
from Sensor_Fault_Detection.entity.artifact_entity import (DataIngestionArtifact, 
                                                           DataValidationArtifact,
                                                           DataTransformationArtifact)
from Sensor_Fault_Detection.exceptions.exceptions import SensorException
from Sensor_Fault_Detection.app_logging.app_logger import AppLogger
from Sensor_Fault_Detection.components.data_ingestion import DataIngestion
from Sensor_Fault_Detection.components.data_validation import DataValidation
from Sensor_Fault_Detection.components.data_transformation import DataTransformation
from Sensor_Fault_Detection.config.config import TRAINING_LOG_FILE
import sys, logging

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
        self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
        self.data_transformation_config = DataTransformationConig(training_pipeline_config=self.training_pipeline_config)
        self.logger = AppLogger(open(TRAINING_LOG_FILE,'a+'))

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.logger.log("Started data ingestion...")
            data_ingestion_artifcat = DataIngestion(self.data_ingestion_config).initiate_data_ingestion()
            self.logger.log('End of data ingestion')
            return data_ingestion_artifcat
        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact)->DataValidationArtifact:
        try:
            self.logger.log("Started data validation...")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                                      data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            
            self.logger.log("End of data validation.")
            return data_validation_artifact

        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact

        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()
        
    def start_model_training(self)->DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()

    def start_model_evaluation(self)->DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()
    
    def start_model_pushing(self)->DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()

    def run_pipeline(self):
        try:
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact: DataValidationArtifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact: DataTransformationArtifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)

        except Exception as e: 
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()
    