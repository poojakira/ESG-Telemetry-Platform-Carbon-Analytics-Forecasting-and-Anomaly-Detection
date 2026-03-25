# 🔐 EcoTrack API: Industrial Deep Dive

The EcoTrack Enterprise API is a high-integrity RESTful nexus built on FastAPI. This document provides developer guidance for industrial integration.

## 1. Authentication (JWT)
All non-public endpoints require a Bearer Token.
- **Endpoint**: `POST /api/v1/auth/login`
- **Logic**: Returns a scoped access token if credentials match the industrial registry.

## 2. Telemetry Ingestion
- **Endpoint**: `POST /api/v1/data/ingest`
- **Pattern**: Asynchronous Producer-Consumer. Returns `202 Accepted` immediately.
- **Rate Limit**: 10 requests / minute / IP.

## 3. Cryptographic Audit
- **Endpoint**: `GET /api/v1/ledger/verify-chain`
- **Output**: Returns the Merkle Root and full verification status of the immutable ledger.

## 4. Documentation Explorer
When running locally, access the interactive industrial explorer:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
