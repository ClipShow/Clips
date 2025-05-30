from flask import Flask, request, jsonify, send_from_directory
import subprocess
import uuid
import os

app = Flask(__name__)
CLIP_FOLDER = "clips"
os.makedirs(CLIP_FOLDER, exist_ok=True)

@app.route("/clip", methods=["POST"])
def clip_video():
    data = request.get_json()
    video_url = data.get("url")
    creator = data.get("creator", "unknown")

    if not video_url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    video_id = str(uuid.uuid4())
    output_filename = f"{video_id}.mp4"
    output_path = os.path.join(CLIP_FOLDER, output_filename)

    try:
        # Download video
        subprocess.run([
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "-o", "input.%(ext)s",
            video_url
        ], check=True)

        # Clip 30 seconds from 5s mark
        subprocess.run([
            "ffmpeg", "-y",
            "-i", "input.mp4",
            "-ss", "00:00:05", "-t", "00:00:30",
            "-vf", "scale=720:1280",
            output_path
        ], check=True)

        # Serve full URL
        base_url = request.url_root.rstrip("/")
        return jsonify({
            "clipUrl": f"{base_url}/clips/{output_filename}",
            "creator": creator
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500

@app.route("/clips/<filename>")
def serve_clip(filename):
    return send_from_directory(CLIP_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
