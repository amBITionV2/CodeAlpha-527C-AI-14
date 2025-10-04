# SignSpeak AI - Production Guide

## Overview

SignSpeak AI is a production-ready sign language communication system that provides real-time gesture recognition, speech processing, and 3D avatar animation. This guide covers the complete setup and usage of the production system.

## Features

### 🎯 Core Capabilities
- **Real-time Gesture Recognition**: Uses MediaPipe and TensorFlow for accurate ISL gesture detection
- **Speech Processing**: Multi-language speech-to-text and text-to-speech conversion
- **3D Avatar Animation**: Three.js-powered 3D avatar with realistic gesture animations
- **Text-to-Gesture Conversion**: Converts written text to sign language gesture sequences
- **Multi-language Support**: Supports 12+ Indian languages

### 🚀 Production Features
- **High Performance**: Optimized for real-time processing
- **Scalable Architecture**: Modular design for easy extension
- **Professional UI**: Modern, responsive web interface
- **Error Handling**: Comprehensive error handling and user feedback
- **Status Monitoring**: Real-time system status and health checks

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 8GB (16GB recommended)
- **Storage**: 2GB free space
- **Webcam**: For gesture recognition
- **Microphone**: For speech processing

### Recommended Requirements
- **OS**: Windows 11 or macOS 12+
- **Python**: 3.9 or higher
- **RAM**: 16GB or more
- **Storage**: 5GB free space
- **GPU**: NVIDIA GPU with CUDA support (for faster ML processing)
- **Webcam**: 1080p or higher resolution
- **Microphone**: High-quality microphone

## Installation

### Quick Installation (Windows)
```bash
# Run the installation script
install-production.bat
```

### Manual Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd SignSpeak-AI
```

2. **Install Python dependencies**
```bash
pip install -r requirements-production.txt
```

3. **Install additional dependencies**
```bash
pip install requests websockets asyncio
```

4. **Create necessary directories**
```bash
mkdir backend\models
mkdir logs
mkdir data
```

## Running the Production System

### 1. Start the Backend Server
```bash
python backend/app_production.py
```

The backend will start on `http://localhost:5000` with the following endpoints:
- `GET /health` - Health check
- `POST /recognize_gesture` - Gesture recognition
- `POST /speech_to_text` - Speech recognition
- `POST /text_to_gesture` - Text to gesture conversion
- `POST /text_to_speech` - Text to speech conversion
- `GET /get_available_gestures` - List available gestures
- `GET /get_available_languages` - List supported languages

### 2. Start the Frontend Server
```bash
python frontend/web/production-server.py
```

The frontend will be available at `http://localhost:3000/production.html`

### 3. Access the Application
Open your browser and navigate to `http://localhost:3000/production.html`

## Usage Guide

### Real-time Gesture Recognition

1. **Start Camera**: Click "Start Camera" to activate your webcam
2. **Position Hands**: Place your hands in the detection area
3. **Capture Gesture**: Click "Capture Gesture" to recognize the current hand position
4. **View Results**: The recognized gesture will be displayed with confidence score

**Supported Gestures**: 50+ ISL gestures including:
- Greetings: HELLO, HI, GOODBYE, WELCOME
- Emotions: HAPPY, SAD, ANGRY, SURPRISED
- Responses: YES, NO, MAYBE, OK
- Questions: WHAT, WHERE, WHEN, WHY, HOW, WHO
- Actions: COME, GO, STOP, WAIT, HELP, LEARN
- Objects: BOOK, PEN, COMPUTER, PHONE, CAR, HOUSE
- Family: MOTHER, FATHER, SISTER, BROTHER, FAMILY
- Colors: RED, BLUE, GREEN, YELLOW, BLACK, WHITE
- Numbers: ONE through TEN

### Speech Processing

1. **Select Language**: Choose your preferred language from the dropdown
2. **Start Listening**: Click "Start Listening" to begin speech recognition
3. **Speak**: Speak clearly into your microphone
4. **Stop Listening**: Click "Stop Listening" to process the audio
5. **View Results**: The recognized text will be displayed

**Supported Languages**:
- English (en)
- Hindi (hi)
- Tamil (ta)
- Telugu (te)
- Bengali (bn)
- Gujarati (gu)
- Kannada (kn)
- Malayalam (ml)
- Marathi (mr)
- Punjabi (pa)
- Odia (or)
- Assamese (as)

### Text-to-Speech

1. **Enter Text**: Type or paste text in the text area
2. **Select Language**: Choose the output language
3. **Convert**: Click "Convert to Speech" to generate audio
4. **Play**: Use the audio controls to play the generated speech

### Text-to-Gesture Conversion

1. **Enter Text**: Type the text you want to convert
2. **Convert**: Click "Convert to Gestures" to generate gesture sequence
3. **View Sequence**: See the list of gestures that will be performed
4. **Watch Animation**: The 3D avatar will perform the gesture sequence

### 3D Avatar Controls

- **Reset Pose**: Return the avatar to neutral position
- **Test Animation**: Play a sample gesture sequence
- **Current Gesture**: Shows the gesture currently being performed
- **Progress Bar**: Shows progress through gesture sequences

## API Documentation

### Gesture Recognition API

**Endpoint**: `POST /recognize_gesture`

**Request Body**:
```json
{
    "image": "base64_encoded_image_data"
}
```

**Response**:
```json
{
    "gesture": "HELLO",
    "confidence": 0.95,
    "description": "Wave hand side to side",
    "duration": 1.0,
    "message": "Recognized gesture: HELLO with 0.95 confidence"
}
```

### Speech Recognition API

**Endpoint**: `POST /speech_to_text`

**Request Body**:
```json
{
    "audio": "base64_encoded_audio_data",
    "language": "en"
}
```

**Response**:
```json
{
    "text": "Hello, how are you?",
    "confidence": 0.92,
    "language": "en",
    "message": "Speech recognized: \"Hello, how are you?\" with 0.92 confidence"
}
```

### Text-to-Gesture API

**Endpoint**: `POST /text_to_gesture`

**Request Body**:
```json
{
    "text": "Hello, thank you"
}
```

**Response**:
```json
{
    "gesture_sequence": [
        {
            "gesture": "HELLO",
            "duration": 1.0,
            "description": "Wave hand side to side",
            "word": "hello"
        },
        {
            "gesture": "THANK_YOU",
            "duration": 1.2,
            "description": "Hand to chin, then forward",
            "word": "thank"
        }
    ],
    "text": "Hello, thank you",
    "message": "Converted text to 2 gestures"
}
```

## Troubleshooting

### Common Issues

1. **Camera Not Working**
   - Check camera permissions in browser
   - Ensure no other applications are using the camera
   - Try refreshing the page

2. **Microphone Not Working**
   - Check microphone permissions in browser
   - Ensure microphone is not muted
   - Test microphone in other applications

3. **API Connection Failed**
   - Ensure backend server is running on port 5000
   - Check firewall settings
   - Verify no other application is using port 5000

4. **Low Gesture Recognition Accuracy**
   - Ensure good lighting
   - Keep hands within the detection area
   - Make clear, deliberate gestures
   - Avoid background clutter

5. **Speech Recognition Issues**
   - Speak clearly and at normal volume
   - Reduce background noise
   - Check microphone quality
   - Try different languages

### Performance Optimization

1. **For Better Gesture Recognition**:
   - Use good lighting conditions
   - Keep background simple
   - Make gestures clearly and deliberately
   - Ensure stable internet connection

2. **For Better Speech Recognition**:
   - Use a high-quality microphone
   - Minimize background noise
   - Speak at normal pace and volume
   - Choose appropriate language setting

3. **For Better Performance**:
   - Close unnecessary applications
   - Ensure adequate RAM (8GB+)
   - Use a modern web browser
   - Keep the system updated

## Development

### Project Structure
```
SignSpeak-AI/
├── backend/
│   ├── app_production.py          # Production backend API
│   └── models/
│       ├── real_gesture_recognition.py
│       └── real_speech_processing.py
├── frontend/
│   └── web/
│       ├── production.html        # Production frontend
│       ├── production-styles.css  # Production styles
│       ├── production-script.js   # Production JavaScript
│       ├── three_js_avatar.js     # 3D avatar system
│       └── production-server.py   # Frontend server
├── requirements-production.txt    # Production dependencies
└── PRODUCTION_GUIDE.md           # This guide
```

### Adding New Gestures

1. **Update Gesture Database** in `backend/models/real_gesture_recognition.py`
2. **Add Animation** in `frontend/web/three_js_avatar.js`
3. **Update Word Mapping** in `backend/app_production.py`

### Adding New Languages

1. **Update Language Support** in `backend/models/real_speech_processing.py`
2. **Add Language Option** in `frontend/web/production.html`
3. **Test Speech Recognition** with the new language

## Support

For technical support or questions:
- Check the troubleshooting section above
- Review the API documentation
- Check system requirements
- Ensure all dependencies are installed

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**SignSpeak AI - Bridging Communication Through Technology**
