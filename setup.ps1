# SignSpeak AI - Automated Setup Script
# This script will install dependencies and set up the development environment

Write-Host "🚀 SignSpeak AI Setup Starting..." -ForegroundColor Green

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.[0-9]+") {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Python not found or wrong version" -ForegroundColor Red
        Write-Host "Please install Python 3.9+ from https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "❌ Python not found" -ForegroundColor Red
    Write-Host "Please install Python 3.9+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if pip is available
Write-Host "Checking pip installation..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip not found" -ForegroundColor Red
    Write-Host "Please install pip or reinstall Python with pip" -ForegroundColor Yellow
    exit 1
}

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "✅ Python dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install Python dependencies" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    if ($nodeVersion -match "v[0-9]+\.[0-9]+\.[0-9]+") {
        Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Node.js not found or wrong version" -ForegroundColor Red
        Write-Host "Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "❌ Node.js not found" -ForegroundColor Red
    Write-Host "Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Install frontend dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
try {
    Set-Location frontend
    npm install
    Set-Location ..
    Write-Host "✅ Frontend dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install frontend dependencies" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Set-Location ..
    exit 1
}

# Create necessary directories
Write-Host "Creating project directories..." -ForegroundColor Yellow
$directories = @("data", "data/models", "data/datasets", "logs", "frontend/node_modules")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Green
    }
}

# Test the setup
Write-Host "Testing the setup..." -ForegroundColor Yellow

# Test backend import
try {
    Set-Location backend
    python -c "import app; print('Backend imports successful')"
    Set-Location ..
    Write-Host "✅ Backend setup successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend setup failed" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Set-Location ..
}

# Test frontend setup
try {
    Set-Location frontend
    npm list --depth=0 | Out-Null
    Set-Location ..
    Write-Host "✅ Frontend setup successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend setup failed" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Set-Location ..
}

Write-Host "🎉 SignSpeak AI Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Start the backend: cd backend && python app.py" -ForegroundColor White
Write-Host "2. Start the frontend: cd frontend && npm start" -ForegroundColor White
Write-Host "3. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host ""
Write-Host "For more information, see SETUP.md" -ForegroundColor Yellow
