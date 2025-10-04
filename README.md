# SignSpeak AI - Real-Time Sign Language Communication Bridge

## 🎯 Project Overview

SignSpeak AI is a real-time, two-way translation application that converts spoken language into animated Indian Sign Language (ISL) and recognizes ISL gestures from a camera, converting them back to text or speech.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd SignSpeak-AI

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Running the Application
```bash
# Terminal 1 - Start Backend
python backend/app.py

# Terminal 2 - Start Frontend
cd frontend
npm start
```

## 📁 Project Structure

```
SignSpeak-AI/
├── backend/                 # Flask API server
│   ├── app.py              # Main API server
│   └── models/             # ML models
│       ├── isl_recognition.py
│       └── speech_processing.py
├── frontend/               # React Native mobile app
│   ├── App.js              # Main application
│   ├── package.json        # Dependencies
│   └── app.json            # Expo configuration
├── avatar/                 # 3D avatar system
│   └── avatar_3d.py        # ISL gesture animations
├── datasets/               # Data processing
│   └── scripts/
│       └── data_processing.py
├── tests/                  # Test suite
│   ├── test_isl_recognition.py
│   └── test_speech_processing.py
├── docker/                 # Production deployment
│   ├── nginx.conf
│   └── start.sh
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Container orchestration
└── README.md              # This file
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/text_to_gesture` | POST | Convert text to ISL gestures |
| `/speech_to_text` | POST | Speech recognition |
| `/text_to_speech` | POST | Text to speech |
| `/recognize_gesture` | POST | ISL gesture recognition |

## 🎯 Features

- **Real-time ISL Recognition**: Camera-based gesture detection
- **Speech Processing**: Bidirectional speech conversion
- **3D Avatar System**: Animated ISL gestures
- **Mobile App**: Cross-platform React Native application
- **REST API**: Complete backend with ML models

## 🚀 Deployment

### Development
```bash
python backend/app.py
cd frontend && npm start
```

### Production
```bash
docker-compose up -d
```

## 📱 Access

- **Backend API**: http://localhost:5000
- **Frontend**: http://localhost:8081 (Metro Bundler)
- **Mobile App**: Use Expo Go app to scan QR code

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test API
python -c "import requests; print(requests.get('http://localhost:5000/health').json())"
```

## 📊 Status

- ✅ Backend API: Running
- ✅ Frontend: React Native ready
- ✅ 3D Avatar: Gesture animations
- ✅ Documentation: Complete
- ⚠️ Models: Need training data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🌟 Impact

Serving 63M+ deaf and hard-of-hearing individuals in India by breaking communication barriers and promoting accessibility.