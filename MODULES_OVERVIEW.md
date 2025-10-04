# 🔧 SignSpeak AI - Modules & Dependencies Overview

## 📊 **Complete Technology Stack**

This document provides a comprehensive overview of all modules, libraries, and dependencies used in the SignSpeak AI project.

---

## 🐍 **Python Backend Modules**

### **Core AI/ML Libraries**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `numpy` | 1.24.3 | Numerical computing | Array operations, data processing |
| `opencv-python` | 4.8.1.78 | Computer vision | Image processing, video capture |
| `mediapipe` | 0.10.7 | Hand/pose detection | Real-time gesture recognition |
| `tensorflow` | 2.13.0 | Deep learning | ISL recognition model training |
| `torch` | 2.0.1 | PyTorch framework | Alternative ML models |
| `torchvision` | 0.15.2 | Computer vision | Image transformations |

### **Speech Processing**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `speechrecognition` | 3.10.0 | Speech-to-text | Google Speech API integration |
| `pyttsx3` | 2.90 | Text-to-speech | Voice synthesis |
| `pyaudio` | 0.2.11 | Audio I/O | Microphone access |

### **Web Framework**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `flask` | 2.3.3 | Web framework | REST API server |
| `flask-cors` | 4.0.0 | CORS handling | Cross-origin requests |
| `fastapi` | 0.103.2 | Modern API framework | Alternative API server |
| `uvicorn` | 0.23.2 | ASGI server | FastAPI server |

### **Database**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `sqlalchemy` | 2.0.21 | ORM | Database operations |
| `psycopg2-binary` | 2.9.7 | PostgreSQL driver | Database connectivity |

### **3D Graphics**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `pygame` | 2.5.2 | Game development | 3D avatar rendering |
| `moderngl` | 5.8.2 | OpenGL wrapper | 3D graphics |

### **Utilities**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `pillow` | 10.0.0 | Image processing | Image manipulation |
| `matplotlib` | 3.7.2 | Data visualization | Charts and graphs |
| `scikit-learn` | 1.3.0 | Machine learning | Model utilities |
| `pandas` | 2.0.3 | Data analysis | Data processing |

### **Development Tools**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `pytest` | 7.4.2 | Testing framework | Unit testing |
| `black` | 23.7.0 | Code formatting | Code style |
| `flake8` | 6.0.0 | Linting | Code quality |

---

## 📱 **React Native Frontend Modules**

### **Core Framework**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `expo` | ~49.0.0 | Development platform | React Native framework |
| `react` | 18.2.0 | UI library | Component framework |
| `react-native` | 0.72.6 | Mobile framework | Cross-platform development |

### **Camera & Media**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `expo-camera` | ~13.4.4 | Camera access | Gesture recognition |
| `expo-av` | ~13.4.1 | Audio/Video | Media processing |
| `expo-speech` | ~11.3.0 | Text-to-speech | Voice synthesis |
| `expo-media-library` | ~15.4.1 | Media storage | File management |
| `expo-permissions` | ~14.2.1 | Permissions | Access control |
| `react-native-camera` | ^4.2.1 | Camera API | Image capture |
| `react-native-vision-camera` | ^3.6.17 | Advanced camera | Real-time processing |

### **Navigation & UI**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `@react-navigation/native` | ^6.1.7 | Navigation | App routing |
| `@react-navigation/stack` | ^6.3.17 | Stack navigation | Screen transitions |
| `@react-navigation/bottom-tabs` | ^6.5.8 | Tab navigation | Bottom tabs |
| `react-native-gesture-handler` | ~2.12.0 | Gesture recognition | Touch handling |
| `react-native-reanimated` | ~3.3.0 | Animations | Smooth transitions |
| `react-native-safe-area-context` | 4.6.3 | Safe areas | Device compatibility |
| `react-native-screens` | ~3.22.0 | Screen optimization | Performance |

### **3D Graphics & Animation**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `three` | ^0.155.0 | 3D graphics | 3D avatar rendering |
| `@react-three/fiber` | ^8.13.0 | React Three.js | 3D components |
| `@react-three/drei` | ^9.88.0 | Three.js helpers | 3D utilities |
| `react-native-3d-model-view` | ^1.2.0 | 3D models | Model rendering |

### **UI Components**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `react-native-vector-icons` | ^10.0.0 | Icons | UI icons |
| `react-native-linear-gradient` | ^2.8.3 | Gradients | Background effects |
| `react-native-svg` | 13.9.0 | SVG support | Vector graphics |

### **Network & Data**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `axios` | ^1.5.0 | HTTP client | API communication |
| `react-native-fs` | ^2.20.0 | File system | File operations |
| `react-native-base64` | ^0.2.1 | Encoding | Data conversion |

### **Development Tools**
| Module | Version | Purpose | Usage |
|--------|---------|---------|-------|
| `@babel/core` | ^7.20.0 | JavaScript compiler | Code transformation |
| `@types/react` | ~18.2.14 | TypeScript types | Type definitions |
| `@types/react-native` | ~0.72.2 | TypeScript types | RN type definitions |
| `typescript` | ^5.1.3 | TypeScript | Type safety |
| `jest` | ^29.2.1 | Testing framework | Unit testing |
| `jest-expo` | ~49.0.0 | Expo testing | Test utilities |

---

## 🐳 **Docker & Deployment**

### **Containerization**
| Tool | Purpose | Usage |
|------|---------|-------|
| `Docker` | Containerization | Application packaging |
| `docker-compose` | Orchestration | Multi-service deployment |
| `nginx` | Reverse proxy | Load balancing |

---

## 🎯 **Module Usage by Feature**

### **ISL Gesture Recognition**
- **OpenCV** - Image processing and video capture
- **MediaPipe** - Hand and pose landmark detection
- **TensorFlow** - Deep learning model for gesture classification
- **NumPy** - Numerical operations on image data

### **Speech Processing**
- **SpeechRecognition** - Google Speech API integration
- **PyTTSx3** - Text-to-speech synthesis
- **PyAudio** - Audio input/output handling

### **3D Avatar Animation**
- **NumPy** - Mathematical operations for 3D coordinates
- **Three.js** - 3D graphics rendering
- **React Three Fiber** - React integration with Three.js

### **Mobile App Interface**
- **React Native** - Cross-platform mobile development
- **Expo** - Development platform and tools
- **React Navigation** - App navigation and routing

### **Backend API**
- **Flask** - REST API server
- **Flask-CORS** - Cross-origin request handling
- **SQLAlchemy** - Database ORM

---

## 📊 **Dependency Statistics**

### **Python Backend**
- **Total Dependencies**: 15 core modules
- **AI/ML Libraries**: 6 modules
- **Web Framework**: 4 modules
- **Utilities**: 5 modules

### **React Native Frontend**
- **Total Dependencies**: 20+ modules
- **Core Framework**: 3 modules
- **Camera/Media**: 7 modules
- **Navigation/UI**: 8 modules
- **3D Graphics**: 4 modules

### **Development Tools**
- **Testing**: 3 frameworks
- **Code Quality**: 2 tools
- **TypeScript**: 3 modules

---

## 🚀 **Installation Commands**

### **Python Backend**
```bash
pip install -r requirements.txt
```

### **React Native Frontend**
```bash
cd frontend
npm install
```

### **Docker Deployment**
```bash
docker-compose up -d
```

---

## 🏆 **Module Architecture**

The SignSpeak AI project uses a **modular architecture** with:

1. **Backend**: Python-based AI/ML processing
2. **Frontend**: React Native mobile application
3. **3D Graphics**: Three.js for avatar animation
4. **Database**: PostgreSQL with SQLAlchemy ORM
5. **Deployment**: Docker containerization

**Total Modules**: 35+ dependencies across Python and JavaScript ecosystems, creating a comprehensive real-time sign language communication system! 🌟
