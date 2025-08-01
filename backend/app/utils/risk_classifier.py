"""
Risk classification utilities. Classify a conversation based on Annex III keywords loaded from YAML.
"""

from pathlib import Path
from typing import Tuple, List, Dict
import os

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

_KEYWORDS_CACHE: Dict[str, List[str]] | None = None


def _load_keywords() -> Dict[str, List[str]]:
    """
    Load risk keywords from a YAML file specified by the RISK_KEYWORDS_FILE environment variable.
    The YAML should map categories to a list of keywords.
    """
    global _KEYWORDS_CACHE
    if _KEYWORDS_CACHE is not None:
        return _KEYWORDS_CACHE

        default_path = Path(__file__).resolve().parent / "config" / "risk_keywords.yaml"
    keywords_file = os.getenv("RISK_KEYWORDS_FILE", str(default_path))
    data: Dict[str, List[str]] = {}
    if yaml is not None and os.path.exists(keywords_file):
        with open(keywords_file, "r", encoding="utf-8") as f:
            loaded = yaml.safe_load(f) or {}
            # Ensure all values are lists of lowercase strings
            for category, words in loaded.items():
                if isinstance(words, list):
                    data[category] = [str(w).lower() for w in words]
    _KEYWORDS_CACHE = data
    return data


def classify_text(text: str) -> Tuple[str, List[str]]:
    """
    Classify the given text into a risk level based on Annex III keywords.
    Returns a tuple (risk_level, tags). If any keyword is found, risk level is 'high-risk'.
    Otherwise 'limited-risk'. Tags are the categories whose keywords matched.
    """
    text_lower = text.lower()
    keywords = _load_keywords()
    matched_categories: List[str] = []
    for category, words in keywords.items():
        for word in words:
            if word in text_lower:
                matched_categories.append(category)
                break
    risk = "high-risk" if matched_categories else "limited-risk"
    return risk, matched_categories


def classify_risk(text: str) -> Tuple[str, List[str]]:
    """
    Alias for classify_text to maintain backward compatibility.
    """
    return classify_text(text)

