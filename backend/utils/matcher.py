from typing import List


def find_best_match(query: str, candidates: List[str]) -> str:
    """Return the best matching candidate for the query."""
    return candidates[0] if candidates else ""
