import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime

# Allow import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.predict import predict_next_6_hours
from src.optimizer import menu_recommendation

st.set_page_config(
    page_title="Airport Lounge Intelligence Engine",
    page_icon="✈",
    layout="wide"
)

# =========================
# PREMIUM UI
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
h1 { text-align: center; font-weight: bold; }
h2, h3 { color: #00c6ff; }
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 0 18px rgba(0,198,255,0.4);
}
div[data-testid="stAlert"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("✈ Airport Lounge Peak-Hour Intelligence Engine")
st.caption(f"🕒 Live Monitoring | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.success("AI Model Active | Flight-Schedule-Aware Forecasting Enabled")
st.divider()

# =========================
# BASE HISTORICAL PREDICTIONS
# =========================
base_predictions = predict_next_6_hours()

# =========================
# FLIGHT SCHEDULE INTEGRATION
# =========================
st.subheader("✈ Incoming Flight Schedule (Next 6 Hours)")

col1, col2, col3 = st.columns(3)

with col1:
    flights_per_hour = st.slider("Flights Arriving per Hour", 1, 15, 6)

with col2:
    avg_aircraft_capacity = st.slider("Average Aircraft Capacity", 100, 400, 180)

with col3:
    lounge_access_rate = st.slider("Passengers Using Lounge (%)", 5, 40, 15)

# Passenger inflow calculation
flight_passengers = flights_per_hour * avg_aircraft_capacity
expected_lounge_passengers = flight_passengers * (lounge_access_rate / 100)
flight_adjustment = expected_lounge_passengers / 6

adjusted_predictions = [
    int(p + flight_adjustment)
    for p in base_predictions
]

st.divider()

# =========================
# DYNAMIC CONFIDENCE INTERVAL
# =========================
historical = pd.read_csv("data/raw/lounge_data.csv")
recent_std = historical["crowd"].tail(48).std()

peak_crowd = int(max(adjusted_predictions))
confidence_margin = int(recent_std)

lower_bound = peak_crowd - confidence_margin
upper_bound = peak_crowd + confidence_margin

current_crowd = int(adjusted_predictions[0])
max_capacity = 200
utilization = (peak_crowd / max_capacity) * 100

# =========================
# MULTI-ROLE STAFFING
# =========================
def multi_role_staffing(crowd):
    service_staff = int(crowd / 25)
    kitchen_staff = int(crowd / 40)
    cleaning_staff = int(crowd / 60)
    total_staff = service_staff + kitchen_staff + cleaning_staff
    return service_staff, kitchen_staff, cleaning_staff, total_staff

service, kitchen, cleaning, total_staff = multi_role_staffing(peak_crowd)

# =========================
# KPI DISPLAY
# =========================
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Current Crowd", current_crowd)
col2.metric("Peak Crowd", peak_crowd)
col3.metric("Capacity Usage", f"{utilization:.1f}%")
col4.metric("Forecast Range", f"{lower_bound}-{upper_bound}")
col5.metric("Confidence Margin", f"±{confidence_margin}")

st.divider()

# =========================
# SURGE DETECTION
# =========================
st.subheader("🚨 Surge Intelligence")

growth_rates = np.diff(adjusted_predictions)
max_growth = max(growth_rates)

if max_growth > 25:
    st.error("Rapid surge growth detected! Pre-emptive staffing recommended.")
elif max_growth > 15:
    st.warning("Moderate surge acceleration detected.")
else:
    st.success("Stable growth pattern observed.")

st.divider()

# =========================
# GUEST EXPERIENCE SCORE
# =========================
total_service_capacity = service * 20
service_score = max(0, 100 - max(0, peak_crowd - total_service_capacity))

st.subheader("⭐ Guest Experience Prediction")
st.metric("Service Quality Score", f"{service_score}%")

st.divider()

# =========================
# SMART CATERING
# =========================
data = []
for i, crowd in enumerate(adjusted_predictions):
    snacks, drinks, meals = menu_recommendation(crowd)
    data.append({
        "Hour": i+1,
        "Crowd": crowd,
        "Snacks": snacks,
        "Drinks": drinks,
        "Meals": meals
    })

df = pd.DataFrame(data)

st.subheader("🍽 Smart Catering Optimization")
st.dataframe(df)

traditional_snacks = 150 * 6
ai_snacks = sum(df["Snacks"])
waste_reduction = max(0, traditional_snacks - ai_snacks)
sustainability_score = min(100, (waste_reduction / traditional_snacks) * 100)

st.metric("Food Waste Reduction", f"{waste_reduction} units")
st.metric("Sustainability Score", f"{sustainability_score:.1f}%")

st.divider()

# =========================
# COST OPTIMIZATION (FIXED LOGIC)
# =========================
st.subheader("💰 Cost Optimization")

avg_staff_cost = 500

# Traditional approach assumes buffer staffing (realistic airport behavior)
traditional_staff_baseline = 15
traditional_cost = traditional_staff_baseline * avg_staff_cost * 6

ai_cost = total_staff * avg_staff_cost * 6
savings = traditional_cost - ai_cost

col1, col2, col3 = st.columns(3)
col1.metric("AI Optimized Cost (6H)", f"₹{ai_cost}")
col2.metric("Traditional Buffered Cost (6H)", f"₹{traditional_cost}")
col3.metric("Operational Savings", f"₹{savings}")

st.divider()

# =========================
# HISTORICAL TREND
# =========================
st.subheader("📊 Historical Learning Trend")
st.line_chart(historical["crowd"].tail(168))

st.caption("Model trained on historical lounge entry data combined with flight schedule impact signals.")

st.divider()

# =========================
# ENTERPRISE SCALABILITY
# =========================
st.subheader("🚀 Enterprise Scalability")

st.markdown("""
- Explicit flight schedule integration  
- Passenger inflow modeling  
- Multi-role workforce optimization  
- Dynamic confidence estimation  
- Sustainability analytics  
- API-ready cloud architecture  
""")