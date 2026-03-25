import requests # type: ignore
import json
import time
import random
import uuid

API_URL = "http://localhost:8000/api/v1/data/ingest"
AUTH_TOKEN = "your_admin_jwt_here" # Placeholder

def generate_sample_batch(size=50):
    batch = []
    for _ in range(size):
        batch.append({
            "sku_name": f"SKU-{str(uuid.uuid4()).split('-')[0].upper()}",
            "product_id": f"PRD-{random.randint(100, 999)}",
            "category": random.choice(["Electronics", "HVAC", "Logistics", "Energy"]),
            "vendor": f"Vendor-{random.choice(['Alpha', 'Beta', 'Gamma'])}",
            "region": random.choice(["US-East", "EU-West", "APAC-South"]),
            "raw_material_energy": random.uniform(50.0, 500.0),
            "manufacturing_energy": random.uniform(20.0, 300.0),
            "transport_distance_km": random.uniform(100.0, 5000.0),
            "usage_duration_hours": random.randint(1000, 20000)
        })
    return batch

def ingest_samples(total=1000, batch_size=100):
    print(f"🚀 Starting industrial ingestion of {total} records...")
    for i in range(0, total, batch_size):
        batch = generate_sample_batch(batch_size)
        try:
            # We skip auth check if running locally in dev mode with auth bypassed or using a real token
            response = requests.post(
                API_URL, 
                json=batch, 
                headers={"Authorization": f"Bearer {AUTH_TOKEN}"}
            )
            if response.status_code == 202:
                print(f"✅ Ingested batch {i//batch_size + 1}: {len(batch)} records.")
            else:
                print(f"⚠️ Batch {i//batch_size + 1} failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        time.sleep(0.1) # Simulate network gap

if __name__ == "__main__":
    ingest_samples(total=500, batch_size=100)
