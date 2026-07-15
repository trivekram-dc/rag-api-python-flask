FALLBACK_MESSAGE = (
    "The approved customer success documents do not contain enough information "
    "to answer that question. Review the relevant policy or contact a supervisor "
    "before acting on this request."
)


def format_sources(context_chunks):
    """Return source metadata for retrieved context chunks."""
    sources = []
    seen = set()

    for chunk in context_chunks or []:
        chunk_id = str(chunk.get("id") or "")
        source_id = str(chunk.get("source_id") or chunk_id or "")

        if not source_id:
            continue

        unique_key = (source_id, chunk_id)

        if unique_key in seen:
            continue

        seen.add(unique_key)

        sources.append(
            {
                "id": source_id,
                "title": chunk.get("title") or "Untitled Source",
                "category": chunk.get("category") or "Uncategorized",
                "section": chunk.get("section") or "",
                "chunk_id": chunk_id,
            }
        )

    return sources


def format_success_response(answer, sources):
    """Return the successful RAG API response body."""
    return {
        "answer": str(answer).strip(),
        "sources": list(sources or []),
    }


def format_fallback_response(question=None):
    """Return a safe response when there is not enough approved context."""
    return {
        "answer": FALLBACK_MESSAGE,
        "sources": [],
    }


def format_error_response(error, message):
    """Return a standard error response body."""
    return {
        "error": error,
        "message": message,
    }