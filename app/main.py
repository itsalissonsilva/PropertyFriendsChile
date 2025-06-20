from fastapi import FastAPI, HTTPException, Request, Header, Depends
from typing import Optional
from app.schemas import PropertyInput, PredictionOutput
from app.model import get_model, make_prediction
from app.utils import log_request, validate_api_key
from pathlib import Path
import time


START_TIME = time.time()

app = FastAPI()

@app.on_event("startup")
def check_model_ready():
    model_path = Path("models/model.pkl")
    if not model_path.exists():
        raise RuntimeError("Model file not found. Make sure training is complete.")


@app.get("/")
def root():
    return {"message": "API is running. Visit /docs for testing."}


@app.get("/health")
def health_check():
    uptime_seconds = int(time.time() - START_TIME)
    return {
        "status": "ok",
        "uptime": f"{uptime_seconds} seconds"
    }

@app.post("/predict", response_model=PredictionOutput)
async def predict_price(
    data: PropertyInput,
    x_api_key: Optional[str] = Header(None),
    model_pipeline = Depends(get_model)
):
    validate_api_key(x_api_key)
    log_request(data.dict())
    prediction = make_prediction(model_pipeline, data)
    rounded = round(prediction)
    return {"predicted_price": rounded}