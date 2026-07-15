import pytest

from lib.prompt_builder import build_rag_prompt, format_context_chunk


def test_format_context_chunk_includes_metadata_and_text(sample_context_chunks):
    formatted = format_context_chunk(sample_context_chunks[0])

    assert "SUB-101" in formatted
    assert "Subscription Plan Changes" in formatted
    assert "Billing" in formatted
    assert "Upgrades" in formatted
    assert "Customers may upgrade" in formatted


def test_build_rag_prompt_includes_required_sections_context_and_question(sample_context_chunks):
    prompt = build_rag_prompt(
        "Can I upgrade a customer today?",
        sample_context_chunks,
    )

    for section in [
        "Instructions:",
        "Context:",
        "Question:",
        "Response Requirements:",
    ]:
        assert section in prompt

    assert "Can I upgrade a customer today?" in prompt
    assert "SUB-101" in prompt
    assert "INV-205" in prompt
    assert "Customers may upgrade" in prompt
    assert "Use only" in prompt
    assert "approved context" in prompt
    assert "do not invent" in prompt.lower()
    assert "source" in prompt.lower()


def test_build_rag_prompt_rejects_blank_question(sample_context_chunks):
    with pytest.raises(ValueError):
        build_rag_prompt("   ", sample_context_chunks)


def test_build_rag_prompt_rejects_empty_context():
    with pytest.raises(ValueError):
        build_rag_prompt("Can I upgrade a customer?", [])