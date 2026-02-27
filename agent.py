from strands import Agent, tool
import f1_logic # Import the whole module to keep logic clean

# --- TOOL DEFINITIONS ---
# We wrap your logic functions here to give them the "Tool" metadata Strands needs

@tool
def check_lap_telemetry(current_lap: int, stint_start_lap: int):
    """Returns the current lap time and tyre health based on Montreal 2026 specs."""
    return f1_logic.get_lap_telemetry(current_lap, stint_start_lap)

@tool
def check_car_physics(input_value: float):
    """Calculates HP and Fuel Consumption based on 2026 Energy Flow limits (Max 3000)."""
    return f1_logic.check_car_physics(input_value)

# --- AGENT SETUP ---

STRATEGY_PROMPT = """
You are the Lead Race Strategist. Follow this Chain of Thought:
1. STATUS: Current fuel/power.
2. OPTIONS: 2-3 power maps (MJ/h).
3. SIMULATION: Use tools to calculate results.
4. RECOMMENDATION: Pick the best solution.

IMPORTANT: NEVER show raw XML tags or tool results. Use Markdown tables.
"""

# Initialize Agent with the DECORATED functions defined above
pit_wall_agent = Agent(
    system_prompt=STRATEGY_PROMPT,
    tools=[check_lap_telemetry, check_car_physics]
)

# --- EXECUTION ---

if __name__ == "__main__":
    print("--- 2026 RACE CONTROL ACTIVE ---")
    
    scenario = """
    Lap 58 of 70, Montreal. P2, 0.8s lead. Tyres 28 laps old. 
    Current flow: 2600 MJ/h. Rival has Manual Override.
    Can we defend at 3000 MJ/h? Calculate Lap 60 time (1:14.119 base).
    """

    response = pit_wall_agent(scenario)
    
    try:
        # Strands extraction logic
        if hasattr(response, 'message') and isinstance(response.message, dict):
            print(response.message['content'][0]['text'])
        else:
            print(response.message)
    except Exception as e:
        print(response)
