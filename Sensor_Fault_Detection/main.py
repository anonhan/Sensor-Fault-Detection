from Sensor_Fault_Detection.pipeline.training_pipeline import TrainingPipeline
from Sensor_Fault_Detection.ml.model.estimator import ModelResolver
import Sensor_Fault_Detection.utils.utils as utils
from Sensor_Fault_Detection.constants.application import APP_HOST, APP_PORT
from Sensor_Fault_Detection.constants.traininig_constants import SAVED_MODELS_DIR

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from uvicorn import run
from starlette.responses import RedirectResponse
import pandas as pd


app = FastAPI()


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_model():
    try:
        train_pipeline = TrainingPipeline()
        if train_pipeline.is_pipeline_running:
            Response("Training Pipeline is already running, Please try in sometime!!")
        else:
            Response("Started running the Training Pipeline")
            train_pipeline.run_pipeline()
            Response("Training completed")
    except Exception as e:
        return Response("Error occured: \n"+str(e))

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        model_resolver = ModelResolver(models_dir=SAVED_MODELS_DIR)
        if not model_resolver.is_model_available():
            return Response("Model is not available.")
        model_path = model_resolver.get_latest_model()
        model = utils.load_object(model_path)

        y_pred = model.predict(df)
        # Reverse mapping of target column
        y_actual = model.inverse_transform(y_pred)
        df['predictions'] = y_actual
        return df.to_html()
        
    except Exception as e:
        return Response("Error occured during running Training Pipeline\n"+str(e))

if __name__ == '__main__':
        run(app, host=APP_HOST, port=APP_PORT)
