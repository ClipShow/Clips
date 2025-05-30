from flask import Flask, request, jsonify, send_from_directory
import subprocess
import uuid
import os

app = Flask(__name__)
VIDEO_FOLDER = os.path.join(os.getcwd(), "videos")
os.makedirs(VIDEO_FOLDER, exist_ok=True)

@app.route("/clip", methods=["POST"])
def clip_video():
    data = request.get_json()
    video_url = data.get("url")
    creator = data.get("creator", "unknown")

    if not video_url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    video_id = str(uuid.uuid4())
    input_path = os.path.join(VIDEO_FOLDER, f"{video_id}_input.mp4")
    output_path = os.path.join(VIDEO_FOLDER, f"{video_id}.mp4")

    try:
        # Download video with yt-dlp and cookies
        subprocess.run([
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "best[ext=mp4]/mp4",
            "-o", input_path,
            video_url
        ], check=True)

        # Clip video with ffmpeg
        subprocess.run([
            "ffmpeg", "-y",
            "-i", input_path,
            "-ss", "00:00:05", "-t", "00:00:30",
            "-vf", "scale=720:1280",
            output_path
        ], check=True)

        clip_url = f"/videos/{os.path.basename(output_path)}"
        return jsonify({
            "clipUrl": clip_url,
            "creator": creator
        })

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Processing failed", "details": str(e)}), 500

@app.route("/videos/<filename>")
def serve_video(filename):
    return send_from_directory(VIDEO_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
