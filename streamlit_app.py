import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN SCREEN ----------------
if not st.session_state.logged_in:
    st.set_page_config(page_title="AI Health Checker Login", layout="centered")

    st.markdown("""
    <div style="text-align:center; padding:30px;">
        <h1>🩺 AI Health Checker</h1>
        <h4>Powered by <b>Ebiklean Global</b></h4>
        <p>AI-assisted health awareness & early risk insights</p>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Enter your name")

    if st.button("Login"):
        if username.strip():
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.warning("Please enter your name")

    st.stop()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Health Checker",
    page_icon="🩺",
    layout="wide"
)

FOUNDER = "Ebieme Bassey"
ORG = "Ebiklean Global"

# ---------------- LOAD MODEL SAFELY ----------------
@st.cache_resource
def load_health_model():
    try:
        return load_model("Health_model.h5")
    except:
        return None

model = load_health_model()

# ---------------- HEADER ----------------
st.markdown("""
<div style="
padding:25px;
border-radius:15px;
background:linear-gradient(90deg,#198754,#0dcaf0);
color:white;
text-align:center;
margin-bottom:25px;">
<h1>AI Health Checker 🩺</h1>
<h4>Powered by <b>Ebiklean Global</b></h4>
<p>AI-powered health awareness & early risk screening</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.success(f"Welcome {st.session_state.username}")

menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Health Check", "Dashboard", "DeepTech Portfolio"]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.experimental_rerun()

# ---------------- HOME ----------------
if menu == "Home":
    st.subheader("About AI Health Checker")
    st.write("""
    AI Health Checker is a lightweight AI application that helps users
    assess basic health risks using symptom-based inputs.

    ⚠️ This tool does NOT provide medical diagnosis.
    """)

# ---------------- HEALTH CHECK ----------------
elif menu == "Health Check":
    st.subheader("AI Health Assessment")

    age = st.number_input("Age", 1, 120, 30)
    fever = st.checkbox("Fever")
    cough = st.checkbox("Cough")
    fatigue = st.checkbox("Fatigue")
    headache = st.checkbox("Headache")

    if st.button("Run Health Check"):
        features = np.array([[age, fever, cough, fatigue, headache]], dtype=float)

        if model:
            risk_score = float(model.predict(features)[0][0])
        else:
            risk_score = sum([fever, cough, fatigue, headache]) / 4

        if risk_score > 0.7:
            st.error("⚠️ High health risk detected. Consult a medical professional.")
        elif risk_score > 0.4:
            st.warning("⚠️ Moderate health risk. Monitor symptoms.")
        else:
            st.success("✅ Low health risk detected.")

# ---------------- DASHBOARD ----------------
elif menu == "Dashboard":
    st.subheader("📊 Investor Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Users", "1,200+", "+140")
    col2.metric("Monthly Growth", "18%", "+4%")
    col3.metric("AI Confidence", "92%")
    col4.metric("Retention Rate", "67%")

    st.subheader("""
💰 Revenue Potential
""")
