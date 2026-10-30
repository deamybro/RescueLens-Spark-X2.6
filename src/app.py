import os
import sys
import json
import streamlit as st

# Setup paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from engine import SparkTriageEngine
from schemas import EmergencyTriageResult

# Page Config
st.set_page_config(
    page_title="RescueLens | Spark-X2.6 Disaster Triage Engine",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #dc2626; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.05rem; color: #4b5563; margin-bottom: 1.2rem; }
    .metric-card { background: #f9fafb; padding: 1.2rem; border-radius: 0.5rem; border-left: 5px solid #dc2626; }
    .p1-badge { background-color: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 4px; font-weight: 700; }
    .p2-badge { background-color: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 4px; font-weight: 700; }
    .p3-badge { background-color: #d1fae5; color: #065f46; padding: 4px 10px; border-radius: 4px; font-weight: 700; }
    .thinking-box { background: #1e293b; color: #94a3b8; font-family: monospace; font-size: 0.85rem; padding: 12px; border-radius: 6px; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='main-header'>🚨 RescueLens (救援智标)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Humanitarian Emergency Triage & Decision-Support System powered by <b>Spark-X2.6-4B</b></div>", unsafe_allow_html=True)

# Load sample data
sample_path = os.path.join(CURRENT_DIR, "..", "data", "sample_emergencies.json")
samples = []
if os.path.exists(sample_path):
    with open(sample_path, "r", encoding="utf-8") as f:
        samples = json.load(f)

# Sidebar
st.sidebar.title("⚙️ Mission Settings")
st.sidebar.markdown("**Target Model**: `XHToken/Spark-X2.6-4B`")
st.sidebar.markdown("**Model Revision**: `d1b5f26071101c27fcd07728e7a7770e428281f4`")
st.sidebar.markdown("**Deployment Mode**: Low-latency CPU / Edge Triage")

st.sidebar.divider()
st.sidebar.subheader("📋 Pre-loaded Scenarios")
scenario_names = [f"{s['id']}: {s['disaster_type']}" for s in samples]
selected_scenario_idx = st.sidebar.selectbox("Choose realistic distress case:", range(len(scenario_names)), format_func=lambda i: scenario_names[i])

selected_sample = samples[selected_scenario_idx] if samples else None

# Main Layout
col_input, col_output = st.columns([1, 1.15], gap="large")

with col_input:
    st.subheader("📥 Incoming Distress Signal")
    
    with st.expander("Report Metadata", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            incident_id = st.text_input("Incident ID", value=selected_sample['id'] if selected_sample else "INC-CUSTOM-001")
            disaster_hint = st.text_input("Disaster Type Hint", value=selected_sample['disaster_type'] if selected_sample else "Flood")
        with c2:
            channel = st.selectbox("Ingestion Channel", ["SMS / Citizen Hotline", "Social Media (Crowdsourced)", "Emergency Radio Relay", "Community Shelter"], index=0)
            sender = st.text_input("Source / Contact", value=selected_sample['metadata']['sender_contact'] if selected_sample else "+1-555-HELP")

    raw_message = st.text_area(
        "Raw Unstructured Message / Transcript:",
        value=selected_sample['raw_text'] if selected_sample else "",
        height=180
    )

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        triage_btn = st.button("🚀 Analyze & Triage with Spark-X2.6", type="primary", use_container_width=True)
    with col_btn2:
        clear_btn = st.button("🔄 Reset", use_container_width=True)

with col_output:
    st.subheader("🎯 Structured Triage & Dispatch Plan")

    if triage_btn and raw_message:
        engine = SparkTriageEngine()
        with st.spinner("Spark-X2.6-4B is reasoning through distress signals..."):
            result, raw_generation = engine.triage_incident(incident_id, raw_message, channel=channel, disaster_hint=disaster_hint)

        # Priority Banner
        badge_cls = "p1-badge" if "P1" in result.priority_level else ("p2-badge" if "P2" in result.priority_level else "p3-badge")
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; background:#f3f4f6; padding:12px 16px; border-radius:8px; margin-bottom:15px;">
            <div>
                <span class='{badge_cls}'>{result.priority_level}</span>
                <span style="margin-left:12px; font-weight:600; font-size:1.1rem; color:#1f2937;">Urgency Score: {result.urgency_score}/10</span>
            </div>
            <div style="color:#6b7280; font-size:0.9rem;">
                Category: <b>{result.disaster_category}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info(f"**Dispatcher Summary**: {result.summary}")

        # Metrics & Key Info
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total People Affected", f"{result.demographics.total_people or 'Unspecified'}")
        with m2:
            st.metric("Vulnerable Individuals", f"{len(result.demographics.vulnerable_groups)} groups flagged")
        with m3:
            st.metric("Hazards Detected", f"{len(result.hazards_identified)} active")

        # Location Clues
        with st.container():
            st.markdown("##### 📍 Location & Landmarks Extracted")
            st.write(f"**Target Area**: `{result.location.raw_location_text}`")
            if result.location.landmarks:
                st.write("**Landmarks / Street Clues**:", ", ".join([f"`{lm}`" for lm in result.location.landmarks]))

        # Resource Requirements Table
        st.markdown("##### 📦 Critical Resource Allocation")
        if result.resources_required:
            res_data = [{"Category": r.category.upper(), "Urgency": r.urgency.upper(), "Details": r.details} for r in result.resources_required]
            st.table(res_data)
        else:
            st.write("No specialized equipment required at this time.")

        # Controllable Reasoning Display
        with st.expander("🧠 Spark-X2.6-4B Controllable Reasoning (<think> trace)", expanded=True):
            st.markdown(f"<div class='thinking-box'>{result.thinking_process}</div>", unsafe_allow_html=True)

        # Standard Humanitarian JSON Payload
        with st.expander("📄 Export Standardized EDXL / Humanitarian JSON"):
            st.code(result.model_dump_json(indent=2), language="json")

        # Human Verification Protocol Alert
        if result.human_verification_recommended:
            st.warning(f"⚠️ **Human-in-the-Loop Protocol**: {result.human_verification_notes}")

    else:
        st.markdown("""
        <div style="border: 2px dashed #cbd5e1; border-radius: 8px; padding: 40px; text-align: center; color: #64748b;">
            Select a scenario on the left and click <b>Analyze & Triage with Spark-X2.6</b> to view live triage reasoning, severity score, and automated resource matching.
        </div>
        """, unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 0.85rem;">
    HER Hack-Astron #7 | Spark-X2.6 Open Source AI for Good Challenge | Built for Emergency Responders & Dispatchers
</div>
""", unsafe_allow_html=True)
