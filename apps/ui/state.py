"""Session state initialisation and helpers."""

from __future__ import annotations

import os

import streamlit as st


def _clamp(val: int, low: int, high: int) -> int:
    return max(low, min(high, val))


def init() -> None:
    """Seed default values in ``st.session_state``."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "lang" not in st.session_state:
        st.session_state.lang = "en"
    if "model" not in st.session_state:
        st.session_state.model = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo-0125")
    if "max_tokens" not in st.session_state:
        v = int(os.getenv("MAX_TOKENS", "256"))
        st.session_state.max_tokens = _clamp(v, 32, 2048)
    if "history_max_turns" not in st.session_state:
        v = int(os.getenv("HISTORY_MAX_TURNS", "10"))
        st.session_state.history_max_turns = _clamp(v, 1, 32)
    st.session_state.setdefault("sending", False)
    st.session_state.setdefault("error", None)
    st.session_state.setdefault("health", "unknown")
