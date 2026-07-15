import pytest
import requests

import lib.model_client as model_client
from lib.model_client import ModelClientError, generate_answer


def test_generate_answer_posts_to_ollama_and_returns_response(monkeypatch):
    calls = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"response": "  Use the approved upgrade process.  "}

    def fake_post(url, json, timeout):
        calls["url"] = url
        calls["json"] = json
        calls["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(model_client.requests, "post", fake_post)

    answer = generate_answer(
        "Prompt text",
        model_name="llama3.2",
        base_url="http://ollama.test",
    )

    assert answer == "Use the approved upgrade process."
    assert calls["url"] == "http://ollama.test/api/generate"
    assert calls["json"] == {
        "model": "llama3.2",
        "prompt": "Prompt text",
        "stream": False,
    }
    assert calls["timeout"] == 60


def test_generate_answer_raises_model_client_error_for_request_failure(monkeypatch):
    def fake_post(url, json, timeout):
        raise requests.RequestException("network unavailable")

    monkeypatch.setattr(model_client.requests, "post", fake_post)

    with pytest.raises(ModelClientError):
        generate_answer("Prompt text")


def test_generate_answer_raises_model_client_error_for_missing_response(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"message": "no response field"}

    def fake_post(url, json, timeout):
        return FakeResponse()

    monkeypatch.setattr(model_client.requests, "post", fake_post)

    with pytest.raises(ModelClientError):
        generate_answer("Prompt text")


def test_generate_answer_rejects_blank_prompt():
    with pytest.raises(ModelClientError):
        generate_answer("   ")