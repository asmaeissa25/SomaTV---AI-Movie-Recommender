# SomaTV - AI Movie Recommender 🎬

**SomaTV** is an innovative AI-powered web application that recommends movies based on the user's real-time emotions. By leveraging Deep Learning and Computer Vision, the app analyzes facial expressions to suggest the perfect film for your current mood.

## ✨ Key Features

- **Real-time Emotion Detection:** Uses a CNN model trained on the FER2013 dataset to detect emotions (Happy, Neutral, Sad, etc.) with ultra-low latency (~40ms).
- **Mood-Based Recommendations:** Dynamic filtering of movies using the TMDB API based on detected emotions.
- **Privacy-First Design:** Features a dedicated "AI Mode" toggle to give users full control over their camera and privacy.
- **Cinematic UI:** A modern, responsive interface built with React for an immersive experience.

## 🚀 Tech Stack

- **Frontend:** React.js, Axios, Tailwind CSS, Framer Motion
- **Backend:** FastAPI (Python), Uvicorn
- **AI/ML:** TensorFlow/Keras, OpenCV
- **Data:** TMDB API for movie metadata

## 📸 Demo & Screenshots

### Application Interface

![SomaTV Interface](https://raw.githubusercontent.com/asmaeissa25/SomaTV---AI-Movie-Recommender/main/demo/soma1.png)

### Emotion Detection in Action

![Emotion Detection](https://raw.githubusercontent.com/asmaeissa25/SomaTV---AI-Movie-Recommender/main/demo/soma2.png)

### AI-Powered Recommendations

![Movie Recommendations](https://raw.githubusercontent.com/asmaeissa25/SomaTV---AI-Movie-Recommender/main/demo/soma3.png)

### Feature Showcase

![Feature Showcase](https://raw.githubusercontent.com/asmaeissa25/SomaTV---AI-Movie-Recommender/main/demo/soma4.png)

### User Experience

![User Experience](https://raw.githubusercontent.com/asmaeissa25/SomaTV---AI-Movie-Recommender/main/demo/soma5.png)

### Real-time Analysis

![Real-time Analysis](https://raw.githubusercontent.com/asmaeissa25/SomaTV---AI-Movie-Recommender/main/demo/soma6.png)

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Node.js 16+** and npm/yarn
- **Git**
- **Webcam** (for emotion detection feature)

## 📋 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/asmaeissa25/SomaTV---AI-Movie-Recommender.git
cd SOMATV
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn tensorflow keras opencv-python pillow python-dotenv

# Create .env file (copy from .env.example)
cp .env.example .env

# Configure CORS origins in .env if needed (default: localhost:5173,3000)
```

### 3. Start the Backend Server

```bash
# From the backend directory
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will run on `http://127.0.0.1:8000`

**API Documentation:** Visit `http://127.0.0.1:8000/docs` for interactive API docs

### 4. Frontend Setup

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file if needed (configure TMDB API key)
# VITE_TMDB_API_KEY=your_api_key_here

# Start development server
npm run dev
```

The frontend will run on `http://localhost:5173`

### 5. Access the Application

Open your browser and navigate to: `http://localhost:5173`

## 🔐 Environment Variables

### Backend (.env)

```env
# Allowed CORS origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Model configuration
MODEL_PATH=emotion_model.h5

# Server configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### Frontend (.env.local or .env)

```env
VITE_TMDB_API_KEY=your_tmdb_api_key_here
VITE_API_URL=http://localhost:8000
```

## 📋 Project Structure

```
SOMATV/
├── backend/
│   ├── main.py              # FastAPI server with emotion prediction
│   ├── api.py               # Alternative API implementation
│   ├── emotion_model.h5     # Pre-trained CNN model
│   └── tempCodeRunnerFile.py
├── frontend/
│   ├── src/
│   │   ├── SomaTV.jsx       # Main app component
│   │   ├── App.jsx          # App wrapper
│   │   ├── main.jsx         # Entry point
│   │   ├── index.css        # Global styles
│   │   └── App.css          # App styles
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── package.json
│   └── index.html
├── demo/                    # Demo screenshots
└── README.md
```

## 🔧 Configuration

### TMDB API Key

To use the movie recommendations feature, you need to add your TMDB API key:

1. Go to [The Movie Database (TMDB)](https://www.themoviedb.org/settings/api)
2. Get your API key
3. Update the `API_KEY` variable in `frontend/src/SomaTV.jsx`

## 🎯 How It Works

1. **Camera Capture:** The app captures video frames from your webcam
2. **Emotion Detection:** Sends frames to the backend AI model every 3 seconds
3. **Mood Analysis:** TensorFlow model predicts your current emotion
4. **Smart Filtering:** TMDB API is queried and results are filtered based on your mood
5. **Dynamic Display:** Movies matching your mood are highlighted in red

### Mood to Genre Mapping

- **Happy** → Comedy, Animation
- **Sad** → Drama
- **Angry** → Action
- **Fear** → Horror
- **Neutral** → All genres

## 🎨 UI Features

- **Dark cinematic theme** with modern glassmorphism design
- **Real-time mood display** in the header
- **Animated movie cards** with hover effects
- **Category filters** for easy navigation
- **Search functionality** to find specific movies
- **AI Mode toggle** for privacy control

## 📊 Performance

The backend is optimized for performance, handling emotion detection requests in approximately **40ms**, ensuring a smooth and "live" recommendation feel.

## 🔌 API Endpoints

### Emotion Prediction

**POST** `/predict`

Request:

```json
{
  "image": "base64_encoded_image_string"
}
```

Response:

```json
{
  "mood": "Happy"
}
```

### Health Check

**GET** `/docs` - Interactive API documentation (Swagger UI)

**GET** `/redoc` - Alternative API documentation (ReDoc)

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'tensorflow'`

- **Solution:** Ensure you're in the virtual environment and have installed all dependencies:
  ```bash
  pip install -r requirements.txt
  ```

**Problem:** `emotion_model.h5 not found`

- **Solution:** Ensure the model file is in the backend directory or update the `MODEL_PATH` in `.env`

**Problem:** CORS errors in browser console

- **Solution:** Update `ALLOWED_ORIGINS` in `.env` to include your frontend URL

### Frontend Issues

**Problem:** `TMDB API key errors`

- **Solution:** Verify your TMDB API key is correctly set in the environment variables

**Problem:** Webcam not working

- **Solution:**
  - Check browser permissions for camera access
  - Try a different browser
  - Ensure your camera is not already in use by another app

## 📦 Build & Deployment

### Frontend Build

```bash
cd frontend
npm run build
```

Output will be in `frontend/dist/`

### Backend Deployment

For production deployment, use a production ASGI server:

```bash
# Using gunicorn with uvicorn workers
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

## 📈 Future Improvements

- [ ] Add backend caching for frequently detected emotions
- [ ] Implement user preferences and watchlist
- [ ] Add more emotion categories
- [ ] Optimize model for faster inference
- [ ] Add Docker containerization
- [ ] Deploy to cloud (AWS, GCP, Azure)
- [ ] Add analytics and telemetry

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙋 Support

For issues, questions, or suggestions, please open an issue on [GitHub Issues](https://github.com/asmaeissa25/SomaTV---AI-Movie-Recommender/issues).

## 👨‍💻 Author

**Asmae Issa** - [GitHub](https://github.com/asmaeissa25)

**SomaTV Development Team** - 2026

---

**© 2026 SOMATV - AI DRIVEN STREAMING** 🎬✨
