from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
import os

app = Flask(__name__)
AUDIO_FOLDER = "static/audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/tts', methods=['POST'])
def tts():
    text = request.json.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    filename = f"{abs(hash(text))}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)

    if not os.path.exists(filepath):
        tts = gTTS(text)
        tts.save(filepath)

    full_url = request.host_url + f"static/audio/{filename}"
    return jsonify({"audio_url": full_url})

@app.route('/static/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)
