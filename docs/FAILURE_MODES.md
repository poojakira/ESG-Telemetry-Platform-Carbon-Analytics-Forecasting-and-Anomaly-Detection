# 🚨 EcoTrack Failure-Mode Analysis

This document describes technical system behavior during anomalous industrial events to ensure 100% data durability.

## 1. Database Failure (SQL Server / PostgreSQL)
- **Symptom**: `OperationalError` on write.
- **Recovery**: 
  - Async queue buffers up to 10,000 records in-memory.
  - Failover to Secondary Read-Replica.
  - Primary write retries with exponential backoff (Max 5 attempts).

## 2. Integrity Hash Mismatch
- **Symptom**: Merkle Root Verification `FAIL`.
- **Action**:
  - `SecurityNode` triggers immediate API Lock.
  - ISO-compliant audit trail generated for root-cause analysis (Log: `nexus_audit.log`).
  - System initiates local Ledger Re-sync from Trusted Cold Storage.

## 3. Malformed Payload Ingestion
- **Symptom**: JSON `ValidationError` (Pydantic).
- **Response**: `422 Unprocessable Entity` returned to source.
- **Prevention**: High-integrity schemas in `backend/app/schemas.py`.

## 4. Rate-Limit Saturation (DDoS / Burst)
- **Symptom**: Telemetry speed > 10 RPS.
- **Control**: `SlowAPI` returns `429 Too Many Requests`. 
- **Grace**: Burst buffer allows transient peaks of 20 RPS for 5 seconds.
