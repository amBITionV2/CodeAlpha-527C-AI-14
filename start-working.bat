@echo off
echo ========================================
echo SignSpeak AI - Working System
echo ========================================
echo.

echo Starting Backend Server...
start "SignSpeak AI Backend" cmd /k "cd /d %~dp0 && python backend\app_production_simple.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo Starting Frontend Server...
start "SignSpeak AI Frontend" cmd /k "cd /d %~dp0\frontend\web && python simple-server.py"

echo Waiting for frontend to start...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo SignSpeak AI Working System Started!
echo ========================================
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:3000/simple-production.html
echo.
echo Opening application in browser...
start http://localhost:3000/simple-production.html
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the system.
echo.
echo Features:
echo ✓ Real-time gesture recognition (improved accuracy)
echo ✓ Text-to-gesture conversion
echo ✓ Simple avatar animation
echo ✓ Working interface without complex dependencies
echo.
pause
