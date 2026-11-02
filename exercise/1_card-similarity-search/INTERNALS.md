# How It Works Internally

A deep-dive into what gets encoded, how queries work, and what "metadata" means
in the context of this system and vector databases.

---

## What parts of your card schema are actually used

```json
{
  "cardId":      "card-001",
  "description": "A fierce dragon that breathes scorching flames.",
  "aspects":     ["fire", "dragon", "attack", "legendary"],
  "imageUrl":    "https://..."
}
```

| Field | Used for encoding? | How |
|-------|--------------------|-----|
| `cardId` | No — identifier only | Looked up after search to label results |
| `description` | Yes | Concatenated with aspects → fed into CLIP text encoder |
| `aspects` | Yes | Joined as space-separated words, appended to description |
| `imageUrl` | Yes (if reachable) | Image downloaded → fed into CLIP image encoder |

Before encoding, description and aspects are joined into a single string:

```
"A fierce dragon that breathes scorching flames. fire dragon attack legendary"
```

That one string goes into CLIP's text encoder and becomes a 512-number vector —
the card's semantic fingerprint.

---

## How the stored vector is built (offline, at encode time)

```
description + aspects  →  CLIP text encoder  →  512-dim text vector  (always)

imageUrl (if reachable) →  download image
                        →  CLIP image encoder →  512-dim image vector (optional)

                            ┌── text vector only (if no image)
                            │
                            └── average(text vector, image vector)  (if both)
                                        │
                                        ▼
                              normalize to length 1
                                        │
                                        ▼
                        stored as one row in card_embeddings.npy
```

If the image is missing or fails to download, only the text vector is used.
There is no penalty — text-only encoding works well on its own.

---

## How a text query works at search time

```
your input: "a creature with fire powers"
        │
        ▼
  CLIP text encoder   ← same encoder used when building card embeddings
        │
        ▼
  512-dim query vector (normalized)
        │
        ▼
  dot product against every row in card_embeddings.npy
  (dot product of two unit vectors = cosine similarity)
        │
        ▼
  one similarity score per card  (higher = more similar)
        │
        ▼
  sort descending → take top K → filter by threshold
        │
        ▼
  return cardId, description, aspects, imageUrl, score
```

---

## How an image query works at search time

```
your input: an image (local file or URL)
        │
        ▼
  CLIP image encoder  ← different encoder, but same 512-dim output space
        │
        ▼
  512-dim query vector (normalized)
        │
        ▼
  dot product against every row in card_embeddings.npy
        │   ↑ these rows may have been built from text only — that's fine
        ▼
  same ranking and filtering as text query
```

### Why cross-modal search works

CLIP was trained on hundreds of millions of (image, caption) pairs from the internet.
Its training objective was: *push matching image-text pairs close together in the
512-dim space; push non-matching pairs apart.*

After training, "a photo of a dragon" and the sentence "a fire-breathing dragon"
end up near each other in that space — not because you told it that, but because
it learned the association from data.

This means:
- A text query can find cards that were encoded from images
- An image query can find cards that were encoded from text descriptions
- Neither the query nor the card needs to use the same modality

---

## What "metadata" means — and how it relates to your schema

### In the current numpy setup

The word "metadata" doesn't formally exist. There are three separate pieces:

```
card_embeddings.npy   →  the vectors (numbers only, no labels)
                         shape: (N_cards, 512)

card_index.json       →  ["card-001", "card-002", ...]
                         maps row number in the matrix → cardId

cards.json            →  the full card objects
                         looked up after search to get description, aspects, imageUrl
```

The card fields are **not stored inside the vector** — they live in a separate file
and are joined at result-building time via `card_index.json`.

### In a vector database (e.g. Qdrant)

Each record in a vector DB has three parts stored together:

```
┌──────────────────────────────────────────────────────────┐
│  id:      "card-001"                                     │
│                                                          │
│  vector:  [0.021, -0.143, 0.087, ...]   (512 numbers)   │
│                                                          │
│  payload: {                             ← "metadata"     │
│    "description": "A fierce dragon...",                  │
│    "aspects": ["fire", "dragon", ...],                   │
│    "imageUrl": "https://..."                             │
│  }                                                       │
└──────────────────────────────────────────────────────────┘
```

The **payload** (also called metadata) is your card's own fields stored directly
alongside the vector inside the DB. It is **not** additional or different information —
it is the same schema you already have, just co-located with the vector so you
don't need a separate `cards.json` lookup.

### The extra power metadata gives you: filtered search

In the current numpy setup, filtering by aspect requires a manual Python step
after retrieving results. In a vector DB, filters run inside the search itself:

```python
# "top 3 fire cards most similar to this query — not just any top 3"
results = qdrant.search(
    collection_name="cards",
    query_vector=query_vec,
    query_filter={"aspects": {"$in": ["fire"]}},
    limit=3
)
```

This is one of the main practical reasons to migrate to a vector DB
when the dataset grows or filtering requirements become more complex.

---

## Summary

| Question | Answer |
|----------|--------|
| What gets encoded into the vector? | `description` + `aspects` (as text), `imageUrl` (as image if available) |
| What is NOT encoded? | `cardId` — it's a label, not semantic content |
| Text query path | Text → CLIP text encoder → cosine similarity against stored vectors |
| Image query path | Image → CLIP image encoder → cosine similarity against **same** stored vectors |
| Why cross-modal search works | CLIP places matching text and images near each other in the same 512-dim space by design |
| What is metadata? | Your card fields (description, aspects, imageUrl) stored alongside the vector — same schema, just co-located inside a vector DB record instead of a separate JSON file |
| Is metadata extra/different data? | No — it is your existing card fields, stored differently |
| What does metadata unlock? | Filtered search: "top-3 similar AND has aspect fire" — done inside the DB, not in Python |
