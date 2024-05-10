import os
import pathlib
import Sensor_Fault_Detection
from datetime import datetime

PACKAGE_ROOT = pathlib.Path(Sensor_Fault_Detection.__file__).parent

LOG_PATH = os.path.join(PACKAGE_ROOT, "application_logs",f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}")
os.makedirs(LOG_PATH, exist_ok=True)
INGESTION_LOG_FILE = os.path.join(LOG_PATH, 'data_ingestion_logs.log')
VALIDATION_LOG_FILE = os.path.join(LOG_PATH, 'data_validation_logs.log')
TRAINING_LOG_FILE = os.path.join(LOG_PATH, 'training_logs.log')
RANDOM_STATE = 42