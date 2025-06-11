from typing import Dict, List, Tuple
from difflib import SequenceMatcher


def find_best_match(query: str, candidates: List[str]) -> str:
    """Return the best matching candidate for the query."""
    return candidates[0] if candidates else ""


def _similarity(a: str, b: str) -> float:
    """Return a simple similarity ratio between two strings."""

    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def choose_best_match_across_platforms(
    query: str, platform_results: Dict[str, List[str]]
) -> Tuple[str, str]:
    """Return the platform and candidate with the highest similarity score.

    Parameters
    ----------
    query:
        The search string used to find candidates.
    platform_results:
        Mapping of platform name to a list of candidate titles.

    Returns
    -------
    Tuple[str, str]
        ``(platform, title)`` pair of the best match. Empty strings if no
        candidates were provided.
    """

    best_platform = ""
    best_title = ""
    best_score = 0.0

    for platform, titles in platform_results.items():
        for title in titles:
            score = _similarity(query, title)
            if score > best_score:
                best_score = score
                best_platform = platform
                best_title = title

    return best_platform, best_title
