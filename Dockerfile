# Use slim Python image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install flask yt-dlp gunicorn

# Set working directory
WORKDIR /app

# Copy all app files into container
COPY . .

# Expose port for Railway
EXPOSE 5000

# Launch app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
