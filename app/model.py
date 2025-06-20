import joblib
import pandas as pd
from app.config import MODEL_PATH

def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        raise RuntimeError(f"Model not found at: {MODEL_PATH}")

def get_model():
    return load_model()

def make_prediction(pipeline, data):
    try:
        df = pd.DataFrame([data.dict()])
        return pipeline.predict(df)[0]
    except Exception as e:
        raise RuntimeError(f"Inference failed: {str(e)}")