# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Update the package list and install system dependencies
RUN apt-get update -y && \
    apt-get install -y \
    libopenblas-dev \
    liblapack-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxinerama1 \
    libxi6 \
    mesa-common-dev \
    libegl1-mesa \
    libegl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set environment variables for CPU operation
ENV MEDIAPIPE_DISABLE_GPU=1
ENV KMP_DUPLICATE_LIB_OK=True
ENV OMP_NUM_THREADS=4
ENV MKL_NUM_THREADS=4
ENV OPENBLAS_NUM_THREADS=4
ENV NUMEXPR_NUM_THREADS=4
ENV VECLIB_MAXIMUM_THREADS=4
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/Uploaded_Files /app/static/frames /app/static/graphs /app/Admin/datasets /app/instance

# Set proper permissions
RUN chmod -R 755 /app/static /app/Admin

# Expose the port
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:10000/ || exit 1

# Run the application with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--workers", "1", "--timeout", "300", "wsgi:app"]
