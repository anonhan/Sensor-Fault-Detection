from Sensor_Fault_Detection.app_logging.app_logger import AppLogger
from Sensor_Fault_Detection.exceptions.exceptions import SensorException
import Sensor_Fault_Detection.utils.utils as utils
from Sensor_Fault_Detection.entity.config_entity import ModelEvaluationConfig
from Sensor_Fault_Detection.entity.artifact_entity import ModelTrainingArtifact, ModelEvaluationArtifact, DataValidationArtifact
from Sensor_Fault_Detection.ml.metric.evaluation_metric  import get_evaluation_metrics
from Sensor_Fault_Detection.ml.model.estimator import SensorModel, ModelResolver
from Sensor_Fault_Detection.config.config import MODEL_EVALUATIOIN_LOG_FILE
from Sensor_Fault_Detection.constants.traininig_constants import TARGET_COLUMN, MODEL_FILE_NAME


import logging, pandas as pd, os

class ModelEvaluation:
    def __init__(self, model_training_artifact: ModelTrainingArtifact,
                  data_validation_artifact: DataValidationArtifact,
                  model_evaluation_config: ModelEvaluationConfig):
        self.model_training_artifact = model_training_artifact
        self.data_validation_artifact = data_validation_artifact 
        self.model_evaluation_config = model_evaluation_config
        self.logger = AppLogger(open(MODEL_EVALUATIOIN_LOG_FILE, 'a+'))

    
    def initiate_model_evaluaton(self) -> ModelEvaluationArtifact:
        try:
            training_file_path = self.data_validation_artifact.valid_train_file_path
            testing_file_path = self.data_validation_artifact.valid_test_file_path

            # reading dataframe
            train_set = pd.read_csv(training_file_path)
            test_set = pd.read_csv(testing_file_path)
            df = pd.concat([train_set, test_set], axis=0)
            y_true = df[TARGET_COLUMN]

            # current model path 
            model_file_path = self.model_training_artifact.trained_model_file_path
            model_file = os.path.join(self.model_training_artifact.trained_model_file_path, MODEL_FILE_NAME)
            # checking if model is available
            is_model_accepted = True
            model_resolver = ModelResolver()
            if not model_resolver.is_model_available():
                model_evaluation_artifact = ModelEvaluationArtifact(
                                        train_model_metric_artifact=self.model_training_artifact.test_metric_artifact,
                                        trained_model_path=model_file_path,
                                        improved_accuracy=None,
                                        best_model_path=None,
                                        best_model_metric_artifact=None,
                                        is_model_accepted=is_model_accepted
                                        )
                self.logger.log(f"Model Evaluation Artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact

            latest_model_path = model_resolver.get_latest_model()
            latest_model = utils.load_object(latest_model_path)
            train_model = utils.load_object(model_file)

            # Comparing both models
            y_pred_latest = latest_model.predict(df.drop(TARGET_COLUMN, axis=1))
            y_pred_train = train_model.predict(df.drop(TARGET_COLUMN, axis=1))

            y_score_latest = latest_model.predict_proba(df.drop(TARGET_COLUMN, axis=1))[:, 1]
            y_score_train = train_model.predict_proba(df.drop(TARGET_COLUMN, axis=1))[:, 1]

            # encoding labels
            y_true_encoded = train_model.encode_labels(df[TARGET_COLUMN])
            trained_metric = get_evaluation_metrics(y_true_encoded, y_pred_train, y_score_train)
            latest_metric = get_evaluation_metrics(y_true_encoded, y_pred_latest, y_score_latest)

            improved_accuracy = trained_metric.f1_score-latest_metric.f1_score
            if self.model_evaluation_config.model_accuracy_changed_threshold <= improved_accuracy:
                is_model_accepted = True
            else:
                is_model_accepted = False

            model_evaluation_artifact = ModelEvaluationArtifact(
                                        train_model_metric_artifact=trained_metric,
                                        trained_model_path=model_file_path,
                                        improved_accuracy=improved_accuracy,
                                        best_model_path=latest_model_path,
                                        best_model_metric_artifact=latest_metric,
                                        is_model_accepted=is_model_accepted
                                        )
            model_evaluation_report = model_evaluation_artifact.__dict__
            utils.write_yaml_file(self.model_evaluation_config.evaluation_report, model_evaluation_report)
            self.logger.log(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact

        except Exception:
            exception = SensorException()
            self.logger.log(exception, logging.ERROR)
            raise exception