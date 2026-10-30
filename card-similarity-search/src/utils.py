# utils.py — shared helpers used by both encode_dataset.py and search.py.
# Nothing here is specific to cards; it's all generic CLIP + image utilities.

import numpy as np
import requests
from PIL import Image
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel
import torch

# Which pretrained CLIP variant to use.
# "vit-base-patch32" is the smallest/fastest. Swap for "vit-large-patch14" for
# better quality at the cost of more memory and slower inference.
MODEL_NAME = "openai/clip-vit-base-patch32"

# Module-level cache so the model is only loaded once per Python process.
# The first call to load_model() downloads ~600MB from HuggingFace (cached locally
# afterward). Every subsequent call returns the already-loaded object instantly.
_model = None
_processor = None


def load_model():
    """Load (or return the cached) CLIP model and processor.

    CLIPModel       — the neural network that produces embeddings.
    CLIPProcessor   — handles tokenizing text and resizing/normalizing images
                      into the exact format CLIP expects before inference.

    model.eval() puts the model in inference mode (disables dropout etc.).
    """
    global _model, _processor
    if _model is None:
        print(f"Loading CLIP model ({MODEL_NAME})...")
        _model = CLIPModel.from_pretrained(MODEL_NAME)
        _processor = CLIPProcessor.from_pretrained(MODEL_NAME)
        _model.eval()
        print("Model loaded.")
    return _model, _processor


def encode_text(texts: list[str]) -> np.ndarray:
    """Convert a list of text strings into a matrix of CLIP embeddings.

    Each string is independently encoded into a 512-dimensional vector.
    The returned matrix has shape (len(texts), 512) and every row is
    already unit-normalized (length = 1), which is required for cosine
    similarity to work correctly.

    Why torch.no_grad()?
    During normal training, PyTorch records every operation so it can
    compute gradients for backprop. We're only doing inference here, so
    we disable that bookkeeping to save memory and speed things up.
    """
    model, processor = load_model()
    # processor turns raw strings into token IDs + attention masks that CLIP understands.
    # padding=True makes all sequences the same length; truncation=True cuts anything too long.
    inputs = processor(text=texts, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        out = model.get_text_features(**inputs)
    # Newer transformers versions may wrap the tensor in a model-output object.
    vec = out if isinstance(out, torch.Tensor) else out.pooler_output
    return _normalize(vec.detach().numpy())


def encode_image(image: Image.Image) -> np.ndarray:
    """Convert a PIL Image into a CLIP embedding vector.

    Returns shape (1, 512) — normalized, ready for cosine similarity.
    CLIP resizes and normalizes the image internally via the processor,
    so you don't need to do any preprocessing yourself.
    """
    model, processor = load_model()
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        out = model.get_image_features(**inputs)
    vec = out if isinstance(out, torch.Tensor) else out.pooler_output
    return _normalize(vec.detach().numpy())


def load_image_from_url(url: str) -> Image.Image | None:
    """Download an image from a URL and return it as a PIL Image.

    Returns None (instead of raising) if the download fails or times out,
    so the caller can gracefully fall back to text-only encoding.
    convert("RGB") strips alpha channels and ensures a consistent 3-channel format.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGB")
    except Exception:
        return None


def load_image_from_path(path: str) -> Image.Image:
    """Load a local image file as a PIL Image."""
    return Image.open(path).convert("RGB")


def cosine_similarity(query: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Compute the cosine similarity between one query vector and every row in matrix.

    Cosine similarity measures the angle between two vectors.
    - Score = 1.0  → vectors point in exactly the same direction (identical meaning)
    - Score = 0.0  → vectors are perpendicular (unrelated)
    - Score = -1.0 → vectors point in opposite directions

    Because both inputs are already unit-normalized (length = 1), the dot product
    IS the cosine similarity — no division needed. This is why _normalize() is
    called everywhere before storing or querying embeddings.

    matrix @ query.T is a matrix-vector multiply producing one score per card.
    """
    # Both query and matrix rows are already unit-normalized
    return (matrix @ query.T).squeeze()


def _normalize(vectors: np.ndarray) -> np.ndarray:
    """Scale each vector to unit length (length = 1) along axis 1.

    This is required before computing cosine similarity. Without normalization,
    longer vectors would score higher simply because of their magnitude, not
    because they're semantically closer.

    np.clip(..., 1e-8, None) prevents division by zero for any all-zero vectors.
    """
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.clip(norms, 1e-8, None)


def card_to_text(card: dict) -> str:
    """Combine a card's description and aspects into a single string for encoding.

    CLIP's text encoder takes one string per card. We concatenate description
    and aspects so the model sees both when building the embedding.
    Example output: "A fierce dragon that breathes fire. fire dragon attack legendary"
    """
    aspects = " ".join(card.get("aspects", []))
    return f"{card['description']} {aspects}"
