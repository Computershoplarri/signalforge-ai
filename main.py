import json
import datetime

from agents.ingestion_agent import load_data
from agents.contradiction_agent import detect_conflict
from agents.planning_agent import generate_plan
from agents.execution_agent import execute_actions
from agents.recovery_agent import recover

logs = []

def log(agent, msg):
    logs.append({
        "time": str(datetime.datetime.now()),
        "agent": agent,
        "message": msg
    })

# 1. INGESTION
df, supplier, complaints = load_data()
log("ingestion_agent", "Data loaded")

# 2. CONTRADICTION
result = detect_conflict(supplier, complaints)
log("contradiction_agent", result["reason"])

# 3. RISK
risk = 4 if result["conflict"] else 1
log("planning_agent", f"Risk calculated: {risk}")

# 4. PLANNING
actions = generate_plan(risk)
log("planning_agent", f"Actions generated: {len(actions)}")

# 5. EXECUTION
results = execute_actions(actions)

for r in results:
    log("execution_agent", f"{r['action']} → {r['status']}")

# 6. RECOVERY
recovery = recover(results)

for r in recovery:
    log("recovery_agent", r)

# 7. OUTPUT
print("\n=== ACTIONS ===")
print(actions)

print("\n=== EXECUTION ===")
print(results)

print("\n=== RECOVERY ===")
print(recovery)

# 8. SAVE TRACE LOGS
with open("logs/agent_trace.json", "w") as f:
    json.dump(logs, f, indent=2)

print("\nTRACE SAVED ✔")