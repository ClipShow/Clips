# === app.py (Flask backend) ===
from flask import Flask, request, jsonify
import subprocess
import uuid
import os
import traceback

app = Flask(__name__)
app.static_folder = os.getcwd()

@app.route("/clip", methods=["POST"])
def clip_video():
    data = request.get_json()
    video_url = data.get("url")
    creator = data.get("creator", "unknown")

    if not video_url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    video_id = str(uuid.uuid4())
    output_filename = f"{video_id}.mp4"

    try:
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

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500

@app.route("/videos/<filename>")
def serve_video(filename):
    return app.send_static_file(filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


// === Google Apps Script ===
const YOUTUBE_API_KEY = 'AIzaSyBgOuxKwu_ytl8nL7spHywYI8xMUkIyQnk';
const CLIPPER_URL = 'https://clips-production.up.railway.app/clip';

function fetchLatestYouTubeVideos() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const streamerSheet = ss.getSheetByName("Streamers");
  const videoSheet = ss.getSheetByName("Videos") || ss.insertSheet("Videos");

  videoSheet.clearContents().appendRow([
    "ChannelName", "ChannelID", "VideoTitle", "VideoID", "PublishedAt", "YouTubeLink", "ClippedVideoURL"
  ]);

  const data = streamerSheet.getRange(2, 1, streamerSheet.getLastRow() - 1, 6).getValues();

  data.forEach(row => {
    const channelName = row[0];
    const channelID = row[5];

    if (!channelID || !channelID.startsWith("UC")) return;

    const url = `https://www.googleapis.com/youtube/v3/search?key=${YOUTUBE_API_KEY}&channelId=${channelID}&part=snippet,id&order=date&maxResults=1`;

    try {
      const response = UrlFetchApp.fetch(url);
      const json = JSON.parse(response.getContentText());
      const video = json.items?.[0];

      if (video && video.id.kind === "youtube#video") {
        const videoID = video.id.videoId;
        const videoTitle = video.snippet.title;
        const publishedAt = video.snippet.publishedAt;
        const videoURL = `https://www.youtube.com/watch?v=${videoID}`;

        videoSheet.appendRow([
          channelName, channelID, videoTitle, videoID, publishedAt, videoURL, ""
        ]);
      }
    } catch (e) {
      Logger.log(`❌ Error fetching for ${channelName}: ${e}`);
    }
  });
}

function triggerClipperAPI() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Videos");
  const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 7).getValues();

  data.forEach((row, i) => {
    const [channelName, , videoTitle, , , youtubeUrl, existingClip] = row;

    if (!youtubeUrl || !youtubeUrl.includes("youtube.com/watch")) return;
    if (existingClip && existingClip !== "") return;

    const payload = {
      url: youtubeUrl,
      creator: channelName,
      title: videoTitle
    };

    const options = {
      method: "POST",
      contentType: "application/json",
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    try {
      const response = UrlFetchApp.fetch(CLIPPER_URL, options);
      const resultText = response.getContentText();

      try {
        const result = JSON.parse(resultText);

        if (result.clipUrl) {
          Logger.log(`✅ ${channelName}: ${result.clipUrl}`);
          sheet.getRange(i + 2, 7).setValue(result.clipUrl);
        } else {
          Logger.log(`⚠️ No clip returned for ${channelName}: ${JSON.stringify(result)}`);
        }
      } catch (parseErr) {
        Logger.log(`❌ JSON parse error for ${channelName}: ${resultText}`);
      }
    } catch (e) {
      Logger.log(`❌ Error clipping ${channelName}: ${e}`);
    }
  });
}
