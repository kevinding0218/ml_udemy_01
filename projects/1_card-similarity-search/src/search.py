"""
search.py — Query the card dataset by text or image and return the top-K most similar cards.

Requires embeddings to be precomputed first:
    python src/encode_dataset.py

Public API (import these in your own code or in demo.py):
    search_by_text(query, top_k, threshold)  → list of result dicts
    search_by_image(image_source, top_k, threshold) → list of result dicts
"""

import json
import numpy as np
from pathlib import Path
from PIL import Image
from utils import encode_text, encode_image, load_image_from_url, load_image_from_path, cosine_similarity

EMBEDDINGS_PATH = Path(__file__).parent.parent / "embeddings" / "card_embeddings.npy"
INDEX_PATH = Path(__file__).parent.parent / "embeddings" / "card_index.json"
DATA_PATH = Path(__file__).parent.parent / "data" / "cards.json"

# Module-level cache — assets are loaded once on first query and reused for every
# subsequent call. This makes repeated queries fast (no disk I/O after the first).
_embeddings = None   # numpy matrix (N_cards, 512) — one row per card
_index = None        # list of cardIds in the same order as rows in _embeddings
_cards_by_id = None  # dict {cardId: card_dict} for fast lookup when building results


def _load_assets():
    """Load embeddings and card data from disk into memory (once).

    Raises FileNotFoundError with a helpful message if encode_dataset.py
    has not been run yet — the most common setup mistake.
    """
    global _embeddings, _index, _cards_by_id
    if _embeddings is None:
        if not EMBEDDINGS_PATH.exists():
            raise FileNotFoundError(
                "Embeddings not found. Run: python src/encode_dataset.py"
            )
        _embeddings = np.load(EMBEDDINGS_PATH)      # shape (N, 512)
        with open(INDEX_PATH) as f:
            _index = json.load(f)                   # ["card-001", "card-002", ...]
        with open(DATA_PATH) as f:
            cards = json.load(f)
        _cards_by_id = {c["cardId"]: c for c in cards}


def search_by_text(query: str, top_k: int = 3, threshold: float = 0.20) -> list[dict]:
    """Find the most similar cards to a text query.

    Args:
        query:     Any free-form text, e.g. "a fire-breathing creature" or "defensive warrior".
        top_k:     Maximum number of results to return (default 3).
        threshold: Minimum similarity score to include a result (0–1).
                   Cards scoring below this are excluded even if they're the closest matches.
                   Note: CLIP scores cluster between ~0.70–0.85, so a low default (0.20)
                   effectively means "return everything and let top_k do the filtering".

    Returns:
        List of dicts, each with: cardId, description, aspects, imageUrl, score.
        Sorted by score descending. May be shorter than top_k if threshold filters results.
    """
    _load_assets()
    # Encode the query text the same way card descriptions were encoded at index time.
    # encode_text returns (1, 512); [0] extracts the single vector → shape (512,).
    query_vec = encode_text([query])[0]
    return _rank(query_vec, top_k, threshold)


def search_by_image(image_source: str, top_k: int = 3, threshold: float = 0.20) -> list[dict]:
    """Find the most similar cards to an image query.

    Because CLIP maps both text and images into the same vector space, this
    works even if the card embeddings were built from text only — the image query
    vector will be compared against text-derived card vectors directly.

    Args:
        image_source: Either a local file path (e.g. "./my_card.png") or an
                      HTTP/HTTPS URL. The image is loaded and encoded by CLIP.
        top_k:        Maximum number of results to return.
        threshold:    Minimum similarity score.

    Returns:
        Same format as search_by_text.
    """
    _load_assets()

    # Detect URL vs local path and load accordingly.
    if image_source.startswith("http://") or image_source.startswith("https://"):
        image = load_image_from_url(image_source)
        if image is None:
            raise ValueError(f"Could not load image from URL: {image_source}")
    else:
        image = load_image_from_path(image_source)

    query_vec = encode_image(image)[0]
    return _rank(query_vec, top_k, threshold)


def _rank(query_vec: np.ndarray, top_k: int, threshold: float) -> list[dict]:
    """Core ranking logic shared by both search functions.

    Steps:
    1. Compute a similarity score between the query and every card in the dataset.
    2. Sort cards by score, highest first.
    3. Take only the top_k candidates.
    4. Drop any that fall below the threshold.
    5. Look up full card details and return a clean result list.

    Args:
        query_vec: 1-D normalized numpy array, shape (512,).
        top_k:     Max results.
        threshold: Min score to keep.
    """
    # cosine_similarity returns a 1-D array of length N_cards.
    # argsort gives indices sorted ascending; [::-1] reverses to descending.
    scores = cosine_similarity(query_vec, _embeddings)
    sorted_indices = np.argsort(scores)[::-1]

    results = []
    for idx in sorted_indices[:top_k]:
        score = float(scores[idx])
        # Stop early if remaining scores are all below threshold (list is sorted).
        if score < threshold:
            break
        card_id = _index[idx]
        card = _cards_by_id[card_id]
        results.append({
            # --- from the vector ---
            # Only `score` comes from the embedding. The vector decided this card
            # was returned; it knows nothing about the fields below.
            "score": round(score, 4),

            # --- metadata (from cards.json) ---
            # These fields play no part in similarity search. They are looked up
            # from cards.json after the vector search is done and attached to the
            # result so the caller doesn't need a second lookup.
            # Adding or changing these fields never requires re-running encode_dataset.py.
            "cardId":      card_id,
            "description": card["description"],
            "aspects":     card["aspects"],
            "imageUrl":    card.get("imageUrl", ""),
            "releaseId":   card.get("releaseId", ""),
            "releaseDate": card.get("releaseDate", ""),
        })

    return results
