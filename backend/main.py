from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cv2
import numpy as np
import base64
from tensorflow.keras.models import load_model

# 1. أول حاجة هي تعريف الـ app
app = FastAPI()

# 2. إعدادات الـ CORS ضرورية باش يهضر React مع Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. تحميل الموديل والقاموس
try:
    model = load_model('emotion_model.h5')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprise"}

# 4. تعريف الـ Schema ديال البيانات
class ImageData(BaseModel):
    image: str

# 5. دابا عاد تقدري تستخدمي @app.post
@app.post("/predict")
async def predict_emotion(data: ImageData):
    try:
        # 1. فك تشفير الصورة
        img_str = data.image.split(',')[1] if ',' in data.image else data.image
        img_bytes = base64.b64decode(img_str)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return {"mood": "Neutral"}

        # 2. تحويل للرمادي (Grayscale)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            # رسم المربع الأخضر (اللون 255 في Grayscale كيعطي أبيض، غانديروه كيفما تدرب الموديل)
            cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 255, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
        else:
            roi_gray = gray # خطة بديلة

        # 3. المعالجة النهائية
        roi_gray = cv2.resize(roi_gray, (48, 48))
        roi_gray = roi_gray.astype("float") / 255.0
        roi_gray = np.expand_dims(np.expand_dims(roi_gray, axis=0), axis=-1)
        
        # 4. التوقع وطباعة النتائج للتشخيص
        prediction = model.predict(roi_gray)
        max_index = int(np.argmax(prediction))
        label = emotion_dict[max_index]
        
        # هاد السطور مهمة بزاف تشوفيها فـ Terminal
        print(f"📊 Raw Prediction Scores: {prediction[0]}")
        print(f"🎯 AI Result: {label}")
        
        return {"mood": label}

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"mood": "Neutral"}
# 6. تشغيل السيرفر
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)