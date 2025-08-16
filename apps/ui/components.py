"""UI components for the Streamlit chat interface."""

from __future__ import annotations

from html import escape
from typing import Callable, Dict

import streamlit as st

from .i18n import t


def top_bar(status: str, lang: str) -> str:
    """Render top bar with health chip."""
    health_text = t(f"status.{status}", lang)
    st.markdown(
        f"<div class='top-bar'><strong>{t('app.title', lang)}</strong> "
        f"<span class='health'>{health_text}</span></div>",
        unsafe_allow_html=True,
    )
    return health_text


def sidebar(lang: str) -> None:
    """Render left sidebar with controls."""
    with st.sidebar:
        st.selectbox(t("sidebar.model", lang), [st.session_state.model], key="model")
        st.slider(t("sidebar.max_tokens", lang), 32, 2048, key="max_tokens")
        st.selectbox(t("sidebar.language", lang), ["en", "pl"], key="lang")
        st.slider(t("sidebar.history", lang), 1, 32, key="history_max_turns")
        st.button(
            t("sidebar.new_chat", lang),
            on_click=lambda: st.session_state.messages.clear(),
        )
        st.button(
            t("sidebar.clear_chat", lang),
            on_click=lambda: st.session_state.messages.clear(),
        )
        st.caption(t("sidebar.help", lang))


def bubble(msg: Dict[str, str], lang: str) -> str:
    """Return HTML for a single chat bubble."""
    content = escape(msg.get("content", ""))
    ts = msg.get("ts", "")
    usage = msg.get("usage")
    usage_html = f" <span class='usage'>{usage}</span>" if usage else ""
    return (
        f"<div class='bubble {msg['role']}'><div class='content'>{content}</div>"
        f"<div class='meta'>{ts}{usage_html}</div></div>"
    )


def empty_state(lang: str, on_example: Callable[[str], None]) -> None:
    """Render empty state with example prompts."""
    examples = [
        t("empty.prompt1", lang),
        t("empty.prompt2", lang),
        t("empty.prompt3", lang),
    ]
    for ex in examples:
        if st.button(ex):
            on_example(ex)


def input_bar(on_send: Callable[[str], None], lang: str) -> None:
    """Render sticky input bar."""
    with st.form("chat-input", clear_on_submit=True):
        txt = st.text_area(t("input.placeholder", lang), key="chat_input")
        submitted = st.form_submit_button(
            t("input.send", lang), disabled=st.session_state.sending
        )
    if submitted and txt.strip():
        on_send(txt.strip())
