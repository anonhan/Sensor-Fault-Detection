from Sensor_Fault_Detection.app_logging.app_logger import AppLogger
from Sensor_Fault_Detection.exceptions.exceptions import SensorException
import Sensor_Fault_Detection.utils.utils as utils
from Sensor_Fault_Detection.entity.config_entity import ModelTrainingConfig
from Sensor_Fault_Detection.entity.artifact_entity import ModelTrainingArtifact, DataTransformationArtifact
from Sensor_Fault_Detection.ml.metric.evaluation_metric  import get_evaluation_metrics
from Sensor_Fault_Detection.ml.model.estimator import SensorModel
from Sensor_Fault_Detection.config.config import RANDOM_STATE, MODEL_TRAINING_LOG_FILE

from xgboost import XGBClassifier
import matplotlib.pyplot as plt
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, roc_auc_score


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

    def train_model(self, x_train, y_train):
        try:
            XGBoost = XGBClassifier(use_label_encoder=False, n_estimators=100)
            XGBoost.fit(x_train, y_train)
            return XGBoost
        except Exception as e:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception

    def initiate_model_training(self) -> ModelTrainingArtifact:
        try:
            self.logger.log('Model Training Started')
            # Read the train and test data
            train_set, test_set = self.read_data()
            
            # Split the data into features and label
            x_train, y_train = train_set[:, :-1], train_set[:, -1]
            x_test, y_test = test_set[:, :-1], test_set[:, -1]

            # Train the model and get predictions
            model = self.train_model(x_train, y_train)
            # Train scores
            y_preds_train = model.predict(x_train)
            y_scores_train = model.predict_proba(x_train)[:, 1]
            classification_report_train = get_evaluation_metrics(y_pred=y_preds_train, y_true=y_train, y_score=y_scores_train)

            # Test scores
            y_preds_test = model.predict(x_test)
            y_scores_test = model.predict_proba(x_test)[:, 1]
            classification_report_test = get_evaluation_metrics(y_pred=y_preds_test, y_true=y_test, y_score=y_scores_test)

            # Determining the Model acceptance
            if classification_report_test.f1_score <= self.model_training_config.expected_accuracy:
                raise Exception("Model performance does not meet the set accuracy threshold.")

            # Detecting Overfitting and Underfitting:
            score_diff = abs(classification_report_test.f1_score - classification_report_train.f1_score)
            if score_diff >= self.model_training_config.model_score_difference_threshold:
                raise Exception("Model has high difference in scores (Overfitting or Underfitting detected)!")

            # binding the preprocessor and model together
            preprocessing_obj = utils.load_object(self.data_transformation_artifact.transformed_object_file_path)
            encoder_obj = utils.load_object(self.data_transformation_artifact.label_encoder_object_file_path)
            sensor_model = SensorModel(preprocessing_obj, encoder_obj, model)
            # Saving the Model pipeline
            utils.save_object(self.model_training_config.trained_model_name, sensor_model)

            # Generating Model Trainer Artifact
            model_artifact: ModelTrainingArtifact = ModelTrainingArtifact(self.model_training_config.trained_models_file_path,
                                                                                  classification_report_train,
                                                                                  classification_report_test)
            self.logger.log(f"Model training completed: [{model_artifact.test_metric_artifact.f1_score, model_artifact.train_metric_artifact.f1_score}]")
            return model_artifact

        except Exception:
            exception = SensorException()
            self.logger.log(str(exception), logging.ERROR)
            raise exception