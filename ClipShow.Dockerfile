
# Minimal Dockerfile to test Railway build
FROM python:3.12-slim

# Install Flask
RUN pip install flask gunicorn

# Set working directory
WORKDIR /app

# Copy app
COPY app.py .

# Expose port
EXPOSE 5000

# Start with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
