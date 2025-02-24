from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
load_dotenv()  # Loads variables from .env file
import os

app = Flask(__name__)

proxyUserName = os.getenv('PROXY_USERNAME')
proxyPassword = os.getenv('PROXY_PASSWORD')

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    proxy = {
            "https": f"https://{proxyUserName}:{proxyPassword}@gate.smartproxy.com:10001"
            }

    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxy)
        transcript_text = " ".join([t['text'] for t in transcript])
        return jsonify({"transcript": transcript_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)