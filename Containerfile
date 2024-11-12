# Base image for Raspberry Pi
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-rpi.gpio \
    mpg321 \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port Flask will use
EXPOSE 5000

# Run the Flask app
CMD ["python3", "app.py"]
