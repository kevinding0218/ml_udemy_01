"""
encode_dataset.py — Offline script: encode all cards and save their embeddings to disk.

Run this once before using search.py, and re-run it whenever you change cards.json.

    python src/encode_dataset.py

What it produces:
    embeddings/card_embeddings.npy  — a matrix of shape (N, 512) where N = number of cards.
                                      Each row is the normalized embedding for one card.
    embeddings/card_index.json      — an ordered list of cardIds that maps row numbers in
                                      the matrix back to actual card identifiers.
                                      Row 0 in the matrix = card_index[0].

Why offline?
    Encoding is slow (runs the neural network). We do it once and save the results so that
    every query just does a fast vector comparison instead of re-running the model on all cards.
"""

import json
import numpy as np
from pathlib import Path
from utils import encode_text, encode_image, load_image_from_url, card_to_text

# Resolve paths relative to this file so the script works from any working directory.
DATA_PATH = Path(__file__).parent.parent / "data" / "cards.json"
EMBEDDINGS_PATH = Path(__file__).parent.parent / "embeddings" / "card_embeddings.npy"
INDEX_PATH = Path(__file__).parent.parent / "embeddings" / "card_index.json"


def encode_dataset():
    with open(DATA_PATH) as f:
        cards = json.load(f)

    embeddings = []
    index = []  # ordered list of cardIds — position here matches row in embeddings matrix

    for card in cards:
        print(f"Encoding {card['cardId']}...")

        # Step 1: encode the card's text (description + aspects) into a 512-dim vector.
        # encode_text returns shape (1, 512); [0] takes the single row → shape (512,).
        text_vec = encode_text([card_to_text(card)])[0]
        vectors = [text_vec]

        # Step 2 (optional): if the card has an image, encode that too.
        # Having both a text AND image embedding lets us average them for a richer
        # representation that captures visual style in addition to the text description.
        image_url = card.get("imageUrl", "")
        if image_url:
            image = load_image_from_url(image_url)
            if image is not None:
                image_vec = encode_image(image)[0]
                vectors.append(image_vec)
            else:
                print(f"  Warning: could not load image for {card['cardId']}")

        # Step 3: combine modalities by averaging.
        # If only text was available, mean([text_vec]) == text_vec.
        # If both text and image were available, we get a vector in between.
        # After averaging, re-normalize so the result is still unit length.
        combined = np.mean(vectors, axis=0)
        norm = np.linalg.norm(combined)
        combined = combined / max(norm, 1e-8)

        embeddings.append(combined)
        index.append(card["cardId"])

    # Stack all per-card vectors into one matrix: shape (N_cards, 512).
    # float32 is standard for neural network weights — smaller than float64, no quality loss.
    embeddings_matrix = np.array(embeddings, dtype=np.float32)

    # Persist both files so search.py can load them without re-running the model.
    EMBEDDINGS_PATH.parent.mkdir(exist_ok=True)
    np.save(EMBEDDINGS_PATH, embeddings_matrix)

    with open(INDEX_PATH, "w") as f:
        json.dump(index, f)

    print(f"\nSaved {len(embeddings)} embeddings → {EMBEDDINGS_PATH}")
    print(f"Embedding matrix shape: {embeddings_matrix.shape}")


if __name__ == "__main__":
    encode_dataset()
