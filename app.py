from flask import Flask, request, jsonify, send_from_directory
import subprocess
import uuid
import os

app = Flask(__name__)
OUTPUT_DIR = "videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/clip", methods=["POST"])
def clip_video():
    data = request.get_json()
    video_url = data.get("url")
    creator = data.get("creator", "unknown")

    if not video_url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    try:
        # Step 1: Download YouTube video
        input_filename = "input.mp4"
        subprocess.run([
            "yt-dlp",
            "--no-warnings",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "-o", input_filename,
            video_url
        ], check=True)

        # Step 2: Clip 30s from 5s mark
        clip_id = str(uuid.uuid4())
        output_filename = f"{clip_id}.mp4"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        subprocess.run([
            "ffmpeg", "-y",
            "-i", input_filename,
            "-ss", "00:00:05", "-t", "00:00:30",
            "-vf", "scale=720:1280",
            output_path
        ], check=True)

        return jsonify({
            "clipUrl": f"/videos/{output_filename}",
            "creator": creator
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Clipping failed",
            "details": str(e)
        }), 500

@app.route("/videos/<path:filename>")
def serve_clip(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
