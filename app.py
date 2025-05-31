from flask import Flask, request, jsonify
import os

app = Flask(__name__)
app.static_folder = os.getcwd()

@app.route("/clip", methods=["POST"])
def clip_video():
    print("✅ /clip was triggered")
    return jsonify({"status": "OK"})

@app.route("/videos/<filename>")
def serve_video(filename):
    return app.send_static_file(filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
