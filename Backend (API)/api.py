from flask import Flask, request, jsonify
import pandas as pd
import json
import os
from io import BytesIO, StringIO
import base64
import utils
import requests

PORT = int(os.environ.get("PORT", 7860))

app = Flask(__name__)

# Load resources at startup (assumes NLTK data is pre-installed via Dockerfile)
nlp = utils.load_spacy_model()  # en_core_web_sm from requirements.txt
sia = utils.get_sentiment_analyzer()  # vader_lexicon from Dockerfile


@app.route("/", methods=["GET"])
def home():
    return {"message": "Financial News Analysis API is running!"}, 200


@app.route('/api/news/fetch', methods=['POST'])
def fetch_news():
    data = request.json
    company = data.get('company', '').strip().upper()
    if not company:
        return jsonify({"error": "No company symbol provided"}), 400
    csv_buffer = utils.process_news_data(company, nlp)
    if csv_buffer is None:
        return jsonify({"error": f"No news data found for {company}"}), 404
    csv_b64 = base64.b64encode(csv_buffer.getvalue().encode()).decode()
    return jsonify({"success": True, "file": csv_b64}), 200


@app.route('/api/news/analyze', methods=['POST'])
def analyze_news():
    data = request.json
    company = data.get('company', '').strip().upper()
    csv_b64 = data.get('file')
    if not company or not csv_b64:
        return jsonify({"error": "Missing company symbol or file"}), 400
    csv_data = base64.b64decode(csv_b64).decode()
    csv_buffer = StringIO(csv_data)
    output_data, audio_buffer = utils.analyze_news_data(csv_buffer, company, nlp, sia)
    audio_b64 = base64.b64encode(audio_buffer.getvalue()).decode()
    json_str = json.dumps(output_data, ensure_ascii=False)
    return jsonify({
        "output_data": output_data,
        "audio_file": audio_b64,
        "output_file": f"{company}_news_output.json",
        "json_str": json_str
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)