# SignSpeak AI - Complete Application Launcher
# PowerShell script to start both backend and frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SignSpeak AI - Complete Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.9+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if backend directory exists
if (-not (Test-Path "backend/app.py")) {
    Write-Host "❌ Backend not found. Please run from project root directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if frontend directory exists
if (-not (Test-Path "frontend/web/index.html")) {
    Write-Host "❌ Frontend not found. Please run from project root directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "🚀 Starting Backend API Server..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "backend/app.py" -WindowStyle Normal

Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "🌐 Starting Web Frontend..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "frontend/web/server.py" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Application Started Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔗 Backend API: http://localhost:5000" -ForegroundColor Blue
Write-Host "🌐 Web Frontend: http://localhost:3000" -ForegroundColor Blue
Write-Host ""
Write-Host "💡 The browser should open automatically" -ForegroundColor Green
Write-Host "🛑 Close the terminal windows to stop the servers" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to exit"
