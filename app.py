import streamlit as st
import json

st.set_page_config(page_title="SignalForge AI", layout="wide")

st.title("🧠 SignalForge AI — Autonomous Decision System")

# ================= SAMPLE DATA (replace with your agents) =================
inventory = [
    {"sku": "SKU-101", "stock": 120, "daily_sales": 90},
    {"sku": "SKU-102", "stock": 40, "daily_sales": 75},
]

supplier = "supply chain stable. no delays expected."
complaints = "delivery delayed again. item unavailable."

risk = 4
actions = [
    "Validate inventory",
    "Trigger emergency procurement",
    "Notify logistics team",
    "Update customers",
    "Start monitoring"
]

execution = [
    {"action": "Validate inventory", "status": "SUCCESS"},
    {"action": "Trigger emergency procurement", "status": "FAILED"},
    {"action": "Notify logistics team", "status": "SUCCESS"},
]

recovery = ["Fallback supplier activated"]

# ================= HEADER METRICS =================
col1, col2, col3 = st.columns(3)

col1.metric("Risk Score", risk)
col2.metric("Supplier Status", "STABLE")
col3.metric("Customer Signal", "HIGH RISK")

st.divider()

# ================= INPUT SECTION =================
st.subheader("📦 System Input")

c1, c2 = st.columns(2)

with c1:
    st.write("### Inventory")
    st.dataframe(inventory)

with c2:
    st.write("### Supplier Signal")
    st.info(supplier)
    st.write("### Complaints")
    st.warning(complaints)

st.divider()

# ================= DECISION ENGINE =================
st.subheader("🧠 Decision Engine")

if risk >= 3:
    st.error("HIGH RISK DETECTED")
else:
    st.success("SYSTEM STABLE")

st.code("""
Risk Logic:
+2 Customer complaints
+2 Inventory mismatch
+0 Supplier stable
Final Score = 4
""")

st.divider()

# ================= ACTION PLAN =================
st.subheader("🧠 Action Plan")

for a in actions:
    st.write(f"➡️ {a}")

st.divider()

# ================= EXECUTION =================
st.subheader("⚙️ Execution Layer")

for e in execution:
    if e["status"] == "SUCCESS":
        st.success(f"{e['action']} → SUCCESS")
    else:
        st.error(f"{e['action']} → FAILED")

st.divider()

# ================= RECOVERY =================
st.subheader("🛟 Recovery Layer")

for r in recovery:
    st.warning(r)

st.divider()

# ================= PIPELINE TIMELINE =================
st.subheader("📌 System Pipeline")

st.success("✔ Ingestion Completed")
st.success("✔ Conflict Detection Completed")
st.success("✔ Risk Engine Executed")
st.success("✔ Action Plan Generated")

if any(e["status"] == "FAILED" for e in execution):
    st.error("❌ Execution Failure Detected")
    st.warning("🟡 Recovery Triggered")

st.success("📁 Trace Saved")
