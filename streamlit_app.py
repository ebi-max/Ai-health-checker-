
import streamlit as st
from datetime import datetime
import json

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="AI Health Checker",
    page_icon="🩺",
    layout="centered"
)

# ---------------------------------
# Header / Branding
# ---------------------------------
st.markdown("""
<h2 style="text-align:center;">🩺 AI Health Checker</h2>
<p style="text-align:center; font-weight:bold;">Powered by Ebiklean Global</p>
<p style="text-align:center;">AI-assisted health awareness & early risk insights</p>
<hr>
""", unsafe_allow_html=True)

# ---------------------------------
# Session State Init
# ---------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------------------------
# Login (Simple & Safe)
# ---------------------------------
if st.session_state.user is None:
    name = st.text_input("Enter your name to continue")
    if st.button("Login"):
        if name.strip():
            st.session_state.user = name
            st.rerun()
        else:
            st.warning("Please enter your name")
    st.stop()

st.success(f"Welcome, {st.session_state.user} 👋")

# ---------------------------------
# Notifications
# ---------------------------------
st.info("🔔 Tip: This tool provides awareness, not medical diagnosis.")

# ---------------------------------
# Health Input
# ---------------------------------
st.subheader("🧾 Health Check Form")

age = st.number_input("Age", 1, 120, 25)
weight = st.number_input("Weight (kg)", 1.0, 300.0, 70.0)
height = st.number_input("Height (cm)", 50.0, 250.0, 170.0)

bp = st.selectbox("Blood Pressure Level", ["Normal", "Elevated", "High"])
activity = st.selectbox("Daily Activity Level", ["Low", "Moderate", "High"])

# ---------------------------------
# Classification Logic (Safe)
# ---------------------------------
def classify_health(age, bp, activity):
    if bp == "High" or age > 60:
        return "High Risk", "⚠️ Consult a healthcare professional."
    elif activity == "Low":
        return "Moderate Risk", "⚠️ Increase physical activity."
    else:
        return "Low Risk", "✅ Maintain healthy habits."

# ---------------------------------
# Run Assessment
# ---------------------------------
if st.button("Run AI Health Check"):
    risk, advice = classify_health(age, bp, activity)

    st.subheader("🧠 AI Health Result")
    st.write(f"**Risk Level:** {risk}")
    st.write(f"**Advice:** {advice}")

    report = {
        "Name": st.session_state.user,
        "Age": age,
        "Weight": weight,
        "Height": height,
        "Blood Pressure": bp,
        "Activity Level": activity,
        "Risk Level": risk,
        "Advice": advice,
        "Generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    st.download_button(
        "📥 Download Health Report",
        json.dumps(report, indent=4),
        file_name="ai_health_report.json",
        mime="application/json"
    )

# ---------------------------------
# Gallery (Lightweight)
# ---------------------------------
st.markdown("---")
st.subheader("🖼 Health Awareness Gallery")

st.image(
    [
        "https://images.unsplash.com/photo-1535914254981-b5012eebbd15",
        "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b"
    ],
    caption=["Healthy Lifestyle", "Daily Exercise"],
    use_column_width=True
)

# ---------------------------------
# Chat (Session-based)
# ---------------------------------
st.markdown("---")
st.subheader("💬 Health Assistant Chat")

user_msg = st.text_input("Ask a health-related question")

if st.button("Send"):
    if user_msg:
        st.session_state.chat.append(("You", user_msg))
        st.session_state.chat.append(
            ("AI", "I provide general health guidance. Please consult a professional for medical advice.")
        )

for sender, msg in st.session_state.chat:
    st.write(f"**{sender}:** {msg}")

# ---------------------------------
# Investor / Impact Dashboard
# ---------------------------------
st.markdown("---")
st.subheader("📊 Impact & Investor Snapshot")

c1, c2, c3 = st.columns(3)

c1.metric("Target Users", "Individuals")
c2.metric("Use Case", "Preventive Health")
c3.metric("Scalability", "High")

st.info(
    "This AI Health Checker promotes early health awareness and preventive action. "
    "Designed for NGOs, communities, and digital health initiatives."
)

# ---------------------------------
# Link to CyberSafe Checker
# ---------------------------------
st.markdown("---")
st.subheader("🔐 Explore Other Tools")

st.markdown(
    "➡️ **AI CyberSafe Checker** – Digital safety & phishing awareness platform."
)

# ---------------------------------
# Footer
# ---------------------------------
st.markdown("""
<hr>
<p style="text-align:center; font-size:12px;">
© 2026 Ebiklean Global • AI for Social Good
</p>
""", unsafe_allow_html=True)