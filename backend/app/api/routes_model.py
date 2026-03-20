from fastapi import APIRouter, HTTPException, Request
from app.schemas import PredictionRequest
from app.services.model_service import make_prediction
from app.services.explain_service import explain
from app.services.drift_service import detect_drift
from app.ml.anomaly import is_anomalous
from slowapi import Limiter
from slowapi.util import get_remote_address
import pandas as pd

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/predict")
@limiter.limit("20/minute")
def predict_endpoint(request: PredictionRequest, http_req: Request):
    # 1. Security AI Check
    if is_anomalous(request.features):
        pred = make_prediction(request.features)
        return {
            "prediction": pred,
            "security_flag": "RED",
            "warning": "Anomaly Detected: Input pattern resembles attack vector."
        }
    
    # 2. Business Logic
    prediction = make_prediction(request.features)
    return {"prediction": prediction, "security_flag": "GREEN"}

@router.post("/explain")
def explain_endpoint(request: PredictionRequest):
    return {"shap_values": explain(request.features)}

@router.post("/drift")
def drift_endpoint(request: PredictionRequest):
    df = pd.DataFrame([request.features])
    return detect_drift(df)