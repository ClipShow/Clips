FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install flask yt-dlp gunicorn

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Expose port
EXPOSE 5000

# Use Gunicorn to serve app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
