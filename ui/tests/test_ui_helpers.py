import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import helpers


def test_trim_history():
    messages = [
        {"role": "user", "content": "1"},
        {"role": "assistant", "content": "a"},
        {"role": "user", "content": "2"},
        {"role": "assistant", "content": "b"},
    ]
    assert helpers.trim_history(messages, 1) == [
        {"role": "user", "content": "2"},
        {"role": "assistant", "content": "b"},
    ]


def test_shape_payload():
    messages = [
        {"role": "user", "content": "hi", "ts": "1", "id": "a"},
        {"role": "assistant", "content": "hello", "ts": "2", "id": "b"},
    ]
    payload = helpers.shape_payload(messages, "gpt", 256)
    assert payload == {
        "model": "gpt",
        "max_tokens": 256,
        "messages": [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
        ],
    }


def test_i18n_lookup():
    assert helpers.t("send", "pl") == "Wyślij"


def test_i18n_fallback(monkeypatch):
    translations = {"en": {"greet": "Hello"}, "pl": {}}
    monkeypatch.setattr(helpers, "_TRANSLATIONS", translations)
    assert helpers.t("greet", "pl") == "Hello"


def test_get_config_models(monkeypatch):
    monkeypatch.setenv("DEFAULT_MODEL", "m1")
    monkeypatch.setenv("MODELS", "m1,m2")
    cfg = helpers.get_config()
    assert cfg["models"] == ["m1", "m2"]
    assert cfg["default_model"] == "m1"
