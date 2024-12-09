FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy project files
# COPY models /app/models
COPY . /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir ultralytics fastapi uvicorn pillow python-multipart

# Expose port for FastAPI
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
