# SomaTV - AI Movie Recommender 🎬🤖

**SomaTV** is an innovative AI-powered web application that recommends movies based on the user's real-time emotions. By leveraging Deep Learning and Computer Vision, the app analyzes facial expressions to suggest the perfect film for your current mood.

## ✨ Key Features
- **Real-time Emotion Detection:** Uses a CNN model trained on the FER2013 dataset to detect emotions (Happy, Neutral, Sad, etc.) with ultra-low latency (~40ms).
- **Mood-Based Recommendations:** Dynamic filtering of movies using the TMDB API based on detected emotions.
- **Privacy-First Design:** Features a dedicated "AI Mode" toggle to give users full control over their camera and privacy.
- **Cinematic UI:** A modern, responsive interface built with React for an immersive experience.

## 🚀 Tech Stack
- **Frontend:** React.js, Axios, CSS3 (Cinematic UI).
- **Backend:** FastAPI (Python), Uvicorn.
- **AI/ML:** TensorFlow/Keras, OpenCV.
- **Data:** TMDB API for movie metadata.

## 📸 Demo & Performance
The backend is optimized for performance, handling requests in approximately **40ms**, ensuring a smooth and "live" recommendation feel.

## 🛠️ How to Run
1. **Backend:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload

```

2. **Frontend:**
```bash
cd frontend
npm run dev

```



## 👩‍💻 Author

**Asmae ISSA**
*Master's Student in Artificial Intelligence*

```

