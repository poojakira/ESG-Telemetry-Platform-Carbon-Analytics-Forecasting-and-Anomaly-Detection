# 📊 EcoTrack ESG Dataset Specification

The industrial nexus is engineered for high-frequency ESG (Environmental, Social, and Governance) telemetry.

## 1. Data Schema (Table: `ledger`)
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Primary key (Auto-increment) |
| `product_id` | String(100) | Unique identifier for the asset |
| `sku_name` | String(255) | Full industrial SKU name |
| `carbon_footprint` | Float | Primary carbon intensity metric (kg CO2e) |
| `region` | String(100) | Geographic sourcing origin (e.g., EU-West, US-East) |
| `timestamp` | DateTime | Ingestion telemetry timestamp (ISO 8601) |
| `merkle_hash` | String(64) | Cryptographic signature of the record |

## 2. Telemetry Ingestion Metrics
- **Volume**: 1,000,000+ records / month (Industrial target).
- **Frequency**: Real-time bursts (up to 100 Hz).
- **Format**: JSON Payload via Async POST API.

## 3. Data Integrity & Anchors
- **Merkle Roots**: Generated every 1000 records.
- **Root Audit Frequency**: Weekly full-ledger scan vs 3rd-party trust anchors.
