FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        pkg-config \
        libgtk-3-dev \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libv4l-dev \
        libxvidcore-dev \
        libx264-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        gfortran \
        openexr \
        liblapack-dev \
        libblas-dev \
        libhdf5-dev \
        libtbb-dev \
        libtbbmalloc2 \
        libopenblas-dev \
        liblapacke-dev \
        wget \
        curl \
        git \
        unzip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenCV with contrib modules
RUN pip install --no-cache-dir opencv-python-headless==4.8.1.78

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p /app/models /app/data /app/logs

# Download YOLOv8 model
RUN python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Expose port
EXPOSE 800

# Run the application
CMD ["python", "analyzer_service.py"]