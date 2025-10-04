@echo off
echo Installing SignSpeak AI Dependencies...

echo Installing Python dependencies...
pip install -r requirements.txt

echo Installing Frontend dependencies...
cd frontend
npm install
cd ..

echo Creating necessary directories...
if not exist "data" mkdir data
if not exist "data\models" mkdir data\models
if not exist "data\datasets" mkdir data\datasets
if not exist "logs" mkdir logs

echo.
echo ✅ Dependencies installed successfully!
echo.
echo To start the application:
echo 1. Run start-backend.bat (in one terminal)
echo 2. Run start-frontend.bat (in another terminal)
echo.
pause
