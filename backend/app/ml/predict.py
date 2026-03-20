import joblib
import numpy as np
from app.config import settings

def predict(features):
    model = joblib.load(settings.MODEL_PATH)
    # Note: Scaler logic should be here in prod, simplified for demo
    features = np.array(features).reshape(1, -1)
    return model.predict(features)[0]