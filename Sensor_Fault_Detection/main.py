from Sensor_Fault_Detection.pipeline.training_pipeline import TrainingPipeline
from Sensor_Fault_Detection.exceptions.exceptions import SensorException

if __name__ == '__main__':
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
    except:
        exc = SensorException()
        raise exc
    