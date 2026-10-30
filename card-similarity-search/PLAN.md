# Card Similarity Search — Implementation Plan

## Approach Summary

Use **CLIP** (Contrastive Language–Image Pretraining) as a pretrained feature extractor.
CLIP encodes both text and images into the same vector space, making cross-modal similarity search possible without any training.

Similarity search is done via **cosine similarity** over stored embeddings (numpy for v1).

---

## Phases

### Phase 1 — Project Setup ✅
- [x] Create project folder structure (see below)
- [x] Set up Python virtual environment (`.venv/`)
- [x] Install dependencies: `transformers`, `torch`, `Pillow`, `numpy`, `requests`
- [x] Create `requirements.txt`

**Folder structure:**
```
card-similarity-search/
├── REQUIREMENTS.md
├── PLAN.md
├── data/
│   └── cards.json            # card dataset (cardId, description, aspects, imageUrl)
├── embeddings/
│   └── card_embeddings.npy   # precomputed vectors (generated, not committed)
├── src/
│   ├── encode_dataset.py     # offline: encode all cards → save embeddings
│   ├── search.py             # query function: text or image → top-K results
│   └── utils.py              # shared helpers (load model, cosine sim, etc.)
├── tests/
│   └── test_search.py        # manual + automated tests
└── demo.py                   # interactive demo / quick test runner
```

---

### Phase 2 — Encode the Dataset (offline) ✅

**File:** `src/encode_dataset.py`

Steps:
1. Load the CLIP model and processor from HuggingFace
2. Load `data/cards.json`
3. For each card:
   - Encode `description + " " + " ".join(aspects)` with the CLIP **text encoder**
   - Optionally fetch and encode the image from `imageUrl` with the CLIP **image encoder**
   - Average text + image embeddings (if image available), else use text only
4. Normalize all embeddings to unit vectors (required for cosine similarity to work correctly)
5. Save a mapping: `{ cardId: embedding_vector }` → `embeddings/card_embeddings.npy`

> Run this once. Re-run only when the dataset changes.

---

### Phase 3 — Query / Search ✅

**File:** `src/search.py`

Steps:
1. Load precomputed embeddings from `card_embeddings.npy`
2. Accept query input:
   - If text → encode with CLIP text encoder, normalize
   - If image (path or URL) → encode with CLIP image encoder, normalize
3. Compute cosine similarity between query vector and all stored vectors
4. Sort by similarity descending, take top K (default K=3)
5. Filter out results below a minimum threshold (default `0.20`)
6. Return list of `{ cardId, description, imageUrl, score }`

---

### Phase 4 — Test & Evaluate ✅

**Manual tests (start here):**
- Query with a card's own description → should return that card as #1
- Query with a paraphrased description → should still return the correct card highly ranked
- Query with an unrelated description → should return low scores or empty
- Query with a card's own image → should return that card or close relatives

**Automated tests (`tests/test_search.py`):**
- Load a small fixed test dataset (10–20 cards)
- Assert known queries return expected `cardId` in top 3
- Assert score for a self-query is > 0.80
- Assert an obviously unrelated query scores < threshold

**Metric to track:** Recall@3 — out of N test queries with a known correct card, how many find it in the top 3?

---

### Phase 5 — Tune (only if Phase 4 results are poor)

Tune in this order — stop as soon as results are good enough:

| Step | What to try |
|------|-------------|
| 5a | Adjust similarity threshold (lower = more results, higher = stricter) |
| 5b | Try a larger CLIP model: `clip-vit-large-patch14` |
| 5c | Try combining text embedding differently (e.g. weight description vs aspects separately) |
| 5d | Fine-tune CLIP on your (image, description) pairs using contrastive loss |

Fine-tuning (5d) is a last resort and requires a reasonably sized labeled dataset (100+ pairs minimum).

---

### Phase 6 — Flask REST API ✅

**File:** `src/api.py`

Exposes the search system over HTTP so any app or tool can query it without importing Python.

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Liveness check — confirms server is running |
| `/search/text` | POST | Search by text description |
| `/search/image` | POST | Search by image URL |

Both search endpoints accept JSON body with `query`/`image_url`, optional `top_k` and `threshold`,
and return a JSON list of matching cards with scores.

Start the server:
```bash
python src/api.py        # runs on port 8005
```

---

### Phase 7 — Production Architecture (reference)

> Not implemented — documented for learning and future reference.

#### What changes in production vs this POC

| Concern | POC (now) | Production |
|---------|-----------|------------|
| Vector storage | `.npy` file on disk | **Vector DB** (Qdrant recommended) |
| Adding a new card | Re-run `encode_dataset.py` on full dataset | Upsert one vector via API |
| Search speed | Scans all rows in RAM | HNSW index — sub-10ms at millions of cards |
| Filter by aspect | Post-process in Python | Native metadata filter in vector DB query |
| API server | Flask single-process | Gunicorn + multiple workers, or containerised |
| Model loading | Loaded per-process at startup | Shared model server (Triton / TorchServe) |
| Embedding new cards | Manual script | Async worker triggered by card create/update event |

#### Production data flow

```
[Card CMS / Admin]
      │  card created or updated
      ▼
[Embedding Worker]     ← background job (queue / cron)
      │  1. Fetch card from DB
      │  2. Encode text + image via CLIP (model unchanged)
      │  3. Upsert vector into Qdrant with metadata
      ▼
[Qdrant Vector DB]
      ▲
      │  ANN search at query time
[Search API (Flask)]   ← stateless, no model loaded here
      │  1. Encode incoming query (one CLIP forward pass)
      │  2. Query Qdrant for top-K neighbours
      │  3. Return results
      ▼
[Your app / frontend]
```

#### Key insight: re-embed, don't retrain

When cards change, you only re-run CLIP (the encoder) on the new/changed cards.
The model weights never change unless you explicitly fine-tune (Phase 5d).
This makes card updates cheap and decoupled from the search API.

#### Recommended vector DB: Qdrant

- Runs locally via Docker: `docker run -p 6333:6333 qdrant/qdrant`
- Stores metadata (description, aspects, imageUrl) alongside vectors — no separate `cards.json` needed
- Supports metadata filters: e.g. "top-3 matches that have `aspects` containing `fire`"
- Free managed cloud tier available for small datasets

---

## Decision Log

| Date | Decision | Reason |
|------|----------|--------|
| 2026-10-29 | Use CLIP zero-shot (no fine-tuning) for v1 | Evaluate quality before investing in training |
| 2026-10-29 | Use numpy for similarity search (no vector DB) | Dataset assumed < 10k cards; keep it simple |
| 2026-10-29 | Combine text + image embeddings by averaging | Simple and effective for mixed-modal cards |
| 2026-10-29 | Drop absolute threshold test; use relative score gap instead | CLIP cosine scores cluster high (0.7+) even for unrelated queries — absolute thresholds are unreliable; use ranking, not score magnitude, to judge relevance |
