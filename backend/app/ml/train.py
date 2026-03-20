import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor, IsolationForest
import os
import sys

# Ensure we can import from app if needed, though this script is standalone
sys.path.append(os.getcwd())

# --- CONFIGURATION ---
# default paths (docker container) - will fall back to local relative paths if needed
from app.config import settings

DATA_PATH = settings.DATA_PATH
MODEL_PATH = settings.MODEL_PATH
SECURITY_PATH = settings.SECURITY_PATH

# If running outside container, the working directory is the backend folder.
# try to locate the CSV in a relative path before failing.
if not os.path.exists(DATA_PATH):
    alt_path = os.path.join(os.getcwd(), "data/dpp_data.csv")
    if os.path.exists(alt_path):
        DATA_PATH = alt_path
    # note: we leave MODEL_PATH/SECURITY_PATH unchanged; user should train in container or update settings

def train():
    print(f"🚀 STARTING TRAINING from {__file__}...")

    # 1. Load Data
    if not os.path.exists(DATA_PATH):
        print(f"❌ CRITICAL: Data file not found at {DATA_PATH}")
        print("   -> Please ensure 'data_dpp.csv' is in the 'backend/data' folder.")
        return

    print(f"📂 Loading dataset: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    
    # 2. Define Features (MUST match app/schemas.py)
    features = [
        "raw_material_energy", "raw_material_emission_factor", "raw_material_waste",
        "manufacturing_energy", "manufacturing_efficiency", "manufacturing_water_usage",
        "transport_distance_km", "transport_mode_factor", "logistics_energy",
        "usage_energy_consumption", "usage_duration_hours", "grid_carbon_intensity",
        "recycling_efficiency", "disposal_emission_factor", "recovered_material_value",
        "state_complexity_index", "policy_action_score", "optimization_reward_signal"
    ]
    target = "total_lifecycle_carbon_footprint"

    # Prepare Data
    X = df[features]
    y = df[target]

    # 3. Train Business Model (Regressor)
    print("🧠 Training Carbon Regressor (Random Forest)...")
    regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    regressor.fit(X, y)
    
    # measure R^2 (coefficient of determination) on training data
    try:
        from sklearn.metrics import r2_score
        predictions = regressor.predict(X)
        r2 = r2_score(y, predictions)
        print(f"📊 Training R^2 score: {r2:.4f}")
    except Exception:
        # older sklearn versions or missing import
        print("⚠️  Could not compute R^2 score, check sklearn version.")
    
    joblib.dump(regressor, MODEL_PATH)
    print(f"✅ Saved Business Model to: {MODEL_PATH}")

    # 4. Train Security Model (Anomaly Detector)
    print("🛡️  Training Security Shield (Isolation Forest)...")
    # Contamination=0.05 means we expect 5% of data to be anomalies
    security_model = IsolationForest(contamination=0.05, random_state=42)
    security_model.fit(X)
    
    joblib.dump(security_model, SECURITY_PATH)
    print(f"✅ Saved Security Model to: {SECURITY_PATH}")

    print("🎉 TRAINING COMPLETE.")

if __name__ == "__main__":
    train()