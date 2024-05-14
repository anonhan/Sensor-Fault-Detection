from dataclasses import dataclass
from matplotlib.figure import Figure

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    data_drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    label_encoder_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ModelMetricsArtifact:
    f1_score: float
    precision: float
    recall: float
    roc_curve_fig: Figure

@dataclass
class ModelTrainingArtifact:
    trained_model_file_path: str
    train_metric_artifact: ModelMetricsArtifact
    test_metric_artifact: ModelMetricsArtifact

@dataclass
class ModelEvaluationArtifact:
    trained_model_path: str
    best_model_path: str
    is_model_accepted: bool
    improved_accuracy: float
    train_model_metric_artifact: ModelMetricsArtifact
    best_model_metric_artifact: ModelMetricsArtifact

@dataclass
class ModelPusherArtifact:
    saved_model_path:str
    model_file_path:str