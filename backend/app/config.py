import os

class Settings:
    # By default the container uses /app as its base directory. When the
    # repository is run locally (e.g. on Windows) that path doesn't exist, so
    # we fall back to the current working directory.  This ensures that both
    # DATA_PATH and MODEL_PATH point into `backend/data` during development.
    BASE_DIR = os.getenv("BASE_DIR", "/app")
    if not os.path.exists(BASE_DIR):
        BASE_DIR = os.getcwd()

    # 1. Path to the CSV Data
    DATA_PATH = os.path.join(BASE_DIR, "data/dpp_data.csv")

    # 2. Path to the Trained Models (MATCHING YOUR TRAINING LOGS)
    MODEL_PATH = os.path.join(BASE_DIR, "data/model.pkl")
    SECURITY_PATH = os.path.join(BASE_DIR, "data/security_model.pkl")

settings = Settings()