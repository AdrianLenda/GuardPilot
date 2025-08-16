import html
import uuid
from datetime import datetime

import streamlit as st
from requests import HTTPError, Timeout

from helpers import get_config, send_chat, trim_history, t

cfg = get_config()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "lang" not in st.session_state:
    st.session_state.lang = "pl"
    st.session_state.lang = "en"

st.title(t("title", st.session_state.lang))


with st.sidebar:
    lang_choice = st.selectbox(
        t("language", st.session_state.lang),
        ["pl", "en"],
        index=["pl", "en"].index(st.session_state.lang),
    )
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.experimental_rerun()
    st.session_state.model = st.selectbox(
        t("model", st.session_state.lang),
        cfg["models"],
        index=cfg["models"].index(st.session_state.get("model", cfg["default_model"])),
    st.session_state.model = st.selectbox(
        t("model", st.session_state.lang), [cfg["default_model"]]
    )
    st.session_state.max_tokens = st.number_input(
        t("max_tokens", st.session_state.lang),
        min_value=1,
        max_value=4000,
        value=st.session_state.get("max_tokens", cfg["max_tokens"]),
        value=cfg["max_tokens"],
    )
    st.session_state.lang = st.selectbox(
        t("language", st.session_state.lang),
        ["en", "pl"],
        index=["en", "pl"].index(st.session_state.lang),
    )


def add_message(role: str, content: str) -> None:
    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
            "ts": datetime.utcnow().isoformat(),
            "id": str(uuid.uuid4()),
        }
    )


def send_message() -> None:
    content = st.session_state.user_input.strip()
    if not content:
        return
    if len(content) > 8000:
        st.error(t("message_too_long", st.session_state.lang))
        return
    add_message("user", content)
    history = trim_history(st.session_state.messages, cfg["history_max_turns"])
    try:
        data = send_chat(
            history,
            st.session_state.model,
            st.session_state.max_tokens,
            cfg["api_base"],
        )
    except Timeout:
        st.error(t("error_timeout", st.session_state.lang))
        return
    except HTTPError as exc:
        status = exc.response.status_code
        if status == 422:
            st.error(t("error_validation", st.session_state.lang))
        elif 400 <= status < 500:
            st.error(t("error_client", st.session_state.lang))
        else:
            st.error(t("error_server", st.session_state.lang))
        return
    add_message("assistant", data.get("reply", ""))
    st.session_state.user_input = ""


def clear_chat() -> None:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(html.escape(msg["content"]))

st.text_input(t("message", st.session_state.lang), key="user_input")
col1, col2 = st.columns(2)
col1.button(t("send", st.session_state.lang), on_click=send_message)
col2.button(t("clear_chat", st.session_state.lang), on_click=clear_chat)
