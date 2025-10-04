@echo off
echo ========================================
echo SignSpeak AI - Production System
echo ========================================
echo.

echo Starting Backend Server...
start "SignSpeak AI Backend" cmd /k "cd /d %~dp0 && python backend\app_production_simple.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo Starting Frontend Server...
start "SignSpeak AI Frontend" cmd /k "cd /d %~dp0\frontend\web && python production-server.py"

echo Waiting for frontend to start...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo SignSpeak AI Production System Started!
echo ========================================
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:3000/production.html
echo.
echo Opening application in browser...
start http://localhost:3000/production.html
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the system.
echo.
pause
