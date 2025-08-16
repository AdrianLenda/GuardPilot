"""Minimal CSS theming for the chat UI."""

from __future__ import annotations

import streamlit as st

# Global stylesheet for the chat UI.
THEME_CSS = """
CSS = """
<style>
:root {
  --gp-bg: var(--background-color, #ffffff);
  --gp-card: #f3f4f6;
  --gp-text: #111827;
  --gp-muted: #6b7280;
  --gp-primary: #3B82F6;
  --gp-border: #e5e7eb;
}

.bubble {
  padding: 10px 14px;
  border-radius: 16px;
  margin-bottom: 8px;
  max-width: 70ch;
}

.bubble.user {
  background: var(--gp-primary);
  color: #fff;
  margin-left: auto;
}

.bubble.assistant {
  background: var(--gp-card);
  color: var(--gp-text);
  margin-right: auto;
}

.top-bar, .input-bar {
  position: sticky;
  z-index: 100;
  background: var(--gp-bg);
}
.top-bar {
  top: 0;
  box-shadow: 0 2px 4px rgba(0,0,0,.05);
  padding: 0.5rem 1rem;
}
.input-bar {
  bottom: 0;
  box-shadow: 0 -2px 4px rgba(0,0,0,.05);
  padding: 0.5rem 1rem;
}

.timeline {
  height: calc(100vh - 8rem);
  overflow-y: auto;
}
</style>
"""


def apply_theme() -> None:
    """Inject custom CSS into the app."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)
def inject() -> None:
    """Inject custom CSS into the app."""
    st.markdown(CSS, unsafe_allow_html=True)
