"""Helper utilities for the Streamlit UI."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

import requests

BASE_PATH = Path(__file__).resolve().parent.parent
_TRANSLATIONS: dict[str, dict[str, str]] | None = None


def get_config() -> Dict[str, Any]:
    default_model = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo-0125")
    models_env = os.getenv("MODELS")
    if models_env:
        models = [m.strip() for m in models_env.split(",") if m.strip()]
        if default_model not in models:
            models.insert(0, default_model)
    else:
        models = [default_model]
    return {
        "api_base": os.getenv("GP_API_BASE", "http://127.0.0.1:8000"),
        "default_model": default_model,
        "models": models,
    return {
        "api_base": os.getenv("GP_API_BASE", "http://127.0.0.1:8000"),
        "default_model": os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo-0125"),
        "max_tokens": int(os.getenv("MAX_TOKENS", "256")),
        "history_max_turns": int(os.getenv("HISTORY_MAX_TURNS", "10")),
    }


def trim_history(
    messages: List[Dict[str, Any]], limit_turns: int
) -> List[Dict[str, Any]]:
    return messages[-limit_turns * 2 :]


def shape_payload(
    messages: List[Dict[str, Any]], model: str, max_tokens: int
) -> Dict[str, Any]:
    return {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
    }


def load_translations() -> Dict[str, Dict[str, str]]:
    global _TRANSLATIONS
    if _TRANSLATIONS is None:
        _TRANSLATIONS = {}
        for lang in ("en", "pl"):
            path = BASE_PATH / "i18n" / f"{lang}.json"
            with path.open(encoding="utf-8") as f:
                _TRANSLATIONS[lang] = json.load(f)
    return _TRANSLATIONS


def t(key: str, lang: str) -> str:
    translations = load_translations()
    return translations.get(lang, {}).get(key, translations["en"].get(key, key))


def send_chat(
    messages: List[Dict[str, Any]],
    model: str,
    max_tokens: int,
    api_base: str,
    streaming: bool = False,
) -> Dict[str, Any]:
    payload = shape_payload(messages, model, max_tokens)
    resp = requests.post(f"{api_base}/proxy", json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
