# 📊 EcoTrack Observability & Monitoring

The EcoTrack Nexus uses a structured observability stack to ensure 99.9% industrial availability.

## 1. Structured Logging
Applied via `StructuredLogger` in JSON format.
- **Log Source**: `backend/app/logging_config.py`
- **Output**: `nexus_audit.log` (Rotated daily)
- **Tracing**: Each request is assigned a unique `request_id` for end-to-end tracing across async ingestion nodes.

## 2. Health & Metrics
- **Endpoint**: `/health`
- **Metrics**: 
  - `latency_ms`: Ingestion response time.
  - `merkle_verification_success`: Counter for ledger audits.
  - `model_drift_alarm`: Binary flag for ML drift detection.

## 3. Alerting Strategy
| Trigger | Severity | Action |
| :--- | :--- | :--- |
| **Ingestion Latency > 200ms** | WARNING | Autoscaling trigger |
| **Merkle Root Mismatch** | CRITICAL | Lock ledger / Alert Security Node |
| **API Rate Limit Exceeded (Burst)** | INFO | Notify Traffic Node |
| **DB Connection Lost** | CRITICAL | Initiate Backup/Replica Failover |
