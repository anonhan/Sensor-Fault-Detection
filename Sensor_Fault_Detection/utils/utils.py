from Sensor_Fault_Detection.exceptions.exceptions import SensorException

import pandas as pd, numpy as np
import yaml,os,dill
from sklearn.preprocessing import LabelEncoder

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
    
def save_object(file_path, pkl_object):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file=file_path, mode='wb') as f:
            dill.dump(pkl_object, f)       

    except Exception as e:
        exception = SensorException()
        raise exception
    
def save_numpy_array(file_path, array_object):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file=file_path, mode='wb') as f:
            np.save(file=file_path, arr=array_object)
    except Exception as e:
        exception = SensorException()
        raise exception
    
def load_numpy_array(file_path):
    try:
        with open(file=file_path, mode='rb') as f:
            array = np.load(file=file_path)
        return array
    except Exception as e:
        exception = SensorException()
        raise exception
    
def load_object(file_path):
    try:
        with open(file=file_path, mode='rb') as f:
            pkl = dill.loads(file=file_path)       
        return pkl
    except Exception as e:
        exception = SensorException()
        raise exception
    
def save_csv(file_path, csv_object):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        csv_object.to_csv(file_path)
    except Exception as e:
        exception = SensorException()
        raise exception
    
def read_csv(file_path):
    try:
        data = np.loadtxt(file_path, delimiter=',')
        return data
    except Exception as e:
        exception = SensorException()
        raise exception