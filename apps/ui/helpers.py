"""Helper utilities for the Streamlit chat UI."""

from __future__ import annotations

from typing import Any, Dict, List

import requests

ALLOWED_ROLES = {"user", "assistant", "system"}


def trim_history(messages: List[Dict[str, Any]], turns: int) -> List[Dict[str, Any]]:
    """Return the last *turns* user/assistant pairs from *messages*."""
    if turns <= 0:
        return []
    count = 0
    idx = len(messages)
    while idx > 0 and count < turns:
        idx -= 1
        if messages[idx]["role"] == "user":
            count += 1
    return messages[idx:]


def shape_payload(
    messages: List[Dict[str, Any]], model: str, max_tokens: int
) -> Dict[str, Any]:
    """Validate and shape chat payload for backend /proxy."""
    for m in messages:
        role = m.get("role")
        if role not in ALLOWED_ROLES:
            raise ValueError(f"invalid role: {role}")
        content = m.get("content", "")
        if len(content) > 8000:
            raise ValueError("message too long")
    return {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
    }


def post_proxy(
    base_url: str, payload: Dict[str, Any], timeout: int = 30
) -> Dict[str, Any]:
    """POST *payload* to backend /proxy and return JSON or error dict."""
    url = base_url.rstrip("/") + "/proxy"
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
    except requests.RequestException as exc:  # network error
        return {"error": {"code": "network", "message": str(exc)}}
    if resp.status_code == 200:
        return resp.json()
    return {"error": {"code": resp.status_code, "message": resp.text}}


def healthcheck(base_url: str) -> str:
    """Check backend health endpoint."""
    url = base_url.rstrip("/") + "/health"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return "online"
    except requests.RequestException:
        pass
    return "offline"
