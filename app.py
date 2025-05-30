from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)
app.static_folder = os.getcwd()

@app.route("/clip", methods=["POST"])
def clip_video():
    data = request.get_json()
    video_url = data.get("url")
    creator = data.get("creator", "unknown")

    print(f"📥 Received clip request for: {video_url} from {creator}")

    if not video_url:
        print("❌ Missing YouTube URL")
        return jsonify({"error": "Missing YouTube URL"}), 400

    video_id = str(uuid.uuid4())
    output_filename = f"{video_id}.mp4"

    try:
        # Step 1: Download the video using yt-dlp
        print("⬇️ Downloading video with yt-dlp...")
        subprocess.run([
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "-o", "input.%(ext)s",
            video_url
        ], check=True)
        print("✅ Download complete.")

        # Step 2: Clip the video using ffmpeg
        print("🎞️ Clipping video with ffmpeg...")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", "input.mp4",
            "-ss", "00:00:05", "-t", "00:00:30",
            "-vf", "scale=720:1280",
            output_filename
        ], check=True)
        print(f"✅ Clip complete: {output_filename}")

        # Step 3: Return the URL
        return jsonify({
            "clipUrl": f"/videos/{output_filename}",
            "creator": creator
        })

    except subprocess.CalledProcessError as e:
        print(f"🚨 Error during processing: {e}")
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500

@app.route("/videos/<filename>")
def serve_video(filename):
    return app.send_static_file(filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
