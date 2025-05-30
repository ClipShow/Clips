FROM python:3.12-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install flask yt-dlp

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Expose port
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
