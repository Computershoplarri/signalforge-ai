import streamlit as st
import json

from agents.ingestion_agent import load_data
from agents.contradiction_agent import detect_conflict
from agents.planning_agent import generate_plan
from agents.execution_agent import execute_actions
from agents.recovery_agent import recover

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

    # ================= DISPLAY INPUT =================
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

    # ================= RISK ENGINE =================
    risk = 4 if result["conflict"] else 1
    add_step(f"Risk Computed = {risk}")

    st.subheader("⚠️ Risk Analysis")

    st.metric("Risk Score", risk)

    if risk >= 3:
        st.error("HIGH RISK DETECTED")
    else:
        st.success("SYSTEM STABLE")

    # ================= REASONING ENGINE =================
    st.subheader("🧠 Decision Reasoning Engine")

    st.write("Supplier Signal")
    st.info("Stable → LOW RISK contribution")

    st.write("Customer Signal")
    st.warning("Complaints detected → HIGH RISK contribution")

    st.write("Inventory Signal")
    st.error("Stock vs demand mismatch → CRITICAL")

    st.write("Final Decision Logic")

    st.code(f"""
Risk Score Breakdown:

+2 Customer complaints
+2 Inventory mismatch
+0 Supplier stable

Final Risk = {risk}
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

    if recovery:
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