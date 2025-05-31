FROM python:3.12-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install flask yt-dlp gunicorn

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Expose port
EXPOSE 5000

# Start server with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
