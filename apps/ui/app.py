"""Streamlit chat UI for GuardPilot."""

from __future__ import annotations

import os
import time
import uuid

import streamlit as st

from .components import bubble, empty_state, input_bar, sidebar, top_bar
from .helpers import healthcheck, post_proxy, shape_payload, trim_history
from .i18n import t
from .state import init
from .theme import inject

API_BASE = os.getenv("GP_API_BASE", "http://127.0.0.1:8000")


def send_message(content: str) -> None:
    """Send *content* to backend and append reply."""
    if len(content) > 8000:
        st.session_state.error = t("message_too_long", st.session_state.lang)
        return
    msg = {
        "id": str(uuid.uuid4()),
        "role": "user",
        "content": content,
        "ts": time.strftime("%H:%M"),
    }
    st.session_state.messages.append(msg)
    history = trim_history(
        st.session_state.messages, st.session_state.history_max_turns
    )
    payload = shape_payload(
        history, st.session_state.model, st.session_state.max_tokens
    )
    resp = post_proxy(API_BASE, payload)
    if "error" in resp:
        code = resp["error"]["code"]
        key = {
            429: "error.rate_limited",
            413: "error.too_large",
            422: "error.validation",
            "network": "error.network",
        }.get(code, "error.unavailable")
        st.session_state.error = t(key, st.session_state.lang)
    else:
        reply = resp.get("reply", "")
        usage = resp.get("usage")
        st.session_state.messages.append(
            {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": reply,
                "ts": time.strftime("%H:%M"),
                "usage": usage,
            }
        )


def main() -> None:
    init()
    inject()
    st.session_state.health = healthcheck(API_BASE)
    top_bar(st.session_state.health, st.session_state.lang)
    sidebar(st.session_state.lang)
    st.markdown("<div class='timeline'>", unsafe_allow_html=True)
    if not st.session_state.messages:
        empty_state(st.session_state.lang, send_message)
    else:
        for msg in st.session_state.messages:
            st.markdown(bubble(msg, st.session_state.lang), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    input_bar(send_message, st.session_state.lang)
    if st.session_state.error:
        st.warning(st.session_state.error)
        st.session_state.error = None


if __name__ == "__main__":
    main()
