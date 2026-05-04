from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cv2
import numpy as np
import base64
import os
from tensorflow.keras.models import load_model
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1. First, define the app
app = FastAPI(
    title="SomaTV AI API",
    description="Emotion detection and movie recommendation API",
    version="1.0.0"
)

# 2. CORS settings - restrict to allowed origins for security
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load the model and emotion dictionary
try:
    model = load_model('emotion_model.h5')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprise"}

# 4. Define the data schema
class ImageData(BaseModel):
    image: str

# 5. Now we can use @app.post
@app.post("/predict")
async def predict_emotion(data: ImageData):
    try:
        # 1. Decode the image
        img_str = data.image.split(',')[1] if ',' in data.image else data.image
        img_bytes = base64.b64decode(img_str)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return {"mood": "Neutral"}

        # 2. Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            # Draw the rectangle (color 255 in grayscale gives white, use it as the model was trained)
            cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 255, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
        else:
            roi_gray = gray # Fallback plan

        # 3. Final processing
        roi_gray = cv2.resize(roi_gray, (48, 48))
        roi_gray = roi_gray.astype("float") / 255.0
        roi_gray = np.expand_dims(np.expand_dims(roi_gray, axis=0), axis=-1)
        
        # 4. Make prediction and print results for debugging
        prediction = model.predict(roi_gray)
        max_index = int(np.argmax(prediction))
        label = emotion_dict[max_index]
        
        # These lines are very important, check them in the terminal
        print(f"📊 Raw Prediction Scores: {prediction[0]}")
        print(f"🎯 AI Result: {label}")
        
        return {"mood": label}

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"mood": "Neutral"}
# 6. Start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)