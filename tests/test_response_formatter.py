from lib.response_formatter import (
    format_fallback_response,
    format_sources,
    format_success_response,
)


def test_format_sources_returns_unique_metadata_without_full_context(sample_context_chunks):
    duplicate = sample_context_chunks[0].copy()
    chunks = sample_context_chunks + [duplicate]

    sources = format_sources(chunks)

    assert len(sources) == 2
    assert sources[0] == {
        "id": "SUB-101",
        "title": "Subscription Plan Changes",
        "category": "Billing",
        "section": "Upgrades",
        "chunk_id": "chunk-sub-101-a",
    }
    assert "text" not in sources[0]
    assert "distance" not in sources[0]


def test_format_success_response_returns_answer_and_sources(sample_context_chunks):
    sources = format_sources(sample_context_chunks)

    response = format_success_response("  Customers may upgrade immediately.  ", sources)

    assert response == {
        "answer": "Customers may upgrade immediately.",
        "sources": sources,
    }


def test_format_fallback_response_returns_safe_answer_and_empty_sources():
    response = format_fallback_response("Can I promise a refund?")

    assert response["sources"] == []
    assert "approved customer success documents" in response["answer"]
    assert "do not contain enough information" in response["answer"]