from Sensor_Fault_Detection.exceptions.exceptions import SensorException
from Sensor_Fault_Detection.entity.artifact_entity import ModelMetricsArtifact

from sklearn.metrics import precision_score, recall_score, f1_score, roc_curve, auc
import matplotlib.pyplot as plt

def get_evaluation_metrics(y_true, y_pred, y_score) -> ModelMetricsArtifact:
    try:
        model_f1_score = f1_score(y_pred=y_pred, y_true=y_true)
        model_recall = recall_score(y_pred=y_pred, y_true=y_true)
        model_precision = precision_score(y_pred=y_pred, y_true=y_true)
        
        fpr, tpr, thresholds = roc_curve(y_true=y_true, y_score=y_score)
        roc_auc = auc(fpr, tpr)
        plt.figure()  
        plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend()
        
        return ModelMetricsArtifact(model_f1_score, model_precision, model_recall, plt.gcf())
    except Exception:
        exc = SensorException()
        raise exc