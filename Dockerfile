FROM python:3.12-slim

# Install system packages
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install --no-cache-dir flask gunicorn yt-dlp

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Expose port (important for Railway's routing)
EXPOSE 5000

# ✅ Run using Gunicorn (matches Procfile)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
