from Sensor_Fault_Detection.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from Sensor_Fault_Detection.entity.artifact_entity import DataIngestionArtifact
from Sensor_Fault_Detection.exceptions.exceptions import SensorException
from Sensor_Fault_Detection.app_logging.app_logger import AppLogger
from Sensor_Fault_Detection.components.data_ingestion import DataIngestion
from Sensor_Fault_Detection.config.config import LOG_FILE
import sys

# exception = SensorException()
logger = AppLogger(open(LOG_FILE,'a+'))

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logger.log("Started data ingestion...")
            data_ingestion_artifcat = DataIngestion(self.data_ingestion_config).initiate_data_ingestion()
            logger.log('End of data ingestion')
            return data_ingestion_artifcat
        except Exception as e:
            raise SensorException()

    def start_data_validation(self)->DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise SensorException()

    def start_data_transformation(self)->DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise SensorException()

    def start_model_training(self)->DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise SensorException()

    def start_model_evaluation(self)->DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise SensorException()
    
    def start_model_pushing(self)->DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise SensorException()

    def run_pipeline(self):
        try:
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
            
        except Exception as e:
            raise SensorException()        
    