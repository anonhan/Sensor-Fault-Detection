import os
import pathlib
import Sensor_Fault_Detection
from datetime import datetime

PACKAGE_ROOT = pathlib.Path(Sensor_Fault_Detection.__file__).parent
LOG_FILE = os.path.join(PACKAGE_ROOT, "application_logs",f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log")
RANDOM_STATE = 42