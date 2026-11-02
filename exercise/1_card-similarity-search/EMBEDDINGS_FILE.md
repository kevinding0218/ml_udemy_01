# What is `card_embeddings.npy`?

## The short answer

It is a saved matrix of numbers — one row per card, 512 numbers per row.
Each row is the card's "meaning" compressed into a fixed-size vector by CLIP.
The file exists so that expensive neural network computation only runs once,
not on every query.

---

## What's inside

```
Shape: (12, 512)
       │    │
       │    └── 512 numbers per card (the embedding vector)
       └──────── 12 rows, one per card

Data type: float32   (32-bit decimal numbers, standard for neural network output)
```

Visualised as a table:

```
              num_1      num_2      num_3    ...  num_512
card-001  [ -0.01130,  -0.00915,  -0.02205, ...   0.04821 ]
card-002  [  0.03421,   0.01203,  -0.00871, ...   0.02910 ]
card-003  [ -0.00242,   0.02849,  -0.01644, ...   0.03812 ]
...
card-012  [  0.01823,  -0.04201,   0.00993, ...   0.01204 ]
```

The row order matches `embeddings/card_index.json`:

```json
["card-001", "card-002", "card-003", ..., "card-012"]
```

Row 0 = card-001, row 1 = card-002, and so on.
That index file is the bridge between a row number and a card ID.

---

## What those 512 numbers mean

They are **not human-readable**. No single number means "fire" or "dragon".
The meaning is encoded *across all 512 numbers together* as a position
in high-dimensional space.

Think of it like map coordinates. In 2D you need 2 numbers to place a pin on a map.
CLIP uses 512 numbers to place a card in "meaning space".

- Cards with **similar meaning** end up at **nearby coordinates**
- Cards with **different meaning** end up **far apart**

For example: the dragon card and the phoenix card both contain fire and attack —
their 512-number coordinates are close together. The healer card has completely
different meaning — its coordinates are far away from both.

When you search, you encode your query into the same 512-dim space and measure
distance to every card. The closest cards are your results.

---

## Every vector has length exactly 1.0

All vectors are **unit-normalized** before being saved — their length (magnitude)
is scaled to exactly 1.0. This is required for cosine similarity to work correctly.

```python
import numpy as np
matrix = np.load("embeddings/card_embeddings.npy")
np.linalg.norm(matrix[0])   # → 1.0
np.linalg.norm(matrix[5])   # → 1.0
```

Without normalization, a card with a longer raw vector would score higher simply
because of its magnitude, not because it is semantically closer. Normalization
removes that bias so only the angle (direction) between vectors matters.

---

## Why save it to a file at all?

Running CLIP to produce these numbers is slow — it involves a full neural network
forward pass over text and optionally an image. If you recomputed them on every
query, each search would re-process all 12 cards before even looking at your input.

Instead the workflow is split into two stages:

```
OFFLINE (encode_dataset.py — runs once)
────────────────────────────────────────────────────
CLIP processes all cards
        │
        ▼
(12, 512) matrix produced
        │
        ▼
saved → embeddings/card_embeddings.npy   ✓ done


ONLINE (search.py — runs on every query)
────────────────────────────────────────────────────
load card_embeddings.npy from disk  ← milliseconds, no model needed
        │
encode only the query               ← one CLIP forward pass (fast)
        │
compare query vector against matrix ← pure math, very fast
        │
return top K results
```

The file is a **cache of expensive computation**. That is its entire purpose.

---

## When to regenerate it

Re-run `encode_dataset.py` only when the content that gets encoded changes:

| Change to `cards.json` | Re-encode needed? |
|------------------------|-------------------|
| Edit `description` | Yes |
| Edit `aspects` | Yes |
| Change `imageUrl` | Yes |
| Add / remove a card entirely | Yes |
| Add `releaseDate`, `releaseId`, or any other metadata field | **No** |
| Change `cardId` | **No** — it's never encoded |

Metadata fields never touch the encoder, so the `.npy` file stays valid
no matter how many metadata fields you add or change.

---

## Why `.npy` format?

`.npy` is NumPy's native binary format for saving arrays to disk.

| Property | Detail |
|----------|--------|
| Speed | Loads in milliseconds — much faster than CSV or JSON |
| Lossless | No rounding of float values |
| Simple | One file, no database, no server |
| Dependency | Only NumPy required to read it |

For this POC it is the right choice. In production the same numbers would live
inside a vector database (e.g. Qdrant) instead, which adds indexed search,
metadata filtering, and upsert support — but the numbers themselves are identical.

---

## How to inspect it yourself

```python
import numpy as np
import json

matrix = np.load("embeddings/card_embeddings.npy")
with open("embeddings/card_index.json") as f:
    index = json.load(f)

print("Shape:", matrix.shape)           # (12, 512)
print("Card IDs:", index)               # ["card-001", ...]

# Look at one card's vector
card_row = index.index("card-004")
print("card-004 vector (first 8):", matrix[card_row][:8])
print("card-004 vector length:",    round(np.linalg.norm(matrix[card_row]), 6))  # 1.0
```
