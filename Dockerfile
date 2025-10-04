# SignSpeak AI Docker Configuration
# Multi-stage build for production deployment

# Stage 1: Base image with Python and system dependencies
FROM python:3.9-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libopencv-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libatlas-base-dev \
    gfortran \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Backend dependencies
FROM base as backend-deps

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional ML dependencies
RUN pip install --no-cache-dir \
    tensorflow-gpu==2.13.0 \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Stage 3: Backend application
FROM backend-deps as backend

# Copy backend code
COPY backend/ ./backend/
COPY avatar/ ./avatar/

# Create necessary directories
RUN mkdir -p /app/data/models /app/data/datasets /app/logs

# Set working directory
WORKDIR /app/backend

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run backend application
CMD ["python", "app.py"]

# Stage 4: Frontend dependencies
FROM node:18-alpine as frontend-deps

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Stage 5: Frontend application
FROM frontend-deps as frontend

# Copy frontend code
COPY frontend/ ./

# Build application
RUN npm run build

# Stage 6: Production image
FROM nginx:alpine as production

# Install Python runtime for backend
RUN apk add --no-cache python3 py3-pip

# Copy backend from backend stage
COPY --from=backend /app /app

# Copy frontend build from frontend stage
COPY --from=frontend /app/frontend/build /usr/share/nginx/html

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Create startup script
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

# Expose ports
EXPOSE 80 5000

# Start services
CMD ["/start.sh"]

# Development image
FROM base as development

WORKDIR /app

# Install development dependencies
RUN pip install --no-cache-dir \
    jupyter \
    ipython \
    pytest \
    black \
    flake8 \
    mypy

# Copy all code
COPY . .

# Create development script
COPY docker/dev-start.sh /dev-start.sh
RUN chmod +x /dev-start.sh

# Expose ports for development
EXPOSE 5000 8888

# Start development environment
CMD ["/dev-start.sh"]
