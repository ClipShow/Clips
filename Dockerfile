FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install flask yt-dlp gunicorn

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Ensure writable directory for saving output
RUN mkdir -p /app/videos && chmod -R 777 /app/videos

# Expose Flask port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
