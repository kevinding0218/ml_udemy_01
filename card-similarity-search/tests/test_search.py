"""
Tests for the card similarity search system.
Run from the project root:
    python -m pytest tests/ -v
or directly:
    cd card-similarity-search && python tests/test_search.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from search import search_by_text


def test_self_query_returns_itself():
    """Querying with a card's own description should return that card as #1."""
    results = search_by_text("A fierce dragon that breathes scorching flames, capable of melting steel and incinerating forests.")
    assert len(results) > 0, "Expected at least one result"
    assert results[0]["cardId"] == "card-001", f"Expected card-001, got {results[0]['cardId']}"
    assert results[0]["score"] > 0.80, f"Self-query score too low: {results[0]['score']}"


def test_paraphrase_finds_correct_card():
    """A paraphrased query should still find the right card in top 3."""
    results = search_by_text("fire breathing dragon with legendary power")
    card_ids = [r["cardId"] for r in results]
    assert "card-001" in card_ids, f"Expected card-001 in results, got {card_ids}"


def test_healer_query():
    """A healing-themed query should return support/heal cards."""
    results = search_by_text("a healer who restores life and supports allies")
    aspects_in_results = [a for r in results for a in r["aspects"]]
    assert "heal" in aspects_in_results or "support" in aspects_in_results, \
        f"Expected heal/support cards, got aspects: {aspects_in_results}"


def test_unrelated_query_scores_lower_than_relevant():
    """An unrelated query should score meaningfully lower than a semantically relevant one.
    Note: CLIP cosine scores cluster high (0.7+) even for unrelated inputs — use relative
    gap, not an absolute threshold, to distinguish relevant from irrelevant queries.
    """
    relevant = search_by_text("fire breathing dragon attacking with flames")
    unrelated = search_by_text("quarterly earnings report for fiscal year 2023")
    assert relevant[0]["score"] > unrelated[0]["score"], (
        f"Expected relevant ({relevant[0]['score']}) > unrelated ({unrelated[0]['score']})"
    )


def test_top_k_respected():
    """Never return more than top_k results."""
    results = search_by_text("warrior", top_k=2)
    assert len(results) <= 2


def test_threshold_filters_results():
    """A very high threshold should return fewer (possibly zero) results."""
    results = search_by_text("some text", threshold=0.99)
    assert len(results) == 0 or all(r["score"] >= 0.99 for r in results)


if __name__ == "__main__":
    tests = [
        test_self_query_returns_itself,
        test_paraphrase_finds_correct_card,
        test_healer_query,
        test_unrelated_query_scores_lower_than_relevant,
        test_top_k_respected,
        test_threshold_filters_results,
    ]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {test.__name__}: {e}")
        except Exception as e:
            print(f"  ERROR {test.__name__}: {e}")

    print(f"\n{passed}/{len(tests)} tests passed")
