from flask import Flask, request, jsonify, send_from_directory
import subprocess, uuid, os

app = Flask(__name__)

# Serve videos from this folder
VIDEO_DIR = os.path.join(os.getcwd(), "videos")
os.makedirs(VIDEO_DIR, exist_ok=True)

@app.route("/clip", methods=["POST"])
def clip_video():
    try:
        data = request.get_json()
        video_url = data.get("url")
        creator = data.get("creator", "unknown")

        if not video_url:
            return jsonify({"error": "Missing YouTube URL"}), 400

        video_id = str(uuid.uuid4())
        output_path = os.path.join(VIDEO_DIR, f"{video_id}.mp4")

        # Download full video
        subprocess.run([
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "-o", "input.%(ext)s",
            video_url
        ], check=True)

        # Clip 30s from 5s
        subprocess.run([
            "ffmpeg", "-y",
            "-i", "input.mp4",
            "-ss", "00:00:05", "-t", "00:00:30",
            "-vf", "scale=720:1280",
            output_path
        ], check=True)

        return jsonify({
            "clipUrl": f"/videos/{video_id}.mp4",
            "creator": creator
        })

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Subprocess failed", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

@app.route("/videos/<filename>")
def serve_video(filename):
    return send_from_directory(VIDEO_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
