from sklearn.ensemble import IsolationForest
import joblib
import numpy as np
from app.config import settings
import os

def train_anomaly_detector(X_train):
    clf = IsolationForest(contamination=0.1, random_state=42)
    clf.fit(X_train)
    joblib.dump(clf, settings.ANOMALY_PATH)
    return clf

def is_anomalous(features):
    if not os.path.exists(settings.ANOMALY_PATH):
        return False
    clf = joblib.load(settings.ANOMALY_PATH)
    # IsolationForest returns -1 for anomaly, 1 for normal
    pred = clf.predict(np.array(features).reshape(1, -1))
    return pred[0] == -1