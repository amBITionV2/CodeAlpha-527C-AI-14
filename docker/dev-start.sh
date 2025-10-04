#!/bin/bash

# SignSpeak AI Development Startup Script

set -e

echo "Starting SignSpeak AI development environment..."

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements.txt
pip install jupyter ipython pytest black flake8 mypy

# Start Jupyter notebook
echo "Starting Jupyter notebook..."
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root &
JUPYTER_PID=$!

# Start backend in development mode
echo "Starting backend API in development mode..."
cd /app/backend
python app.py &
BACKEND_PID=$!

# Start frontend development server
echo "Starting frontend development server..."
cd /app/frontend
npm start &
FRONTEND_PID=$!

# Function to handle shutdown
shutdown() {
    echo "Shutting down development services..."
    kill $JUPYTER_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap shutdown SIGTERM SIGINT

echo "Development environment started!"
echo "Backend API: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo "Jupyter: http://localhost:8888"

# Wait for processes
wait $JUPYTER_PID $BACKEND_PID $FRONTEND_PID
