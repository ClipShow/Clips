FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install flask yt-dlp gunicorn

WORKDIR /app

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
