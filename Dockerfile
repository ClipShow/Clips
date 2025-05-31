FROM python:3.12-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install --no-cache-dir flask yt-dlp gunicorn

# Set working directory
WORKDIR /app

# Copy all files (including cookies.txt, app.py, etc.)
COPY . .

# Expose port
EXPOSE 5000

# Start app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
