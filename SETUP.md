# SignSpeak AI - Setup Guide

## Prerequisites Installation

### 1. Install Python 3.9+
Download and install Python from: https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during installation
- ✅ Install pip package manager

### 2. Install Node.js 18+
Download and install Node.js from: https://nodejs.org/
- This includes npm package manager

### 3. Install Git (Optional but recommended)
Download from: https://git-scm.com/downloads

## Quick Setup (Automated)

### Option 1: Using our setup script
```powershell
# Run the setup script
.\setup.ps1
```

### Option 2: Manual setup
```powershell
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install frontend dependencies
cd frontend
npm install
cd ..

# 3. Start the backend
cd backend
python app.py
```

## Development Environment

### Start Backend API
```powershell
cd backend
python app.py
```
Backend will be available at: http://localhost:5000

### Start Frontend (in new terminal)
```powershell
cd frontend
npm start
```
Frontend will be available at: http://localhost:3000

## Testing the Application

### 1. Test Backend API
```powershell
# Test health endpoint
curl http://localhost:5000/health
```

### 2. Test Frontend
Open browser and go to: http://localhost:3000

## API Endpoints

- `GET /health` - Health check
- `POST /recognize_gesture` - Recognize ISL gesture from image
- `POST /text_to_gesture` - Convert text to ISL gesture sequence
- `POST /speech_to_text` - Convert speech to text
- `POST /text_to_speech` - Convert text to speech

## Troubleshooting

### Common Issues:

1. **Python not found**: Make sure Python is installed and added to PATH
2. **Node modules error**: Run `npm install` in the frontend directory
3. **Port already in use**: Change ports in the configuration files
4. **Permission errors**: Run PowerShell as Administrator

### Getting Help:
- Check the logs in the terminal
- Ensure all dependencies are installed
- Verify ports 5000 and 3000 are available

## Next Steps

1. **Collect ISL Data**: Record ISL gesture videos
2. **Train Models**: Use the training scripts in `datasets/scripts/`
3. **Deploy**: Use Docker for production deployment
4. **Test**: Run the test suite with `pytest tests/`

## Features Ready to Use

✅ **Real-time ISL Recognition**: Camera-based gesture detection
✅ **Speech Processing**: Bidirectional speech conversion
✅ **3D Avatar**: Animated ISL gestures
✅ **Mobile App**: React Native cross-platform app
✅ **API Backend**: RESTful API for all services
✅ **Testing**: Comprehensive test suite

Your SignSpeak AI project is ready to make a real impact! 🎉
