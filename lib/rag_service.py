from lib.model_client import ModelClientError, generate_answer
from lib.prompt_builder import build_rag_prompt
from lib.response_formatter import (
    format_fallback_response,
    format_sources,
    format_success_response,
)
from lib.retrieval import DEFAULT_TOP_K, retrieve_context


def answer_question(
    question,
    retriever=None,
    prompt_builder=None,
    model_client=None,
    top_k=DEFAULT_TOP_K,
):
    """Run the full RAG workflow for a validated question."""
    active_retriever = retriever or retrieve_context
    active_prompt_builder = prompt_builder or build_rag_prompt
    active_model_client = model_client or generate_answer

    context_chunks = active_retriever(question, top_k=top_k)

    if not context_chunks:
        return format_fallback_response(question)

    prompt = active_prompt_builder(question, context_chunks)
    answer = active_model_client(prompt)

    if not isinstance(answer, str) or not answer.strip():
        raise ModelClientError("Model service did not return a usable response.")

    sources = format_sources(context_chunks)
    return format_success_response(answer, sources)