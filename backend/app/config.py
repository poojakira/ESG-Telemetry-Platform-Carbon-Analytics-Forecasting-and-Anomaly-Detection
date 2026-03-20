import os

class Settings:
    # Absolute Reality: File-relative URI resolution
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 1. Path to the CSV Data
    DATA_PATH = os.path.join(BASE_DIR, "data/dpp_data.csv")

    # 2. Path to the Trained Models (MATCHING YOUR TRAINING LOGS)
    MODEL_PATH = os.path.join(BASE_DIR, "data/model.pkl")
    SECURITY_PATH = os.path.join(BASE_DIR, "data/security_model.pkl")

settings = Settings()