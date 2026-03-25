# 🧬 EcoTrack System Internals

Deep-dive into the technical architecture of the EcoTrack Industrial Nexus.

## 1. Merkle Ledger Engine
- **Hash Function**: SHA-3 (Keccak-256) for quantum-resistant anchoring.
- **Tree Type**: Binary Merkle Tree with canonical sorting of leave hashes.
- **Verification Complexity**: $O(\log N)$ (Sequential scan is $O(N)$).

## 2. ML Ensemble Strategy
- **ARIMA (Statistical)**: Captures seasonal trends (Daily/Weekly) in carbon intensity.
- **XGBoost (Relational)**: Uses SKU, Region, and Vendor features for high-recall forecasting.
- **Hyperparameters**: 
  - XGBoost: `n_estimators=100`, `max_depth=5`, `learning_rate=0.1`.
  - ARIMA: `order=(1,1,1)`, `seasonal_order=(1,1,0,24)`.

## 3. Database Schema (Table: `users`)
| Column | Type | Security |
| :--- | :--- | :--- |
| `username` | String | Unique Index |
| `hashed_password` | String | Argon2id / BCrypt |
| `role` | Enum | RBAC: Auditor, Operator, Executive |
