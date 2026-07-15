def format_context_chunk(chunk):
    """Format one retrieved chunk for the prompt context block."""
    source_id = chunk.get("source_id") or chunk.get("id") or "unknown-source"
    title = chunk.get("title") or "Untitled Source"
    category = chunk.get("category") or "Uncategorized"
    section = chunk.get("section") or "General"
    text = str(chunk.get("text") or "").strip()

    return f"[{source_id} | {title} | {category} | {section}]\n{text}"


def build_rag_prompt(question, context_chunks):
    """Build a structured RAG prompt from a question and retrieved context."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must be a non-empty string.")

    usable_chunks = [
        chunk
        for chunk in list(context_chunks or [])
        if str(chunk.get("text") or "").strip()
    ]

    if not usable_chunks:
        raise ValueError("At least one context chunk with text is required.")

    context_block = "\n\n".join(format_context_chunk(chunk) for chunk in usable_chunks)

    return f"""Instructions:
You are a customer success knowledge assistant for an internal support team.
Use only the approved context provided below to answer the question.
Do not invent policies, numbers, approvals, refunds, credits, or process steps that are not supported by the approved context.
If the approved context is incomplete, say what still needs to be confirmed.

Context:
{context_block}

Question:
{question.strip()}

Response Requirements:
- Answer in 2 to 5 concise sentences.
- Include only information supported by the approved context.
- Mention missing information when the context does not fully answer the question.
- Refer to supporting source IDs when helpful.
"""