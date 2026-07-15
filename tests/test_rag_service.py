import pytest

from lib.model_client import ModelClientError
from lib.rag_service import answer_question


def test_answer_question_runs_full_sequence_and_returns_answer_with_sources(
    sample_context_chunks,
):
    events = []

    def fake_retriever(question, top_k=3):
        events.append(("retriever", question, top_k))
        return sample_context_chunks

    def fake_prompt_builder(question, context_chunks):
        events.append(("prompt_builder", question, len(context_chunks)))
        return "PROMPT"

    def fake_model_client(prompt):
        events.append(("model_client", prompt))
        return "Customers may upgrade immediately when the plan change is approved."

    response = answer_question(
        "Can a customer upgrade now?",
        retriever=fake_retriever,
        prompt_builder=fake_prompt_builder,
        model_client=fake_model_client,
        top_k=2,
    )

    assert events == [
        ("retriever", "Can a customer upgrade now?", 2),
        ("prompt_builder", "Can a customer upgrade now?", 2),
        ("model_client", "PROMPT"),
    ]
    assert response["answer"] == (
        "Customers may upgrade immediately when the plan change is approved."
    )
    assert response["sources"][0]["id"] == "SUB-101"


def test_answer_question_returns_fallback_without_calling_prompt_or_model():
    def fake_retriever(question, top_k=3):
        return []

    def fake_prompt_builder(question, context_chunks):
        raise AssertionError("Prompt builder should not run when context is empty.")

    def fake_model_client(prompt):
        raise AssertionError("Model client should not run when context is empty.")

    response = answer_question(
        "Can I offer a refund?",
        retriever=fake_retriever,
        prompt_builder=fake_prompt_builder,
        model_client=fake_model_client,
    )

    assert response["sources"] == []
    assert "do not contain enough information" in response["answer"]


def test_answer_question_raises_model_client_error_for_blank_model_answer(
    sample_context_chunks,
):
    def fake_retriever(question, top_k=3):
        return sample_context_chunks

    def fake_prompt_builder(question, context_chunks):
        return "PROMPT"

    def fake_model_client(prompt):
        return "   "

    with pytest.raises(ModelClientError):
        answer_question(
            "Can a customer upgrade now?",
            retriever=fake_retriever,
            prompt_builder=fake_prompt_builder,
            model_client=fake_model_client,
        )