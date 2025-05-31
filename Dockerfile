FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install flask gunicorn

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Expose port
EXPOSE 5000

# Run using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
