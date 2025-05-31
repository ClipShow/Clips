from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)
app.static_folder = os.getcwd()

@app.route("/clip", methods=["POST"])
def clip_video():
    try:
        data = request.get_json()
        video_url = data.get("url")
        creator = data.get("creator", "unknown")

        if not video_url:
            return jsonify({"error": "Missing YouTube URL"}), 400

        video_id = str(uuid.uuid4())
        output_filename = f"{video_id}.mp4"

        print(f"🎬 Clipping video for {creator}: {video_url}")

        subprocess.run([
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "-o", "input.%(ext)s",
            video_url
        ], check=True)

        subprocess.run([
            "ffmpeg", "-y",
            "-i", "input.mp4",
            "-ss", "00:00:05", "-t", "00:00:30",
            "-vf", "scale=720:1280",
            output_filename
        ], check=True)

        return jsonify({
            "clipUrl": f"/videos/{output_filename}",
            "creator": creator
        })

    except subprocess.CalledProcessError as e:
        print(f"❌ Subprocess error: {e}")
        return jsonify({"error": "Subprocess failed", "details": str(e)}), 500
    except Exception as e:
        print(f"❌ General error: {e}")
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

@app.route("/videos/<filename>")
def serve_video(filename):
    return app.send_static_file(filename)

@app.route("/")  # Healthcheck
def home():
    return "OK", 200
