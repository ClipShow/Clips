FROM python:3.12-slim

# Install OS-level dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir flask yt-dlp gunicorn

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run app with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
