@echo off
echo ========================================
echo SignSpeak AI - Complete Application
echo ========================================
echo.

echo Starting Backend API Server...
start "SignSpeak AI Backend" cmd /k "python backend/app.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting Web Frontend...
start "SignSpeak AI Frontend" cmd /k "cd frontend/web && python server.py"

echo.
echo ========================================
echo Application Started Successfully!
echo ========================================
echo.
echo Backend API: http://localhost:5000
echo Web Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
