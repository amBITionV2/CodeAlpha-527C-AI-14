@echo off
echo ========================================
echo SignSpeak AI - Production System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Starting SignSpeak AI Production System...
echo.

REM Check if backend dependencies are installed
echo Checking backend dependencies...
python -c "import tensorflow, mediapipe, cv2, speech_recognition, pyttsx3" >nul 2>&1
if errorlevel 1 (
    echo Warning: Some backend dependencies are missing
    echo Please run: pip install -r requirements-production.txt
    echo.
)

REM Start backend server in background
echo Starting backend server...
start "SignSpeak AI Backend" cmd /k "cd /d %~dp0 && python backend\app_production.py"

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start frontend server
echo Starting frontend server...
start "SignSpeak AI Frontend" cmd /k "cd /d %~dp0 && python frontend\web\production-server.py"

REM Wait for frontend to start
echo Waiting for frontend to initialize...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo SignSpeak AI Production System Started!
echo ========================================
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:3000/production.html
echo.
echo Features Available:
echo ✓ Real-time Gesture Recognition
echo ✓ Speech Processing (12+ languages)
echo ✓ 3D Avatar Animation
echo ✓ Text-to-Gesture Conversion
echo ✓ Professional Web Interface
echo.
echo Press any key to open the application in your browser...
pause >nul

REM Open browser
start http://localhost:3000/production.html

echo.
echo Application opened in browser!
echo.
echo To stop the system:
echo 1. Close this window
echo 2. Close the backend and frontend terminal windows
echo.
echo For help, see PRODUCTION_GUIDE.md
echo.
pause
