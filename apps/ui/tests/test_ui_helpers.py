from __future__ import annotations

from ..helpers import shape_payload, trim_history
from ..i18n import t


def test_trim_history_pairs() -> None:
    msgs = [
        {"role": "user", "content": "u1", "ts": "t", "id": "1"},
        {"role": "assistant", "content": "a1", "ts": "t", "id": "2"},
        {"role": "user", "content": "u2", "ts": "t", "id": "3"},
        {"role": "assistant", "content": "a2", "ts": "t", "id": "4"},
    ]
    trimmed = trim_history(msgs, 1)
    assert trimmed == msgs[2:]


def test_shape_payload_validation() -> None:
    msgs = [{"role": "user", "content": "hi"}]
    payload = shape_payload(msgs, "gpt", 10)
    assert payload["messages"][0]["role"] == "user"
    import pytest

    with pytest.raises(ValueError):
        shape_payload([{"role": "bad", "content": "x"}], "gpt", 10)
    with pytest.raises(ValueError):
        shape_payload([{"role": "user", "content": "x" * 8001}], "gpt", 10)


def test_i18n_fallback_to_en() -> None:
    assert t("title", "xx") == t("title", "en")
