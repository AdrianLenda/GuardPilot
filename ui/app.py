import requests
import streamlit as st

st.title("GuardPilot Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None     


def send_message() -> None:
    user_input = st.session_state.user_input.strip()
    if not user_input:
        return
    st.session_state.messages.append({"role": "user", "content": user_input})
    payload = {
        "conversation_id": st.session_state.conversation_id,
        "messages": st.session_state.messages,
    }
    try:
        response = requests.post("/proxy", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        st.session_state.conversation_id = data.get("conversation_id")
        st.session_state.messages.append(
            {"role": "assistant", "content": data.get("reply", "")}
        )
    except Exception as exc:
        st.session_state.messages.append(
            {"role": "assistant", "content": f"Error: {exc}"}
        )
    st.session_state.user_input = ""
    st.experimental_rerun()


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.text_input("Message", key="user_input")
st.button("Send", on_click=send_message)

