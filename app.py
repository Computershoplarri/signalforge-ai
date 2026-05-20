import streamlit as st
import json
import os
from ingestion_agent import load_data
from contradiction_agent import detect_conflict
from planning_agent import generate_plan
from execution_agent import execute_actions
from recovery_agent import recover

# ✅ FIX: ensure logs folder exists
os.makedirs("logs", exist_ok=True)

st.set_page_config(page_title="SignalForge AI", layout="wide")

st.title("🧠 SignalForge AI — Autonomous Content-to-Action System")

# ================= RUN BUTTON =================
if st.button("🚀 Run Agent System"):

    timeline = []

    def add_step(name, status="DONE"):
        timeline.append({"step": name, "status": status})

    # ================= INGESTION =================
    df, supplier, complaints = load_data()
    add_step("Data Ingestion")

    # ================= INPUT DISPLAY =================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Inventory Data")
        st.dataframe(df)

    with col2:
        st.subheader("📡 Supplier Signal")
        st.write(supplier)

        st.subheader("🧾 Customer Complaints")
        st.write(complaints)

    # ================= CONTRADICTION =================
    result = detect_conflict(supplier, complaints)
    add_step("Contradiction Analysis")

    # ================= RISK ENGINE (FIXED - REAL LOGIC) =================
    risk = 0

    if result["conflict"]:
        risk += 2

    if "delayed" in complaints.lower() or "unavailable" in complaints.lower():
        risk += 1

    if df["stock"].sum() < df["daily_sales"].sum():
        risk += 1

    add_step(f"Risk Computed = {risk}")

    # ================= RISK UI =================
    st.subheader("⚠️ Risk Analysis")
    st.metric("Risk Score", risk)

    if risk >= 3:
        st.error("HIGH RISK DETECTED")
    else:
        st.success("SYSTEM STABLE")

    # ================= REASONING ENGINE =================
    st.subheader("🧠 Decision Reasoning Engine")

    st.info("Supplier Signal → Stable or Neutral")
    st.warning("Customer Complaints → Risk Contribution")
    st.error("Inventory Mismatch → High Risk Factor")

    st.code(f"""
Risk Breakdown:

+ Customer complaints (if any)
+ Inventory mismatch (if any)
+ Supplier stability (neutral)

Final Risk Score = {risk}
""")

    # ================= PLANNING =================
    actions = generate_plan(risk)
    add_step("Action Plan Generated")

    st.subheader("🧠 Action Plan")
    for a in actions:
        st.write("➡️", a)

    # ================= EXECUTION =================
    execution = execute_actions(actions)
    add_step("Execution Completed")

    st.subheader("⚙️ Execution Results")

    for e in execution:
        if e["status"] == "SUCCESS":
            st.success(f"{e['action']} → SUCCESS")
        else:
            st.error(f"{e['action']} → FAILED")

    # ================= RECOVERY =================
    recovery = recover(execution)

    if recovery:
        add_step("Failure Detected", "FAILED")
        add_step("Recovery Triggered", "RECOVERED")

        st.subheader("🛟 Recovery Actions")
        for r in recovery:
            st.warning(r)

    # ================= TIMELINE =================
    st.subheader("📌 Agent Timeline")

    for t in timeline:
        if t["status"] == "FAILED":
            st.error(f"❌ {t['step']}")
        elif t["status"] == "RECOVERED":
            st.warning(f"🟡 {t['step']}")
        else:
            st.success(f"✔ {t['step']}")

    # ================= TRACE LOG =================
    log_data = {
        "risk": risk,
        "conflict": result,
        "actions": actions,
        "execution": execution,
        "recovery": recovery,
        "timeline": timeline
    }

    with open("logs/agent_trace.json", "w") as f:
        json.dump(log_data, f, indent=2)

    st.success("📁 Trace saved successfully")
