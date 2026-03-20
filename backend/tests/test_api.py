import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """ Verify the system health and node synchronization. """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["node"] == "Primary-Industrial-Nexus"

def test_get_metrics():
    """ Verify executive metrics aggregation and regional breakdown. """
    response = client.get("/api/v1/metrics?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "total_co2" in data
    assert "region_breakdown" in data

def test_get_forecast():
    """ Verify the Holt-Winters forecasting kernel output. """
    response = client.get("/api/v1/forecast")
    assert response.status_code == 200
    data = response.json()
    assert len(data["baseline_projection"]) == 12
    assert data["methodology"] == "Holt-Winters Single Exponential Smoothing"

def test_data_ingest():
    """ Verify the SHA-256 hash-chained ingestion pipeline. """
    payload = [{
        "sku_name": "Test PLC Unit",
        "category": "Industrial Logic Controllers",
        "region": "Test Hub",
        "vendor": "Test Vendor",
        "raw_material_energy": 100.0,
        "raw_material_emission_factor": 0.5,
        "raw_material_waste": 1.0,
        "manufacturing_energy": 200.0,
        "manufacturing_efficiency": 0.9,
        "manufacturing_water_usage": 500.0,
        "transport_distance_km": 100.0,
        "transport_mode_factor": 0.1,
        "logistics_energy": 10.0,
        "usage_energy_consumption": 50.0,
        "usage_duration_hours": 1000.0,
        "grid_carbon_intensity": 300.0,
        "recycling_efficiency": 0.8,
        "disposal_emission_factor": 0.05,
        "recovered_material_value": 10.0,
        "state_complexity_index": 1.0,
        "policy_action_score": 1.0,
        "optimization_reward_signal": 1.0
    }]
    response = client.post("/api/v1/data/ingest", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "verification_chain" in response.json()

def test_predict_endpoint():
    """ Verify the ML inference engine with anomaly detection. """
    payload = {
        "sku_name": "Test PLC Unit",
        "category": "Industrial Logic Controllers",
        "region": "Test Hub",
        "vendor": "Test Vendor",
        "raw_material_energy": 100.0,
        "raw_material_emission_factor": 0.5,
        "raw_material_waste": 1.0,
        "manufacturing_energy": 200.0,
        "manufacturing_efficiency": 0.9,
        "manufacturing_water_usage": 500.0,
        "transport_distance_km": 100.0,
        "transport_mode_factor": 0.1,
        "logistics_energy": 10.0,
        "usage_energy_consumption": 50.0,
        "usage_duration_hours": 1000.0,
        "grid_carbon_intensity": 300.0,
        "recycling_efficiency": 0.8,
        "disposal_emission_factor": 0.05,
        "recovered_material_value": 10.0,
        "state_complexity_index": 1.0,
        "policy_action_score": 1.0,
        "optimization_reward_signal": 1.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_carbon_footprint" in data
    assert "confidence_interval" in data
