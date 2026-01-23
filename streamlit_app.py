import streamlit as st
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI CyberSafe Checker",
    layout="wide"
)

# ---------------- LOGIN ----------------
if "user" not in st.session_state:
    st.title("🛡️ AI CyberSafe Checker")
    st.caption("Powered by Ebiklean Global")
    st.write("AI-powered awareness against scams, fraud, and cyber threats")

    name = st.text_input("Enter your name to continue")

    if st.button("Login") and name.strip():
        st.session_state.user = name.strip()
        st.rerun()

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔐 Security Dashboard")
st.sidebar.success("Protection Active")
st.sidebar.write(f"👤 User: **{st.session_state.user}**")

# ---------------- MAIN ----------------
st.title("🛡️ AI CyberSafe Checker")
st.caption("Powered by Ebiklean Global")

st.info(
    "This tool helps you identify potential cyber threats. "
    "It does not replace professional cybersecurity services."
)

# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

def cyber_ai_response(text):
    text_lower = text.lower()

    if any(word in text_lower for word in ["otp", "urgent", "verify", "bank", "account"]):
        return (
            "🚨 **High Risk Alert**\n\n"
            "This message shows strong signs of phishing or scam.\n\n"
            "❌ Do NOT share OTPs\n"
            "❌ Do NOT click suspicious links\n"
            "✅ Verify from official sources"
        )

    return (
        "🧠 **Cyber Advice**\n\n"
        "Your message does not show obvious scam indicators, "
        "but always remain cautious online.\n\n"
        "✅ Use strong passwords\n"
        "✅ Enable 2FA\n"
        "✅ Verify links before clicking"
    )

# ---------------- CHAT UI ----------------
st.subheader("💬 Talk to CyberSafe AI")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Paste a suspicious message or ask a question")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    ai_reply = cyber_ai_response(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    st.rerun()

# ---------------- DOWNLOAD ----------------
st.divider()
st.subheader("⬇️ Download Cyber Report")

if st.button("Generate Report"):
    report = f"""
AI CYBERSAFE REPORT
Powered by Ebiklean Global

User: {st.session_state.user}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Conversation Log:
-----------------
"""

    for msg in st.session_state.messages:
        report += f"{msg['role'].upper()}:\n{msg['content']}\n\n"

    st.download_button(
        "Download Report",
        report,
        file_name="cybersafe_report.txt",
        mime="text/plain"
    )

# ---------------- FOOTER ----------------
st.caption("© 2026 Ebiklean Global • Secure Digital Living")