import numpy as np
import pandas as pd
import sys, json
from typing import Optional
from Sensor_Fault_Detection.constants.database import DATABASE_NAME
from Sensor_Fault_Detection.config.mongodb_connection import MongoDBClient
from Sensor_Fault_Detection.exceptions.exceptions import SensorException

class SensorData:
    def __init__(self):
        '''
        Export the mongodb data as dataframe
        '''
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise SensorException()
    
    def export_collection_as_dataframe(self, collection_name:str, database_name: Optional[str]=None) -> pd.DataFrame:
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if '_id' in df.columns.to_list():
                df = df.drop(['_id'], axis=1)
            df.replace({'na':np.nan}, inplace=True)
            return df

        except Exception as e:
            raise SensorData(e, sys)
    
    # def save_csv(self, file_path:str, dataframe:pd.DataFrame) -> None:
    #     '''Method to save the df as csv in the provided path'''
    #     try:
    #         if

    #     except Exception as e:
    #         raise SensorException()