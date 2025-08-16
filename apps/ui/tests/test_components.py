from __future__ import annotations

from ..components import bubble, top_bar


def test_bubble_html_contains_content_timestamp_and_usage() -> None:
    msg = {
        "role": "assistant",
        "content": "hello",
        "ts": "12:00",
        "usage": "1 tok",
    }
    html = bubble(msg, "en")
    assert "hello" in html and "12:00" in html and "1 tok" in html


def test_top_bar_returns_health_text() -> None:
    text = top_bar("online", "en")
    assert "Online" in text
