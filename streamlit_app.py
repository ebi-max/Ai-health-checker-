import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI Health Checker", layout="wide")

            LOGIN 

if "user" not in st.session_state:
    st.title("🩺 AI Health Checker")
    st.caption("Powered by Ebiklean Global")

    name = st.text_input("Enter your name to continue")
    if st.button("Login") and name.strip():
        st.session_state.user = name
        st.rerun()
    st.stop()

         DASHBOARD

st.sidebar.title("📊 Dashboard")
st.sidebar.write(f"Welcome, **{st.session_state.user}**")
st.sidebar.success("Status: Active")

st.title("🩺 AI Health Checker")
st.caption("AI-assisted health awareness & early risk insights")

             CHAT 

if "messages" not in st.session_state:
    st.session_state.messages = []

def health_ai(text):
    return f"""
🩺 **Health Insight**

Based on your input (**{text}**), this may relate to lifestyle, hydration,
stress, rest, or nutrition.

⚠️ This is **not a diagnosis**. Please consult a healthcare professional if symptoms persist.
"""

st.subheader("💬 Chat with Health AI")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

msg = st.chat_input("Describe how you feel...")

if msg:
    st.session_state.messages.append({"role": "user", "content": msg})
    reply = health_ai(msg)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

          DOWNLOAD 

st.divider()
if st.button("⬇️ Download Health Report"):
    report = f"AI Health Checker Report\nUser: {st.session_state.user}\nDate: {datetime.now()}\n\n"
    for m in st.session_state.messages:
        report += f"{m['role'].upper()}: {m['content']}\n\n"

    st.download_button(
        "Download",
        report,
        file_name="health_report.txt"
    )

st.caption("© Powered by Ebiklean Global")