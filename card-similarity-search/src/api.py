"""
api.py — Flask REST API for card similarity search.

Start the server:
    cd card-similarity-search
    source .venv/bin/activate
    python src/api.py

Endpoints:
    GET  /health           — check the server is up
    POST /search/text      — search by text description
    POST /search/image     — search by image URL

Prerequisites:
    Run encode_dataset.py first to build the embeddings file.
    The CLIP model is loaded once on first request and stays in memory.
"""

import sys
import json
from pathlib import Path
from flask import Flask, request, jsonify

# Add this file's directory to the path so search.py and utils.py can be imported.
sys.path.insert(0, str(Path(__file__).parent))

from search import search_by_text, search_by_image

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    """Simple liveness check.

    Useful for confirming the server started and is reachable before sending real queries.
    Returns HTTP 200 with a JSON body so clients can parse it programmatically.
    """
    return jsonify({"status": "ok"})


@app.route("/search/text", methods=["POST"])
def search_text():
    """Search for similar cards by text description.

    Request body (JSON):
        {
            "query":     "a fire breathing dragon",   // required
            "top_k":     3,                           // optional, default 3
            "threshold": 0.20                         // optional, default 0.20
        }

    Response body (JSON):
        {
            "query": "a fire breathing dragon",
            "results": [
                {
                    "cardId": "card-001",
                    "description": "...",
                    "aspects": ["fire", "dragon"],
                    "imageUrl": "...",
                    "score": 0.8228
                },
                ...
            ]
        }

    Error responses:
        400  missing or invalid "query" field
        500  embeddings not found (encode_dataset.py not run yet)
    """
    data = request.get_json(force=True)

    # Validate that the required field is present.
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Missing required field: 'query'"}), 400

    top_k = int(data.get("top_k", 3))
    threshold = float(data.get("threshold", 0.20))

    try:
        results = search_by_text(query, top_k=top_k, threshold=threshold)
    except FileNotFoundError as e:
        # Embeddings haven't been built yet.
        return jsonify({"error": str(e)}), 500

    return jsonify({"query": query, "results": results})


@app.route("/search/image", methods=["POST"])
def search_image():
    """Search for similar cards using an image URL.

    CLIP encodes the image into the same vector space as the text embeddings,
    so an image query works even when card embeddings were built from text only.

    Request body (JSON):
        {
            "image_url": "https://example.com/card.jpg",  // required
            "top_k":     3,                               // optional, default 3
            "threshold": 0.20                             // optional, default 0.20
        }

    Response body: same format as /search/text, plus "image_url" echoed back.

    Error responses:
        400  missing or invalid "image_url" field
        422  image could not be downloaded or decoded
        500  embeddings not found
    """
    data = request.get_json(force=True)

    image_url = data.get("image_url", "").strip()
    if not image_url:
        return jsonify({"error": "Missing required field: 'image_url'"}), 400

    top_k = int(data.get("top_k", 3))
    threshold = float(data.get("threshold", 0.20))

    try:
        results = search_by_image(image_url, top_k=top_k, threshold=threshold)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        # image_url was unreachable or undecodable.
        return jsonify({"error": str(e)}), 422

    return jsonify({"image_url": image_url, "results": results})


if __name__ == "__main__":
    # debug=True reloads the server on code changes — useful during development.
    # Turn it off (or remove it) before deploying to production.
    app.run(port=8005, debug=True)
