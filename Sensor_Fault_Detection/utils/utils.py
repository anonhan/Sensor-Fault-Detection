from Sensor_Fault_Detection.exceptions.exceptions import SensorException

import pandas as pd
import yaml,os
from Sensor_Fault_Detection.config.config import PACKAGE_ROOT

def read_yaml_file(file_path:str):
    """
    Function to read the YAML File.
    """
    with open(file=file_path, mode='r') as f:
        yaml_data = yaml.load(f, Loader=yaml.SafeLoader)

    return yaml_data
