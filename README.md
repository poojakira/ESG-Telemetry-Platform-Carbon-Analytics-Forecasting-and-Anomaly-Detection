# 🏛️ EcoTrack-Enterprise: Absolute Technical Reality v7.0.0

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Persistence-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Statsmodels](https://img.shields.io/badge/Statsmodels-Forecasting-013220)](https://www.statsmodels.org/)

EcoTrack-Enterprise is a deterministic, industrial-grade ESG (Environmental, Social, and Governance) platform designed for "Absolute Technical Reality." Purging all stochastic placeholders, v7.0.0 implements a verified SHA-256 hash-chain, persistent SQLite telemetry, and statistical Holt-Winters forecasting.

---

## 🏗️ Core Architecture: Absolute Reality

1.  **Immutable Ledger (SHA-256)**: Implements functional block-chaining. Each carbon record identifies its predecessor's hash, creating an auditable, non-repudiable audit trail.
2.  **Deterministic Intelligence**: Time-series projections are powered by **Holt-Winters Seasonal Smoothing** (via `statsmodels`), ensuring forecasts are data-driven reflections of history.
3.  **Industrial Persistence**: A dedicated **SQLite engine** handles all ingestion and telemetry, guaranteeing data continuity across node restarts.
4.  **High-Fidelity SKU Registry**: 200+ authentic industrial components from **Siemens, ABB, and GE** replace all synthetic placeholders.

---

## 🛰️ Technical API Reference (v7.0.0)

The backend provides a comprehensive suite of REST endpoints for industrial ESG management.

### **1. Executive Telemetry & Metrics**
`GET /api/v1/metrics`
- **Methodology**: Real-time aggregation of SQLite ledger state.
- **Parameters**: `limit` (int), `offset` (int) - Supports industrial-scale pagination.
- **Payload**: Aggregated CO2, average intensity, and regional node breakdown.

### **2. Neural Time-Series Forecasting**
`GET /api/v1/forecast`
- **Engine**: Statsmodels Holt-Winters Single Exponential Smoothing.
- **Output**: 12-period projection based on actual historical telemetry.

### **3. Immutable SHA-256 Ingestion**
`POST /api/v1/data/ingest`
- **Logic**: Generates a SHA-256 hash-chain block for the provided industrial telemetry.
- **Verification**: Returns a `verification_chain` string for immediate audit validation.

### **4. Strategic Data Portability**
`GET /api/v1/export`
- **Formats**: `csv`, `json`.
- **Use Case**: Exporting the full immutable ledger for external ISO audits.

### **5. Other Endpoints**
- `POST /predict`: ML Inference with Anomaly Detection (Isolation Forest).
- `GET /health`: Node synchronization status.
- `GET /api/v1/analytics/trends`: Topological categorical and vendor performance audits.

---

## 🚀 Deployment Guide

1.  **Infrastructure**:
    ```bash
    cd backend
    pip install -r requirements.txt
    python -m uvicorn app.main:app --reload
    ```
2.  **Executive Dashboard**:
    ```bash
    cd frontend
    streamlit run dashboard.py
    ```

---

## 🛡️ Stability & Verification
This platform includes an automated unit test suite. Run the audit via:
```bash
cd backend
python -m pytest tests/test_api.py
```

---
**Author**: Antigravity Engineering (v7.0.0 Absolute Reality)
