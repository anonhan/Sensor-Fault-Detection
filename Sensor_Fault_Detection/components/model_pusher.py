
from Sensor_Fault_Detection.exceptions.exceptions import SensorException
from Sensor_Fault_Detection.app_logging.app_logger import AppLogger
from Sensor_Fault_Detection.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from Sensor_Fault_Detection.entity.config_entity import ModelPusherConfig
from Sensor_Fault_Detection.config.config import MODEL_PUSHER_LOG_FILE
import os

import shutil, logging

class ModelPusher:
    def __init__(self, model_pusher_config:ModelPusherConfig, model_eval_artifact:ModelEvaluationArtifact):
        self.model_pusher_config = model_pusher_config
        self.model_eval_artifact = model_eval_artifact
        self.logger = AppLogger(open(MODEL_PUSHER_LOG_FILE, 'a+'))
    
    def initiate_model_pusher(self,)->ModelPusherArtifact:
        try:
            trained_model_path = self.model_eval_artifact.trained_model_path
            
            # Creating model pusher dir to save model
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copytree(src=trained_model_path, dst=model_file_path)

            # saved model dir
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)
            shutil.copytree(src=trained_model_path, dst=saved_model_path)

            #prepare artifact
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path, model_file_path=model_file_path)
            return model_pusher_artifact
        except  Exception as e:
            exc = SensorException()
            self.logger.log(str(exc), logging.ERROR)
            raise exc
    