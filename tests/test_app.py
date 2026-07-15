import app as app_module
from lib.model_client import ModelClientError


def make_client():
    flask_app = app_module.create_app()
    flask_app.config["TESTING"] = True
    return flask_app.test_client()


def test_api_ask_returns_service_response_and_passes_trimmed_question(monkeypatch):
    received = {}

    def fake_answer_question(question):
        received["question"] = question
        return {
            "answer": "Customers may upgrade immediately.",
            "sources": [
                {
                    "id": "SUB-101",
                    "title": "Subscription Plan Changes",
                    "category": "Billing",
                    "section": "Upgrades",
                    "chunk_id": "chunk-sub-101-a",
                }
            ],
        }

    monkeypatch.setattr(app_module, "answer_question", fake_answer_question)

    client = make_client()
    response = client.post(
        "/api/ask",
        json={"question": "  Can I upgrade a customer today?  "},
    )

    assert response.status_code == 200
    assert received["question"] == "Can I upgrade a customer today?"

    data = response.get_json()
    assert data["answer"] == "Customers may upgrade immediately."
    assert data["sources"][0]["id"] == "SUB-101"


def test_api_ask_rejects_invalid_input_without_calling_service(monkeypatch):
    called = {"value": False}

    def fake_answer_question(question):
        called["value"] = True

    monkeypatch.setattr(app_module, "answer_question", fake_answer_question)

    client = make_client()
    response = client.post("/api/ask", json={"question": "   "})

    assert response.status_code == 400
    assert called["value"] is False

    data = response.get_json()
    assert data["error"] == "empty_question"
    assert "message" in data


def test_api_ask_returns_502_for_model_service_error(monkeypatch):
    def fake_answer_question(question):
        raise ModelClientError("Ollama unavailable")

    monkeypatch.setattr(app_module, "answer_question", fake_answer_question)

    client = make_client()
    response = client.post(
        "/api/ask",
        json={"question": "Can I upgrade a customer today?"},
    )

    assert response.status_code == 502

    data = response.get_json()
    assert data["error"] == "model_service_error"
    assert "Ollama unavailable" in data["message"]