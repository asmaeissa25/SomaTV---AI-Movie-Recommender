import streamlit as st
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# 1. Professional Page Configuration
st.set_page_config(page_title="EmoShop AI", page_icon="🛍️", layout="wide")

# Custom CSS for a modern, "Glowy" interface
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #4CAF50; color: white; }
    .product-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .emotion-badge {
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: bold;
        color: white;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Model Loading with Cache
@st.cache_resource
def load_my_model():
    # Load the pre-trained emotion detection model
    return load_model('emotion_model.h5')

model = load_my_model()
emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprise"}

# 3. Sidebar Configuration
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=100)
    st.title("Settings")
    st.write("Scan your face to get personalized deals.")
    st.divider()
    st.info("AI Accuracy: 55%")

# 4. Main Interface Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📸 Live Mood Scanner")
    # Camera input component
    img_file_buffer = st.camera_input("")

with col2:
    st.markdown("### 🎁 Recommended for You")
    if img_file_buffer is not None:
        # Image Processing
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
        
        # Load Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                # Preprocessing the detected face area
                roi_gray = gray[y:y+h, x:x+w]
                roi_gray = cv2.resize(roi_gray, (48, 48)) / 255.0
                roi_gray = np.expand_dims(np.expand_dims(roi_gray, -1), 0)

                # Predict Emotion
                prediction = model.predict(roi_gray)
                label = emotion_dict[np.argmax(prediction)]

                # Display emotion with colored badge
                color = "#28a745" if label == "Happy" else "#007bff" if label == "Neutral" else "#dc3545"
                st.markdown(f'<div class="emotion-badge" style="background-color: {color};">Detected Mood: {label}</div>', unsafe_allow_html=True)
                st.write("")

                # Render dynamic product recommendations based on mood
                if label == "Happy":
                    st.markdown("""
                        <div class="product-card">
                            <img src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=200" width="150">
                            <h4>Smart Watch Pro</h4>
                            <p style="color: #4CAF50; font-weight: bold;">$199.99</p>
                            <button>Buy Now</button>
                        </div>
                    """, unsafe_allow_html=True)
                elif label == "Sad":
                    st.markdown("""
                        <div class="product-card">
                            <img src="https://images.unsplash.com/photo-1511381939415-e44015466834?w=200" width="150">
                            <h4>Comfort Bundle (Chocolate + Candle)</h4>
                            <p style="color: #4CAF50; font-weight: bold;">$29.99</p>
                            <button>Treat Yourself</button>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("Keep smiling! We have daily deals for you.")
        else:
            st.warning("No face detected. Please look at the camera.")

st.divider()
st.caption("Powered by Emotional AI • 2026")