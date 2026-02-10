from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import io
from PIL import Image

app = FastAPI()

# Enable CORS for React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the pre-trained emotion recognition model
model = load_model('emotion_model.h5')
emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprise"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Convert uploaded file to grayscale image
    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content)).convert('L')
    img = img.resize((48, 48))
    
    # 2. Preprocess image for the model (Normalization & Reshaping)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(np.expand_dims(img_array, -1), 0)

    # 3. Model Prediction
    prediction = model.predict(img_array)
    label = emotion_dict[np.argmax(prediction)]
    
    return {"emotion": label}

if __name__ == "__main__":
    import uvicorn
    # Start the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)