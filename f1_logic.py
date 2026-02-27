# f1_logic.py - Core Physics and Simulation for F1 2026 Agent v1.0

# --- FIA 2026 CONSTRAINTS & CONSTANTS ---
FIA_CONSTRAINTS = {
    "MAX_ENERGY_FLOW_MJ_H": 3000.0,  # MJ/h limit (2026 Regs)
    "FUEL_ENERGY_DENSITY": 44.0,     # MJ/kg for sustainable fuel
    "MGU_K_MAX_POWER_KW": 350.0,     # Max electric deployment
    "MGU_K_RECOVERY_LAP": 8.5,       # Max recovery per lap (MJ)
}

# --- MONTREAL 2025/2026 TRACK DATA ---
TRACK_DATA = {
    "NAME": "Circuit Gilles Villeneuve",
    "TOTAL_LAPS": 70,
    "LAP_DISTANCE_KM": 4.361,
    "BASE_LAP_TIME": 76.119,         # 1:14.119 (2025) + 2.0s (2026 Delta)
    "PIT_LOSS_SECONDS": 18.5,        # Time lost during a pit stop
}

# --- TYRE DEGRADATION CONFIG ---
# Simple linear model for GitHub v1.0
TYRE_SETTINGS = {
    "DEG_PER_LAP": 0.12,             # Seconds lost per lap on Mediums
    "CRITICAL_HEALTH_PCT": 30.0,     # Suggest "BOX" below this
}

def check_car_physics(target_flow_mj_h: float):
    """
    Calculates HP and Fuel Consumption based on 2026 Energy Flow limits.
    """
    # Clip to FIA limit
    flow = min(target_flow_mj_h, FIA_CONSTRAINTS["MAX_ENERGY_FLOW_MJ_H"])
    
    # 1 MJ/h = 1/3.6 kW
    power_kw = flow / 3.6
    hp = power_kw * 1.34102
    
    # Fuel flow in kg/s
    fuel_kg_s = (flow / 3600) / FIA_CONSTRAINTS["FUEL_ENERGY_DENSITY"]
    
    return {
        "status": "Legal" if target_flow_mj_h <= 3000 else "Clipped to 3000",
        "power_output_hp": round(hp, 2),
        "fuel_burn_kg_s": round(fuel_kg_s, 5)
    }

def get_lap_telemetry(current_lap: int, stint_start_lap: int):
    """
    Simulates lap time and tyre health based on the 2026 Montreal baseline.
    """
    tyre_age = current_lap - stint_start_lap
    
    # Calculate performance drop
    pace_penalty = tyre_age * TYRE_SETTINGS["DEG_PER_LAP"]
    current_lap_time = TRACK_DATA["BASE_LAP_TIME"] + pace_penalty
    
    # Calculate tyre health (estimated 25 lap lifespan for Mediums)
    health = max(0, 100 - (tyre_age * 4)) 
    
    return {
        "lap_time_seconds": round(current_lap_time, 3),
        "tyre_health_pct": health,
        "recommendation": "BOX" if health < TYRE_SETTINGS["CRITICAL_HEALTH_PCT"] else "STAY OUT"
    }

def calculate_fuel_requirement(laps_remaining: int, current_flow_mj_h: float):
    """
    Estimates total fuel needed to finish the race.
    """
    # Assuming average lap is ~80s for fuel math
    avg_lap_duration_s = 80.0 
    fuel_per_s = (current_flow_mj_h / 3600) / FIA_CONSTRAINTS["FUEL_ENERGY_DENSITY"]
    
    total_needed = laps_remaining * (avg_lap_duration_s * fuel_per_s)
    return round(total_needed, 2)
