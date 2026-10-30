# Card Similarity Search — Feature Requirements

## Overview

Given a collection of cards, build a system that accepts an input (image or text description) and returns the **top 3 most similar cards** from the dataset. If no meaningful match exists, the system should gracefully return zero or fewer results rather than forcing poor matches.

---

## Dataset Schema

Each card entity has the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `cardId` | string | Unique identifier |
| `description` | string | Human-readable card description |
| `aspects` | list[string] | Tags or facets that characterize the card (e.g. `["fire", "attack", "rare"]`) |
| `imageUrl` | string | URL to the card's image |

---

## Inputs

The system must accept either of the following as a query:

1. **Text** — a free-form description or partial description of a card
2. **Image** — a photo or scan of a card (or a similar image)

Queries are cross-modal: a text query can match against image-encoded cards, and vice versa.

---

## Output

- Returns **top 3 most similar cards** from the dataset, ranked by similarity score
- Each result includes: `cardId`, `description`, `imageUrl`, and the similarity `score` (0–1)
- If no card clears a minimum similarity threshold, the system may return fewer than 3 results (including zero)

---

## Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-01 | Accept a text string as query input |
| FR-02 | Accept an image (URL or local file) as query input |
| FR-03 | Return ranked results with similarity scores |
| FR-04 | Support a configurable similarity threshold to filter weak matches |
| FR-05 | Encoding of the card dataset must be done offline (not at query time) |
| FR-06 | Encoded vectors must be persisted and reusable across queries |

---

## Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-01 | Query response time < 500ms for datasets up to 10,000 cards |
| NFR-02 | No GPU required for inference (CPU-compatible) |
| NFR-03 | System must work offline after initial model download |

---

## Constraints & Assumptions

- Dataset size is assumed to be small-to-medium (< 10k cards) initially
- CLIP (`openai/clip-vit-base-patch32`) is the chosen pretrained backbone
- No fine-tuning in v1 — evaluate zero-shot CLIP quality first
- Python 3.9+ environment
