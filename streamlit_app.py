# streamlit_app.py
import streamlit as st
from PIL import Image, ImageStat
import numpy as np
import io
import os
import math

st.set_page_config(page_title="AI Health Checker", layout="centered")

# --------- Utilities & Heuristics ---------
HEALTH_CLASSES = ['Normal', 'Rash', 'Wound', 'Swelling', 'Infection']

def analyze_image(img: Image.Image):
    """Return a dict of heuristic scores for each class from the image."""
    # ensure RGB
    img = img.convert("RGB")
    # Resize small for speed
    small = img.resize((150, 150))
    arr = np.array(small).astype(np.float32)
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    # brightness and redness measures
    mean_r = r.mean()
    mean_g = g.mean()
    mean_b = b.mean()
    mean_gray = ((r + g + b) / 3.0).mean()
    redness = mean_r - (mean_g + mean_b) / 2.0  # positive if R dominates
    saturation = np.std(arr / 255.0) * 255

    # edge / texture (rough estimate): variance of grayscale
    gray = (r + g + b) / 3.0
    texture = gray.std()

    # dark / blood-like colors
    dark_ratio = np.mean((r < 80) & (g < 80) & (b < 80))

    # basic heuristics to produce scores 0..1
    scores = {k: 0.0 for k in HEALTH_CLASSES}

    # Rash: strong redness, moderate brightness
    rash_score = np.clip((redness + 10) / 60.0, 0.0, 1.0)
    scores['Rash'] = float(rash_score)

    # Infection: redness + texture + slightly darker areas
    infection_score = np.clip((redness / 50.0) + (texture / 50.0) + (dark_ratio * 1.2), 0.0, 1.0)
    scores['Infection'] = float(np.clip(infection_score * 0.9, 0.0, 1.0))

    # Wound: dark spots + high texture/variance (cuts / scabs)
    wound_score = np.clip((texture / 60.0) + (dark_ratio * 2.0), 0.0, 1.0)
    scores['Wound'] = float(wound_score)

    # Swelling: low redness but noticeable brightness difference and smooth area (heuristic)
    # We'll detect swelling when image is brighter than average and texture low
    swelling_score = np.clip(((mean_gray - 100) / 120.0) - (texture / 120.0), 0.0, 1.0)
    scores['Swelling'] = float(swelling_score)

    # Normal: inverse of any suspicious signals
    suspicious = max(scores['Rash'], scores['Infection'], scores['Wound'], scores['Swelling'])
    scores['Normal'] = float(np.clip(1.0 - suspicious, 0.0, 1.0))

    # normalize sum to at most 1 (soft)
    total = sum(scores.values())
    if total > 0:
        # scale to keep values interpretable but not strictly probability
        for k in scores:
            scores[k] = float(scores[k] / (total + 1e-9) * min(total, 1.0))

    return scores

def analyze_text(text: str):
    """Return a dict of heuristic scores for each class from the symptom text."""
    text = (text or "").lower()
    tokens = text.replace(',', ' ').replace('/', ' ').split()
    scores = {k: 0.0 for k in HEALTH_CLASSES}

    # keyword groups
    kw = {
        'Rash': ['rash', 'itch', 'itchy', 'red', 'redness', 'skin rash', 'hives'],
        'Wound': ['cut', 'wound', 'bleed', 'bleeding', 'cutting', 'laceration', 'scab'],
        'Swelling': ['swelling', 'swollen', 'puffy', 'inflamed', 'bump', 'swells'],
        'Infection': ['infection', 'pus', 'pusy', 'fever', 'hot', 'warm', 'pain', 'abscess'],
        'Normal': ['ok', 'normal', 'fine', 'no problem', 'no pain', 'healthy']
    }

    # simple scoring: count keyword hits (capped)
    for cls, keys in kw.items():
        hits = 0
        for k in keys:
            if k in text:
                hits += 1
        scores[cls] = float(min(hits, 3) / 3.0)  # 0..1 based on hits

    # small fallback: if user mentions 'cough' or 'stomach' keep normal low but not used here
    # normalize so top can remain meaningful
    return scores

def combine_scores(image_scores: dict, text_scores: dict, text_present: bool):
    """
    Combine image and text scores into final scores.
    If text is present, weight text more (0.7 text, 0.3 image).
    Otherwise use image only.
    """
    final = {k: 0.0 for k in HEALTH_CLASSES}
    if text_present and any(v > 0 for v in text_scores.values()):
        tw = 0.7
        iw = 0.3
    else:
        tw = 0.0
        iw = 1.0

    for k in HEALTH_CLASSES:
        final[k] = float(text_scores.get(k, 0.0) * tw + image_scores.get(k, 0.0) * iw)

    # soft-normalize to sum 1
    s = sum(final.values())
    if s <= 0:
        # fallback: normal
        final['Normal'] = 1.0
    else:
        for k in final:
            final[k] = float(final[k] / s)

    return final

def pretty_prediction(final_scores):
    # choose top class
    top = max(final_scores.items(), key=lambda x: x[1])
    label, score = top[0], top[1]
    confidence = float(score * 100)
    # ensure between 0..100
    confidence = max(0.0, min(100.0, confidence))
    return label, confidence

# Guidance messages
GUIDANCE = {
    'Rash': [
        "Keep the area clean and dry.",
        "Avoid scratching; try cold compresses for relief.",
        "Use gentle, fragrance-free moisturizers.",
        "If it worsens or shows signs of infection, see a dermatologist."
    ],
    'Wound': [
        "Clean the wound with mild soap and water.",
        "Apply an antiseptic and cover with a sterile dressing.",
        "Seek medical attention if bleeding is heavy or doesn't stop.",
        "Watch for signs of infection (increasing pain, pus, fever)."
    ],
    'Swelling': [
        "Elevate the affected area when possible.",
        "Apply cold compresses to reduce swelling.",
        "Avoid tight clothing/jewelry over the area.",
        "Consult a healthcare provider if swelling is severe or sudden."
    ],
    'Infection': [
        "Wash the area gently and avoid squeezing.",
        "Warm compresses may help drainage (if directed by a clinician).",
        "If you have fever, increasing pain, or spreading redness, seek medical care.",
        "Antibiotics may be required — consult a healthcare provider."
    ],
    'Normal': [
        "No major concerns detected from the provided input.",
        "Maintain good hygiene and observe the area for changes.",
        "If you feel unsure, consult a healthcare professional."
    ]
}

# --------- Streamlit Interface ---------
st.image("assets/logo.png" if os.path.exists("assets/logo.png") else None, width=300)
st.title("🩺 AI Health Checker — Lightweight (Image + Symptoms)")
st.write("Upload a photo (skin/X-ray/affected area) and optionally describe symptoms. "
         "This app uses lightweight heuristics (not a medical diagnosis).")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("Upload image (jpg, png)", type=['jpg', 'jpeg', 'png'])
    use_camera = st.checkbox("Use camera (mobile)", value=False)
    if use_camera:
        # Streamlit's camera_input is available in newer versions; try gracefully
        try:
            cam = st.camera_input("Take a photo")
            if cam is not None and uploaded_file is None:
                # prefer camera capture if provided
                uploaded_file = cam
        except Exception:
            pass

with col2:
    symptoms = st.text_area("Describe symptoms (e.g., 'red, itchy rash and fever')", height=140)
    st.markdown("**Tip:** Mention keywords like 'rash', 'cut', 'swelling', 'fever', 'pus' for better results.")

run_btn = st.button("Analyze")

if run_btn:
    # Basic input validation
    if uploaded_file is None and (not symptoms or symptoms.strip() == ""):
        st.warning("Please upload an image and/or type symptoms so the app can analyze.")
    else:
        # Image analysis
        if uploaded_file is not None:
            try:
                image_bytes = uploaded_file.read() if hasattr(uploaded_file, "read") else uploaded_file.getvalue()
                img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                st.image(img, caption="Uploaded Image", use_column_width=True)
                image_scores = analyze_image(img)
            except Exception as e:
                st.error("Could not process the uploaded image. Proceeding with text-only analysis.")
                image_scores = {k: 0.0 for k in HEALTH_CLASSES}
        else:
            image_scores = {k: 0.0 for k in HEALTH_CLASSES}

        # Text analysis
        text_scores = analyze_text(symptoms or "")
        text_present = bool(symptoms and symptoms.strip())

        # Combine
        final = combine_scores(image_scores, text_scores, text_present)
        label, confidence = pretty_prediction(final)

        # Show results
        st.subheader("🩺 Prediction Result")
        st.markdown(f"**Condition:** {label}")
        st.markdown(f"**Prediction Confidence:** {confidence:.1f}%")

        # Show breakdown (optional)
        with st.expander("Show full score breakdown"):
            for k in HEALTH_CLASSES:
                st.write(f"- {k}: {final.get(k,0.0):.3f}")

        st.subheader("💡 Suggested Guidance")
        for tip in GUIDANCE.get(label, GUIDANCE['Normal']):
            st.write(f"- {tip}")

        st.markdown("---")
        st.info("**Important:** This tool provides heuristic-based suggestions and is *not* a medical diagnosis. "
                "If you are worried, please consult a qualified healthcare professional or visit an emergency service for urgent symptoms.")