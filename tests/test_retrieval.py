from lib.retrieval import format_chroma_results, retrieve_context


def test_format_chroma_results_normalizes_nested_chroma_response(chroma_query_results):
    chunks = format_chroma_results(chroma_query_results)

    assert len(chunks) == 2

    first = chunks[0]
    assert first["id"] == "chunk-sub-101-a"
    assert first["source_id"] == "SUB-101"
    assert first["title"] == "Subscription Plan Changes"
    assert first["category"] == "Billing"
    assert first["section"] == "Upgrades"
    assert first["distance"] == 0.12
    assert "upgrade" in first["text"].lower()

    second = chunks[1]
    assert second["id"] == "chunk-inv-205-a"
    assert second["source_id"] == "INV-205"


def test_format_chroma_results_skips_blank_documents():
    results = {
        "ids": [["chunk-1", "chunk-2"]],
        "documents": [["Useful context", "   "]],
        "metadatas": [[{"source_id": "SRC-1"}, {"source_id": "SRC-2"}]],
        "distances": [[0.1, 0.2]],
    }

    chunks = format_chroma_results(results)

    assert len(chunks) == 1
    assert chunks[0]["id"] == "chunk-1"
    assert chunks[0]["text"] == "Useful context"


def test_retrieve_context_queries_collection_and_formats_results(chroma_query_results):
    class FakeCollection:
        def __init__(self):
            self.kwargs = None

        def query(self, **kwargs):
            self.kwargs = kwargs
            return chroma_query_results

    collection = FakeCollection()

    chunks = retrieve_context(
        "  How do subscription upgrades work?  ",
        collection=collection,
        top_k=2,
    )

    assert collection.kwargs["query_texts"] == ["How do subscription upgrades work?"]
    assert collection.kwargs["n_results"] == 2
    assert collection.kwargs["include"] == ["documents", "metadatas", "distances"]
    assert len(chunks) == 2
    assert chunks[0]["source_id"] == "SUB-101"


def test_retrieve_context_returns_empty_list_for_blank_question(chroma_query_results):
    class FakeCollection:
        def query(self, **kwargs):
            raise AssertionError("Blank questions should not query the collection.")

    assert retrieve_context("   ", collection=FakeCollection()) == []