# Use the official Ubuntu image as the base image
FROM ubuntu:20.04

# Set environment variables for non-interactive installations
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, GStreamer, and its plugins
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libgirepository1.0-dev \
    libcairo2-dev \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-rtsp \
    gir1.2-gstreamer-1.0 \
    gir1.2-gst-rtsp-server-1.0

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the RTSP server port
EXPOSE 8554

# Run the RTSP restreamer script on container startup
CMD ["python3", "main.py", "config.txt"]
