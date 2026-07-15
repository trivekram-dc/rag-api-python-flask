from data.knowledge_base import DOCUMENTS
from lib.retrieval import CHROMA_PATH, COLLECTION_NAME


def seed_chroma():
    import chromadb

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(COLLECTION_NAME)

    collection.add(
        ids=[doc["chunk_id"] for doc in DOCUMENTS],
        documents=[doc["text"] for doc in DOCUMENTS],
        metadatas=[
            {
                "source_id": doc["source_id"],
                "title": doc["title"],
                "category": doc["category"],
                "section": doc["section"],
            }
            for doc in DOCUMENTS
        ],
    )

    print(f"Seeded {len(DOCUMENTS)} chunks into Chroma collection '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    seed_chroma()