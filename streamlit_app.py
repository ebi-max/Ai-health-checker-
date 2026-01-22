import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Health Checker",
    page_icon="🩺",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "name" not in st.session_state:
    st.session_state.name = ""

# ---------------- LOGIN SCREEN ----------------
if not st.session_state.logged_in:
    st.title("🩺 AI Health Checker")
    st.caption("AI-assisted health awareness & early risk insights")
    st.markdown("**Powered by Ebiklean Global**")

    name = st.text_input("Enter your name")

    if st.button("Login"):
        if name.strip() == "":
            st.warning("Please enter your name to continue.")
        else:
            st.session_state.name = name
            st.session_state.logged_in = True
            st.rerun()

# ---------------- MAIN APP ----------------
else:
    st.sidebar.success(f"Logged in as {st.session_state.name}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🩺 AI Health Checker")
    st.markdown("**Powered by Ebiklean Global**")

    st.subheader("Health Check Form")

    fever = st.checkbox("Fever")
    cough = st.checkbox("Cough")
    fatigue = st.checkbox("Fatigue")
    headache = st.checkbox("Headache")

    if st.button("Check Health"):
        # Convert booleans to numbers
        fever_n = int(fever)
        cough_n = int(cough)
        fatigue_n = int(fatigue)
        headache_n = int(headache)

        # Simple risk calculation (lightweight & safe)
        risk_score = (fever_n + cough_n + fatigue_n + headache_n) / 4

        st.success("Health analysis complete")
        st.write(f"### Estimated Risk Score: **{risk_score * 100:.1f}%**")

        if risk_score >= 0.75:
            st.error("High risk detected. Please consult a healthcare professional.")
        elif risk_score >= 0.4:
            st.warning("Moderate risk detected. Monitor your symptoms closely.")
        else:
            st.success("Low risk detected. Maintain healthy habits.")

        # ---------------- DOWNLOADABLE REPORT ----------------
        report = f"""
🩺 AI HEALTH CHECKER REPORT
Powered by Ebiklean Global

Name: {st.session_state.name}

Symptoms:
- Fever: {fever}
- Cough: {cough}
- Fatigue: {fatigue}
- Headache: {headache}

Estimated Risk Score: {risk_score * 100:.1f}%

Disclaimer:
This AI tool provides health awareness and early risk insights only.
It is NOT a medical diagnosis.
"""

        st.download_button(
            label="📥 Download Health Report",
            data=report,
            file_name="ai_health_report.txt",
            mime="text/plain"
        )

    st.divider()
    st.subheader("💰 Investor & Impact Overview")
    st.write(
        """
        - Growing demand for AI-assisted health awareness tools  
        - Scalable across mobile & web platforms  
        - Potential use cases: NGOs, schools, community health programs  
        """
    )
