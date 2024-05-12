from Sensor_Fault_Detection.app_logging.app_logger import AppLogger
from Sensor_Fault_Detection.exceptions.exceptions import SensorException
import Sensor_Fault_Detection.utils.utils as utils
from Sensor_Fault_Detection.entity.config_entity import ModelTrainingConfig
from Sensor_Fault_Detection.entity.artifact_entity import ModelTrainingArtifact, DataTransformationArtifact
from Sensor_Fault_Detection.ml.metric.evaluation_metric  import get_evaluation_metrics
from Sensor_Fault_Detection.config.config import RANDOM_STATE, MODEL_TRAINING_LOG_FILE

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, roc_auc_score
# from sklearn.model_selection import cross_val_predict


import os, logging, pandas as pd, numpy as np

class ModelTraining:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, model_training_config: ModelTrainingConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_training_config = model_training_config
        self.logger = AppLogger(file_object=open(MODEL_TRAINING_LOG_FILE, 'a+'))
    
    def read_data(self):
        try:
            self.logger.log("Reading train and test files.")
            train_data = utils.load_numpy_array(self.data_transformation_artifact.transformed_train_file_path)
            test_data = utils.load_numpy_array(self.data_transformation_artifact.transformed_test_file_path)
            self.logger.log("Data read successfully.")
            return train_data, test_data
        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception

    def select_best_model(self, x_train, y_train, x_test, y_test):
        try:
            classifiers = {
                'SVM': SVC(),
                'Random Forest': RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE),
                'XGBoost': XGBClassifier(use_label_encoder=False, n_estimators=100),
                # 'Stacking Classifier': StackingClassifier(estimators=[])
            }

            # Train classifiers and evaluate accuracy
            best_accuracy = 0
            best_model = None

            for name, clf in classifiers.items():
                clf.fit(x_train, y_train)
                y_pred = clf.predict(x_test)
                accuracy = accuracy_score(y_test, y_pred)
                print(f'{name} Accuracy: {accuracy}')
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_model = clf

            self.logger.log(f"Best model is [{best_model}] :: accuracy is [{best_accuracy}]")

        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception


    def initiate_model_training(self) -> ModelTrainingArtifact:
        try:
            # Read the train and test data
            train_set, test_set = self.read_data()
            
            # Split the data into features and label
            x_train, y_train = train_set[:, :-1], train_set[:, -1]
            x_test, y_test = test_set[:, :-1], test_set[:, -1]

            # Train the model
            self.select_best_model(x_train, y_train, x_test, y_test)

        except Exception:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception