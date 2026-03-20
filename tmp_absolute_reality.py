import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib

DATA_PATH = r"c:\Users\pooja\Downloads\EcoTrack-Enterprise-main (3)\EcoTrack-Enterprise-main\EcoTrack-Enterprise\EcoTrack-Enterprise\backend\data\dpp_data.csv"

def generate_absolute_reality_data():
    # 1. Authentic Industrial Registry
    skus = [
        "Siemens Simatic S7-1500 Controller", "ABB IRB 6700 Industrial Robot", "Schneider Electric Altivar Variable Speed Drive",
        "Honeywell Experion PKS Controller", "Rockwell Automation Allen-Bradley ControlLogix", "Emerson DeltaV DCS Node",
        "Cisco IE-4010 Industrial Ethernet Switch", "General Electric Mark VIe Control System", "KUKA KR QUANTEC-2 Robot",
        "Mitsubishi Electric MELSEC iQ-R Series", "Beckhoff New Automation Technology PC", "Phoenix Contact PLCnext Controller",
        "Yokogawa CENTUM VP Integrated Production Control System", "Fanuc R-2000iC Industrial Robot", "Danfoss VLT AutomationDrive FC 302"
    ]
    
    categories = ['Industrial Logic Controllers', 'Robotic Assembly Systems', 'Variable Speed Drives', 'Industrial Networking High-Speed', 'Distributed Control Systems']
    regions = ['Frankfurt Logistics Hub', 'Texas Manufacturing Nexus', 'Shanghai Industrial District', 'Bangalore Tech Corridor', 'Ghent Automotive Cluster']
    vendors = ['Siemens AG', 'ABB Ltd', 'Schneider Electric SE', 'Rockwell Automation Inc', 'Honeywell International']
    
    num_records = 200
    data = []
    
    # Initialize Blockchain Hash
    prev_hash = "0" * 64
    
    base_time = datetime.now() - timedelta(days=365)
    
    for i in range(num_records):
        sku = np.random.choice(skus)
        category = np.random.choice(categories)
        region = np.random.choice(regions)
        vendor = np.random.choice(vendors)
        timestamp = base_time + timedelta(hours=i*12)
        
        # Numeric Sustainability Metrics (Deterministic random for base, then we'll use DB for ingest)
        raw_material_energy = np.random.uniform(50, 500)
        manufacturing_energy = np.random.uniform(100, 1000)
        transport_distance_km = np.random.uniform(100, 5000)
        grid_intensity = np.random.uniform(200, 600)
        
        # Total Carbon (simplified deterministic proxy for RL/Model training)
        total_carbon = (raw_material_energy * 0.45) + (manufacturing_energy * 0.65) + (transport_distance_km * 0.015) + (grid_intensity * 0.2)
        
        # Real Hash Chain (SHA-256)
        payload = f"{timestamp}|{sku}|{total_carbon}|{prev_hash}"
        record_hash = hashlib.sha256(payload.encode()).hexdigest()
        
        data.append({
            "Timestamp": timestamp.isoformat(),
            "Product_ID": f"SKU-{10000+i}",
            "SKU_Name": sku,
            "Category": category,
            "Region": region,
            "Vendor": vendor,
            "raw_material_energy": round(raw_material_energy, 2),
            "raw_material_emission_factor": 0.55,
            "raw_material_waste": 12.5,
            "manufacturing_energy": round(manufacturing_energy, 2),
            "manufacturing_efficiency": 0.88,
            "manufacturing_water_usage": 1500,
            "transport_distance_km": round(transport_distance_km, 2),
            "transport_mode_factor": 0.12,
            "logistics_energy": 120,
            "usage_energy_consumption": 450,
            "usage_duration_hours": 8000,
            "grid_carbon_intensity": round(grid_intensity, 2),
            "recycling_efficiency": 0.65,
            "disposal_emission_factor": 0.08,
            "recovered_material_value": 45.0,
            "state_complexity_index": 1.2,
            "policy_action_score": 0.95,
            "optimization_reward_signal": 0.88,
            "total_lifecycle_carbon_footprint": round(total_carbon, 2),
            "Hash": record_hash,
            "Prev_Hash": prev_hash,
            "lat": np.random.uniform(-40, 60),
            "lon": np.random.uniform(-120, 140)
        })
        
        prev_hash = record_hash
        
    df = pd.DataFrame(data)
    df.to_csv(DATA_PATH, index=False)
    print(f"✅ Absolute Reality Dataset generated: {len(df)} records.")

if __name__ == "__main__":
    generate_absolute_reality_data()
