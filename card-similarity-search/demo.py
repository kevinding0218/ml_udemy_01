"""
demo.py — Command-line interface for testing the card similarity search system.

This file is the entry point for manual testing. It accepts a query (text or image),
calls the appropriate search function, and prints the results in a readable format.

Usage:
    # Text query
    python demo.py --text "a fire breathing creature"

    # Image query (URL)
    python demo.py --image "https://example.com/card.jpg"

    # Image query (local file)
    python demo.py --image "./my_card.png"

    # Adjust number of results and threshold
    python demo.py --text "healer" --top-k 5 --threshold 0.15
"""

import sys
import argparse
from pathlib import Path

# Add src/ to the import path so we can import search.py without installing the package.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from search import search_by_text, search_by_image


def print_results(results: list[dict]):
    """Pretty-print the list of result dicts returned by search_by_text / search_by_image.

    The score (0–1) reflects cosine similarity in CLIP's embedding space.
    Higher = more similar. Note that all CLIP scores tend to cluster in the 0.70–0.85
    range, so small differences in score (e.g. 0.82 vs 0.78) can still be meaningful.
    """
    if not results:
        print("No matches found above the similarity threshold.")
        return
    print(f"\nTop {len(results)} match(es):\n")
    for i, r in enumerate(results, 1):
        print(f"  #{i}  [{r['score']:.4f}]  {r['cardId']}")
        print(f"       {r['description']}")
        print(f"       Aspects: {', '.join(r['aspects'])}")
        if r["imageUrl"]:
            print(f"       Image:   {r['imageUrl']}")
        print()


def main():
    """Parse CLI arguments and run the search.

    argparse handles validation: --text and --image are mutually exclusive,
    and at least one is required. The parser prints usage help if you run
    `python demo.py --help`.
    """
    parser = argparse.ArgumentParser(description="Card Similarity Search Demo")
    # add_mutually_exclusive_group enforces that exactly one of --text or --image is given.
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text query")
    group.add_argument("--image", type=str, help="Image path or URL")
    parser.add_argument("--top-k", type=int, default=3, help="Number of results (default 3)")
    parser.add_argument("--threshold", type=float, default=0.20,
                        help="Minimum similarity score to include a result (default 0.20)")
    args = parser.parse_args()

    if args.text:
        print(f'Query (text): "{args.text}"')
        results = search_by_text(args.text, top_k=args.top_k, threshold=args.threshold)
    else:
        print(f'Query (image): "{args.image}"')
        results = search_by_image(args.image, top_k=args.top_k, threshold=args.threshold)

    print_results(results)


if __name__ == "__main__":
    main()
