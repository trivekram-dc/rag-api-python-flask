CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "customer_success_knowledge"
DEFAULT_TOP_K = 3


def get_chroma_collection(path=CHROMA_PATH, collection_name=COLLECTION_NAME):
    """Return a persistent Chroma collection for manual local testing."""
    import chromadb

    client = chromadb.PersistentClient(path=path)
    return client.get_or_create_collection(collection_name)


def _first_batch(value):
    if not value:
        return []

    first = value[0]
    if isinstance(first, list):
        return first

    return value


def format_chroma_results(results):
    """Normalize Chroma query results into context chunk dictionaries."""
    if not isinstance(results, dict):
        return []

    ids = _first_batch(results.get("ids", []))
    documents = _first_batch(results.get("documents", []))
    metadatas = _first_batch(results.get("metadatas", []))
    distances = _first_batch(results.get("distances", []))

    chunks = []

    for index, document in enumerate(documents):
        if document is None:
            continue

        text = str(document).strip()
        if not text:
            continue

        metadata = {}
        if index < len(metadatas) and isinstance(metadatas[index], dict):
            metadata = metadatas[index]

        chunk_id = ""
        if index < len(ids) and ids[index] is not None:
            chunk_id = str(ids[index])

        distance = None
        if index < len(distances):
            distance = distances[index]

        source_id = metadata.get("source_id") or chunk_id or "unknown-source"

        chunks.append(
            {
                "id": chunk_id,
                "text": text,
                "source_id": source_id,
                "title": metadata.get("title", "Untitled Source"),
                "category": metadata.get("category", "Uncategorized"),
                "section": metadata.get("section", ""),
                "distance": distance,
            }
        )

    return chunks


def retrieve_context(question, collection=None, top_k=DEFAULT_TOP_K):
    """Retrieve context chunks for a user question.

    Tests may pass a fake collection. Manual use should call Chroma.
    """
    if not isinstance(question, str):
        return []

    cleaned_question = question.strip()
    if not cleaned_question:
        return []

    active_collection = collection or get_chroma_collection()

    results = active_collection.query(
        query_texts=[cleaned_question],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    return format_chroma_results(results)