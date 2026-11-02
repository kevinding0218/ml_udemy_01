# How to Run the Card Similarity Search

## Step 1 — Start the API server

Open a terminal and run:

```bash
cd /Users/rading/Development/research/ml_udemy_01/projects/1_card-similarity-search
source .venv/bin/activate
python src/api.py
```

You should see:
```
Running on http://127.0.0.1:8005
```

Leave this terminal running. The API must stay up for searches to work.

## Step 2 — Open the web page

Open a **new terminal tab** (`Cmd+T`) and run:

```bash
open /Users/rading/Development/research/ml_udemy_01/projects/1_card-similarity-search/web/index.html
```

Or in Finder: navigate to `projects/1_card-similarity-search/web/` and double-click `index.html`.

The page opens in your browser from the filesystem (`file://...` in the address bar).

## Step 3 — Search

- **Text tab:** type a description like `"fire breathing creature"` and press Enter or click Search
- **Image tab:** paste an image URL and search — CLIP can match images against the card text embeddings directly

---

## Notes

- `localhost:8005` in the browser shows "Not Found" — that is normal. The API has no home page; it only responds to `/search/text` and `/search/image`. Open the HTML file instead.
- To verify the API is up, visit: `http://localhost:8005/health` — you should see `{"status": "ok"}`
- To stop the API: press `Ctrl+C` in the terminal running it
