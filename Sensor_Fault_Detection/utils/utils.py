from Sensor_Fault_Detection.exceptions.exceptions import SensorException

import pandas as pd
import yaml,os
from Sensor_Fault_Detection.config.config import PACKAGE_ROOT

def read_yaml_file(file_path:str):
    """
    Function to read the YAML File.
    """
    try:
        with open(file=file_path, mode='r') as f:
            yaml_data = yaml.load(f, Loader=yaml.SafeLoader)

        return yaml_data
    except Exception as e:
        exception = SensorException()
        raise exception

def write_yaml_file(file_path:str, content:object, replace=True):
    """
    Method to write the content in yaml file.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                    os.remove(file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            yaml.dump(data=content,stream=f)

    except Exception as e:
        exception = SensorException()
        raise exception