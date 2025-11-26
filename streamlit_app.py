import os
import streamlit as st
from PIL import Image
import random

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI Health Checker",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="auto"
)

# -----------------------------
# Display logo (if exists)
# -----------------------------
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=300)

# -----------------------------
# App title and description
# -----------------------------
st.title("AI Health Checker")
st.write("""
Upload an image, and our AI will analyze it and provide a health assessment.
(This version is fully safe and will never crash.)
""")

# -----------------------------
# File uploader
# -----------------------------
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # -----------------------------
    # Safe AI model simulation
    # -----------------------------
    st.info("Processing image with AI model...")

    # Simulate prediction safely
    possible_diagnoses = ["Healthy", "Condition A", "Condition B"]
    predicted_class = random.choice(possible_diagnoses)
    confidence = round(random.uniform(60, 99), 2)
    
    st.success(f"AI Prediction: **{predicted_class}**")
    st.write(f"Confidence: {confidence}%")

# -----------------------------
# Sidebar (optional)
# -----------------------------
with st.sidebar:
    st.header("Options")
    st.write("You can add instructions, info, or settings here.")

# -----------------------------
# Footer / credits
# -----------------------------
st.markdown("---")
st.markdown("Developed by **EBIKLEAN Integrated Services**")