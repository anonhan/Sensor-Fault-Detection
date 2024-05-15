from Sensor_Fault_Detection.entity.config_entity import (TrainingPipelineConfig, 
                                                         DataIngestionConfig, 
                                                         DataValidationConfig,
                                                         DataTransformationConig,
                                                         ModelTrainingConfig,
                                                         ModelEvaluationConfig,
                                                         ModelPusherConfig)
from Sensor_Fault_Detection.entity.artifact_entity import (DataIngestionArtifact, 
                                                           DataValidationArtifact,
                                                           DataTransformationArtifact,
                                                           ModelTrainingArtifact,
                                                           ModelEvaluationArtifact,
                                                           ModelMetricsArtifact,
                                                           ModelPusherArtifact)
from Sensor_Fault_Detection.exceptions.exceptions import SensorException
from Sensor_Fault_Detection.app_logging.app_logger import AppLogger
from Sensor_Fault_Detection.components.data_ingestion import DataIngestion
from Sensor_Fault_Detection.components.data_validation import DataValidation
from Sensor_Fault_Detection.components.data_transformation import DataTransformation
from Sensor_Fault_Detection.components.model_training import ModelTraining
from Sensor_Fault_Detection.components.model_evaluation import ModelEvaluation
from Sensor_Fault_Detection.components.model_pusher import ModelPusher
from Sensor_Fault_Detection.cloud_stroage.s3_stroge import S3Sync
from Sensor_Fault_Detection.config.config import TRAINING_LOG_FILE
from Sensor_Fault_Detection.constants.s3_bucket import TRAINING_BUCKET_NAME
from Sensor_Fault_Detection.constants.traininig_constants import SAVED_MODELS_DIR
import sys, logging

class TrainingPipeline:
    def __init__(self):
        self.is_pipeline_running = False
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
        self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
        self.data_transformation_config = DataTransformationConig(training_pipeline_config=self.training_pipeline_config)
        self.model_training_config = ModelTrainingConfig(training_pipeline_config=self.training_pipeline_config)
        self.model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
        self.model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)

        self.logger = AppLogger(open(TRAINING_LOG_FILE,'a+'))
        self.s3_sync = S3Sync()

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
            self.logger.log("Started data transformation.")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            self.logger.log("Data transformation completed.")
            return data_transformation_artifact

        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()
        
    def start_model_training(self, data_transformation_artifact)->ModelTrainingArtifact:
        try:
            self.logger.log('Started model training.')
            model_trainer = ModelTraining(data_transformation_artifact=data_transformation_artifact,
                                          model_training_config=self.model_training_config)
            model_training_artifact = model_trainer.initiate_model_training()
            self.logger.log('Model training completed.')
            return model_training_artifact

        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()

    def start_model_evaluation(self, model_training_artifact, data_validation_artifact)->DataIngestionArtifact:
        try:
            self.logger.log("Started Model evaluator.")
            model_evaluator = ModelEvaluation(model_training_artifact=model_training_artifact,
                                              data_validation_artifact=data_validation_artifact,
                                              model_evaluation_config=self.model_evaluation_config)
            model_evaluation_artifact = model_evaluator.initiate_model_evaluaton()
            self.logger.log('Model evaluation completed.')
            return model_evaluation_artifact
        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()
    
    def start_model_pushing(self, model_eval_artifact)->DataIngestionArtifact:
        try:
            self.logger.log("Started model pusher.")
            model_pusher_artifact = ModelPusher(model_pusher_config=self.model_pusher_config,
                                                model_eval_artifact=model_eval_artifact)
            model_pusher_artifact = model_pusher_artifact.initiate_model_pusher()
            self.logger.log('Pushed model.')
            return model_pusher_artifact
        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()
        
    def sync_artifact_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_buket_url)
        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()            
        
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODELS_DIR}"
            self.s3_sync.sync_folder_to_s3(folder = SAVED_MODELS_DIR,aws_bucket_url=aws_buket_url)
        except Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()        

    def run_pipeline(self):
        try:
            self.is_pipeline_running = True
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact: DataValidationArtifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact: DataTransformationArtifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact: ModelTrainingArtifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact: ModelEvaluationArtifact = self.start_model_evaluation(model_training_artifact=model_trainer_artifact,
                                                                                             data_validation_artifact=data_validation_artifact)
            if not model_evaluation_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            model_pusher_artifact: ModelPusherArtifact = self.start_model_pushing(model_eval_artifact=model_evaluation_artifact)
            self.is_pipeline_running = False

            # if successfull
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()

        except Exception as e: 
            self.sync_artifact_dir_to_s3()
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise SensorException()
    