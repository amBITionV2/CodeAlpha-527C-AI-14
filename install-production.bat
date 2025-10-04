@echo off
echo ========================================
echo SignSpeak AI - Production Installation
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

echo Python found. Installing production dependencies...
echo.

REM Install production requirements
echo Installing Python dependencies...
pip install -r requirements-production.txt
if errorlevel 1 (
    echo Warning: Some dependencies failed to install
    echo This may affect functionality
    echo.
)

REM Install additional dependencies for better performance
echo Installing additional performance dependencies...
pip install requests websockets asyncio
if errorlevel 1 (
    echo Warning: Additional dependencies failed to install
    echo.
)

REM Check if Node.js is installed (for potential future use)
node --version >nul 2>&1
if errorlevel 1 (
    echo Warning: Node.js not found
    echo Some advanced features may not work
    echo.
) else (
    echo Node.js found
    echo.
)

REM Create necessary directories
echo Creating necessary directories...
if not exist "backend\models" mkdir "backend\models"
if not exist "frontend\web" mkdir "frontend\web"
if not exist "logs" mkdir "logs"
if not exist "data" mkdir "data"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start the backend server:
echo    python backend\app_production.py
echo.
echo 2. In another terminal, start the frontend:
echo    python frontend\web\production-server.py
echo.
echo 3. Open your browser to:
echo    http://localhost:3000/production.html
echo.
echo For help, see PRODUCTION_GUIDE.md
echo.
pause
