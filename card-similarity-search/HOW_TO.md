# How to Use, Test, and Tune the Card Similarity Search

---

## 1. Setup (first time only)

```bash
cd card-similarity-search

# Create and activate the Python virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Mac/Linux
# .venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

The first time the model runs it downloads ~600MB from HuggingFace. It's cached
locally afterward — no internet required for future runs.

---

## 2. Add your cards

Edit `data/cards.json`. Each card must have this shape:

```json
{
  "cardId": "card-001",
  "description": "A fierce dragon that breathes scorching flames.",
  "aspects": ["fire", "dragon", "attack", "legendary"],
  "imageUrl": "https://..."   // optional — leave "" if no image
}
```

`imageUrl` is optional. If provided, the card is encoded from both text and image.
If omitted or unreachable, text-only encoding is used — results are still good.

---

## 3. Encode your dataset (run this whenever cards.json changes)

```bash
python src/encode_dataset.py
```

This runs CLIP over every card and saves the results to:
- `embeddings/card_embeddings.npy` — one 512-dim vector per card
- `embeddings/card_index.json` — ordered list of cardIds matching the matrix rows

**You must re-run this after any change to cards.json.** If you don't, searches
will use stale embeddings from before your edits.

---

## 4. Query the system

### From the command line

```bash
# Text query
python demo.py --text "a creature that controls fire"

# Image query (local file)
python demo.py --image "./path/to/card.png"

# Image query (URL)
python demo.py --image "https://example.com/card.jpg"

# More results, lower threshold
python demo.py --text "healer" --top-k 5 --threshold 0.15
```

### From your own Python code

```python
import sys
sys.path.insert(0, "src")

from search import search_by_text, search_by_image

results = search_by_text("a shadow rogue with poison daggers", top_k=3)
for r in results:
    print(r["cardId"], r["score"], r["description"])
```

### Understanding the output

```
#1  [0.8228]  card-008
     A golden phoenix reborn from ashes, radiating blinding light and scorching heat.
     Aspects: fire, light, legendary, rebirth
```

- The number in brackets is the **cosine similarity score** (0–1).
- CLIP scores typically range between **0.70 and 0.85** — this is normal.
  A score of 0.83 vs 0.78 is a meaningful difference even though both seem "high".
- Use **ranking** (position #1, #2, #3) as your primary signal, not the absolute score value.

---

## 5. Run the tests

```bash
python tests/test_search.py
```

All 6 tests should pass. The tests verify:
- A self-query (card's own description) returns that card as #1 with score > 0.80
- Paraphrased queries still find the right card in top 3
- Heal/support queries return heal/support aspect cards
- Unrelated queries score lower than relevant ones (relative gap check)
- `top_k` is respected
- High threshold correctly filters out weak matches

---

## 6. Tuning — can it be tuned?

**Yes, in several ways.** Go through these in order; stop when results are good enough.

### 6a. Adjust the threshold (free, instant)

The `threshold` parameter controls the minimum score needed to appear in results.

```bash
# Be more lenient — return more results even if similarity is weak
python demo.py --text "warrior" --threshold 0.10

# Be stricter — only return results that are clearly relevant
python demo.py --text "warrior" --threshold 0.80
```

> **When to use:** Results are clearly wrong but you just want to see more or fewer of them.

---

### 6b. Improve your card text (free, high impact)

CLIP encodes meaning from words. The richer and more precise your descriptions and aspects, the better the embeddings.

| Weaker | Stronger |
|--------|----------|
| `"aspects": ["fire"]` | `"aspects": ["fire", "dragon", "attack", "legendary", "boss"]` |
| `"description": "A dragon"` | `"description": "A fire-breathing dragon that melts steel and incinerates forests"` |

> **When to use:** First thing to try. Poor card text is the most common reason for bad results.

---

### 6c. Upgrade the CLIP model (free, moderate effort)

Change `MODEL_NAME` in `src/utils.py`:

```python
# Current (smaller, faster)
MODEL_NAME = "openai/clip-vit-base-patch32"

# Upgrade option (better quality, ~3× slower, ~3× more memory)
MODEL_NAME = "openai/clip-vit-large-patch14"
```

Then re-run `encode_dataset.py` to rebuild embeddings with the new model.

> **When to use:** Text is already good, but results are still semantically off.

---

### 6d. Weight aspects separately (code change, no training needed)

Right now, description and aspects are concatenated into one string. You can repeat
aspects or weight them more strongly:

```python
# In utils.py — card_to_text()
def card_to_text(card: dict) -> str:
    aspects = " ".join(card.get("aspects", []))
    # Repeat aspects 3× to give them more influence on the embedding
    aspects_weighted = (aspects + " ") * 3
    return f"{card['description']} {aspects_weighted}"
```

> **When to use:** Aspect-based queries work poorly but description queries are fine.

---

### 6e. Fine-tune CLIP on your dataset (most powerful, requires effort)

**What it means:** Instead of using CLIP's weights as-is, you continue training it
on your specific (image, description) pairs. After fine-tuning, the model learns
what "similar" means *for your cards specifically* — e.g., two cards from the same
faction scoring higher than two cards that share only generic attributes.

**What you need:**
- At least 100–500 (image, text) pairs from your real dataset
- A GPU (or a free Colab/Kaggle session with GPU)
- ~1–4 hours of training time

**How it works (conceptually):**
CLIP was trained with "contrastive loss" — it learns to push matching (image, text) pairs
close together and push non-matching pairs apart in the embedding space. Fine-tuning
continues that same process on your data.

**Is it worth it?**
Try steps 6a–6d first. Fine-tuning is usually only needed when:
- Your cards have very domain-specific visual style (proprietary art, unusual game aesthetics)
- Your card descriptions use custom terminology CLIP hasn't seen (invented faction names, mechanics)
- You have hundreds of cards and zero-shot results plateau under ~70% accuracy on a labeled test set

**Resources to start:**
- HuggingFace CLIP fine-tuning tutorial: search "huggingface clip fine-tuning"
- [openai/CLIP](https://github.com/openai/CLIP) — official repo with training code

---

## 7. Adding more cards over time

When you add new cards to `cards.json`:

```bash
# Re-encode the full dataset (fast, takes seconds for small datasets)
python src/encode_dataset.py

# Verify with a query that should return the new card
python demo.py --text "description of your new card"
```

There is no "incremental update" in v1 — the whole dataset is re-encoded each time.
For datasets under 10k cards this takes under a minute and is fine to re-run freely.

---

## 8. REST API

The system is accessible as a running HTTP service via Flask (`src/api.py`),
on the same port (8005) as the classifier service in section 4.

### Start the server

```bash
cd card-similarity-search
source .venv/bin/activate
python src/api.py
# → Running on http://127.0.0.1:8005
```

### Endpoints

#### `GET /health`
Confirm the server is alive.
```bash
curl http://localhost:8005/health
# {"status": "ok"}
```

#### `POST /search/text`
Search by a text description.

```bash
curl -X POST http://localhost:8005/search/text \
     -H "Content-Type: application/json" \
     -d '{"query": "a fire breathing dragon", "top_k": 3}'
```

Request body:
```json
{
  "query":     "a fire breathing dragon",
  "top_k":     3,
  "threshold": 0.20
}
```

Response:
```json
{
  "query": "a fire breathing dragon",
  "results": [
    {
      "cardId": "card-008",
      "description": "A golden phoenix reborn from ashes...",
      "aspects": ["fire", "light", "legendary", "rebirth"],
      "imageUrl": "",
      "score": 0.8228
    },
    ...
  ]
}
```

#### `POST /search/image`
Search using an image URL. CLIP encodes the image and compares it against all card embeddings.

```bash
curl -X POST http://localhost:8005/search/image \
     -H "Content-Type: application/json" \
     -d '{"image_url": "https://example.com/my_card.jpg", "top_k": 3}'
```

Request body:
```json
{
  "image_url": "https://example.com/my_card.jpg",
  "top_k":     3,
  "threshold": 0.20
}
```

Response: same format as `/search/text`, with `"image_url"` echoed back instead of `"query"`.

### Error responses

| Code | Meaning |
|------|---------|
| 400 | Missing required field (`query` or `image_url`) |
| 422 | Image URL could not be downloaded or decoded |
| 500 | Embeddings not found — run `encode_dataset.py` first |

---

## 9. Limitations to know

| Limitation | What it means |
|------------|--------------|
| CLIP scores cluster high | All scores fall between ~0.70–0.85; use ranking not absolute score |
| Text quality matters a lot | Vague descriptions produce vague matches |
| Image encoding requires working URLs | Broken imageUrls silently fall back to text-only |
| No incremental index update | Must re-run encode_dataset.py after any card change |
| No GPU needed, but it's faster with one | CPU inference is ~2–5s per query; GPU would be <100ms |
