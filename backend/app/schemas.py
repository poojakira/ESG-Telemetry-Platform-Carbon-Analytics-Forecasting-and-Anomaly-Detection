from pydantic import BaseModel, ConfigDict

# INPUT: Data sent TO the API
class CarbonDataInput(BaseModel):
    raw_material_energy: float
    raw_material_emission_factor: float
    raw_material_waste: float
    manufacturing_energy: float
    manufacturing_efficiency: float
    manufacturing_water_usage: float
    transport_distance_km: float
    transport_mode_factor: float
    logistics_energy: float
    usage_energy_consumption: float
    usage_duration_hours: float
    grid_carbon_intensity: float
    recycling_efficiency: float
    disposal_emission_factor: float
    recovered_material_value: float
    state_complexity_index: float
    policy_action_score: float
    optimization_reward_signal: float

    # Fix for "protected_namespaces" warning
    model_config = ConfigDict(protected_namespaces=())

# OUTPUT: Data sent FROM the API
class PredictionOutput(BaseModel):
    predicted_carbon_footprint: float
    confidence_interval: list[float]
    anomaly_detected: bool
    model_version: str
    metadata: dict

    model_config = ConfigDict(protected_namespaces=())