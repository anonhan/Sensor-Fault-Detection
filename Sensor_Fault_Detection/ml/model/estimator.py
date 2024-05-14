from Sensor_Fault_Detection.exceptions.exceptions import SensorException
from Sensor_Fault_Detection.constants.traininig_constants import SAVED_MODELS_DIR, MODEL_FILE_NAME

import os

class SensorModel:
    def __init__(self, preprocessor, encoder, model):
        self.preprocessor = preprocessor
        self.encoder = encoder
        self.model = model
    
    def predict(self, x):
        try:
            self.transformed_x = self.preprocessor.transform(x)
            predictions = self.model.predict(self.transformed_x)
            return predictions
        except Exception as e:
            raise SensorException()
    
    def predict_proba(self, x):
        try:
            predictions_proba = self.model.predict_proba(self.transformed_x)
            return predictions_proba
        except Exception as e:
            raise SensorException()
    
    def encode_labels(self, y):
        try:
            y_encoded = self.encoder.transform(y)
            return y_encoded
        except Exception:
            raise SensorException()

    
class ModelResolver:
    def __init__(self, models_dir=SAVED_MODELS_DIR):
        self.models_dir = models_dir

    def get_latest_model(self) -> str:
        try:
            latest_dir = sorted(os.listdir(self.models_dir), reverse=True)[0]
            latest_model_path = os.path.join(self.models_dir,latest_dir,MODEL_FILE_NAME)
            return latest_model_path
        except Exception:
            exc = SensorException()
            raise exc
    
    def is_model_available(self) -> bool:
        try:
            if not os.path.exists(self.models_dir):
                return False
            
            timestamp_dirs = os.listdir(self.models_dir)
            if len(timestamp_dirs) == 0:
                return False

            if not os.path.exists(self.get_latest_model()):
                return False
            
            return True
        except Exception:
            exc = SensorException()
            raise exc
