FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install flask yt-dlp

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Expose port
EXPOSE 5000

# Start app using Flask's built-in server
CMD ["python", "app.py"]
