# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV MEDIAPIPE_DISABLE_GPU=1
ENV KMP_DUPLICATE_LIB_OK=True
ENV OMP_NUM_THREADS=4
ENV MKL_NUM_THREADS=4
ENV OPENBLAS_NUM_THREADS=4
ENV NUMEXPR_NUM_THREADS=4
ENV VECLIB_MAXIMUM_THREADS=4

# Set the working directory inside the container
WORKDIR /app

# Update the package list and install system dependencies
# Using a more robust approach that handles different Debian versions
RUN apt-get update -y && \
    apt-get install -y \
    libopenblas-dev \
    liblapack-dev \
    libglib2.0-0 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxinerama1 \
    libxi6 \
    gcc \
    g++ \
    curl \
    && \
    # Try to install OpenGL packages with fallbacks
    (apt-get install -y libgl1 || apt-get install -y libgl1-mesa-glx || true) && \
    (apt-get install -y libglu1-mesa || apt-get install -y libglu1-mesa-dev || true) && \
    (apt-get install -y mesa-common-dev || true) && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create necessary directories
RUN mkdir -p Uploaded_Files static/frames static/graphs Admin/datasets instance

# Set proper permissions
RUN chmod -R 755 static/ && \
    chmod -R 755 Uploaded_Files/ && \
    chmod -R 755 Admin/

# Expose the port
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:10000/ || exit 1

# Run the application
CMD ["python", "server.py"]
