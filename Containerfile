# Base image for Raspberry Pi
FROM docker.io/library/python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-rpi.gpio \
    mpg321 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

# Set working directory and envs
WORKDIR /app
ENV PATH_AUDIO=/app/MP3

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application files
COPY app.py /app/app.py

# Expose the port Flask will use
EXPOSE 5000

# Run the Flask app
CMD ["python3", "app.py"]
