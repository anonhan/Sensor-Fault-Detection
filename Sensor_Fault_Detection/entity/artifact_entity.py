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
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ModelTrainingArtifact:
    model_training_dir: str
    trained_models_dir: str
    traned_model_name: str
    expected_accuracy: str
    metrics_artifact: str

@dataclass
class ModelEvalutationArtifact:
    f1_score: float
    precision: float
    recall: float
    roc_curve_fig: Figure