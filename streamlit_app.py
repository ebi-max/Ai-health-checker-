import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Load pre-trained model
model = load_model("model/health_model.h5")

# Define health condition classes
health_classes = ['Eczema', 'Psoriasis', 'Acne', 'Skin Infection', 'Normal']

# App title
st.title("🩺 AI Health Checker")
st.write("Upload an image of your skin condition or X-ray, and get a prediction and guidance.")

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # Preprocess image for model
    img = img.resize((224,224))
    img_array = np.array(img)/255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    predictions = model.predict(img_array)
    predicted_class = health_classes[np.argmax(predictions)]
    confidence = np.max(predictions) * 100

    # Display results
    st.subheader("🩺 Prediction Result")
    st.write(f"**Condition:** {predicted_class}")
    st.write(f"**Prediction Confidence:** {confidence:.2f}%")

    # Health guidance
    guidance = {
        'Eczema': "- Keep the area clean\n- Avoid scratching\n- Moisturize regularly\n- Consult dermatologist if persists",
        'Psoriasis': "- Use medicated creams\n- Avoid stress and triggers\n- Consult dermatologist",
        'Acne': "- Keep skin clean\n- Avoid oily products\n- See dermatologist if severe",
        'Skin Infection': "- Clean affected area\n- Avoid spreading\n- Consult healthcare provider",
        'Normal': "- No major concerns detected\n- Maintain healthy skincare"
    }

    st.subheader("💡 Health Guidance")
    st.write(guidance.get(predicted_class, "Consult a healthcare professional for more advice."))