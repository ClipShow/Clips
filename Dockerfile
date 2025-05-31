FROM python:3.12-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install flask yt-dlp gunicorn

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Expose the port Railway will call
EXPOSE 5000

# Launch with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
