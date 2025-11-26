AI Health Checker 🩺

Track: Health & Public Safety
Hackathon: Build with AI Hackathon, September 2025



PROJECT OVERVIEW 

AI Health Checker is an AI-powered web application designed to help users quickly identify common skin conditions or X-ray health issues. By uploading an image of the affected area or X-ray, the app predicts the possible health condition and provides basic guidance for care.

This solution leverages deep learning to classify health images with confidence scores, offering a simple, intuitive interface for anyone to use. It is ideal for early detection, awareness, and guiding users to seek professional care when necessary.




PROBLEM STATEMENT 

Many people face delays or uncertainty in identifying health conditions, especially skin-related issues, due to limited access to specialists. This leads to late treatment and unnecessary anxiety. AI Health Checker addresses this by:

Providing instant image-based predictions.

Offering basic guidance and recommendations.

Supporting early awareness and informed next steps.



SOLUTION FEATURES 

Image Upload: Users can upload skin condition images or X-rays.

AI Classification: Deep learning model predicts condition.

Prediction Confidence: Shows probability (%) of each class.

Health Guidance: Provides basic care recommendations.

User-Friendly UI: Responsive and simple web interface built with Streamlit.





HEALTH CONDITION CLASSES 

CLASS	GUIDANCE SUMMARY 

Eczema	Keep area clean, avoid scratching, moisturize, consult dermatologist if persists
Psoriasis	Use medicated creams, avoid stress/triggers, consult dermatologist
Acne	Keep skin clean, avoid oily products, see dermatologist if severe
Skin Infection	Clean affected area, avoid spreading, consult healthcare provider
Normal	No major concerns, maintain healthy skincare





TECHNOLOGY STACK 

Frontend: Streamlit (Web App)

Backend / AI: Python, TensorFlow / Keras

Image Processing: Pillow, NumPy

Deployment: Streamlit Cloud





HOW IT WORKS 

1. User uploads an image (skin/X-ray).

2. Image is resized and preprocessed.

3. AI model predicts the health condition.

4. App displays prediction, confidence score, and guidance.


EXAMPLE FLOW:

Upload Image → AI Model Predicts → Show Condition & Confidence → Display Guidance


DEMO VIDEO 

Watch Demo on YouTube
(3-minute video demonstrating upload, prediction, and guidance)




Live App / Hosted URL

Access AI Health Checker Here



Source Code Repository

GitHub Repository

Fully open source

Includes all code, assets, and model files

MIT License included





INSTALLATION & RUNNING LOCALLY 

1. Clone the repository


git clone https://github.com/ebi-max/ai-health-checker.git
cd ai-health-checker

2. Install dependencies


pip install -r requirements.txt

3. Run the app


streamlit run streamlit_app.py

4. Upload an image and see predictions live.




TEAM INFORMATION 

Team Name: EBIKLEAN AI Health

Team Members:

Ebieme Bassey – ebiemebassey887@gmail.com



INNOVATION & IMPACT 

Leverages AI for early health condition awareness.

Reduces reliance on immediate access to specialists.

User-friendly and accessible for everyone.

Can be extended to include more health conditions or mobile deployment.




LICENCE 

MIT License – fully open source.