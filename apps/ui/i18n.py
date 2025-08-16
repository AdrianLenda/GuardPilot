"""Simple i18n helper for the Streamlit UI."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_BASE = Path(__file__).resolve().parents[2] / "i18n"


@lru_cache(maxsize=None)
def _load(lang: str) -> dict[str, Any]:
    with (_BASE / f"{lang}.json").open(encoding="utf-8") as f:
        return json.load(f)


def t(key: str, lang: str, **kw: Any) -> str:
    """Translate *key* for *lang* with optional format arguments."""
    try:
        text = _load(lang).get(key)
    except FileNotFoundError:
        text = None
    if text is None:
        text = _load("en").get(key, key)
    return text.format(**kw)
