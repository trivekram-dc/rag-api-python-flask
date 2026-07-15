import pytest

@pytest.fixture
def sample_context_chunks():
    return [
        {
            "id": "chunk-sub-101-a",
            "text": (
                "Customers may upgrade from a lower plan to a higher plan at any time. "
                "The upgrade becomes active immediately."
            ),
            "source_id": "SUB-101",
            "title": "Subscription Plan Changes",
            "category": "Billing",
            "section": "Upgrades",
            "distance": 0.12,
        },
        {
            "id": "chunk-inv-205-a",
            "text": (
                "Support representatives may resend invoice copies to verified billing contacts."
            ),
            "source_id": "INV-205",
            "title": "Invoice Support",
            "category": "Billing",
            "section": "Invoice Copies",
            "distance": 0.33,
        },
    ]

@pytest.fixture
def chroma_query_results():
    return {
        "ids": [["chunk-sub-101-a", "chunk-inv-205-a"]],
        "documents": [
            [
                "Customers may upgrade from a lower plan to a higher plan at any time.",
                "Support representatives may resend invoice copies to verified billing contacts.",
            ]
        ],
        "metadatas": [
            [
                {
                    "source_id": "SUB-101",
                    "title": "Subscription Plan Changes",
                    "category": "Billing",
                    "section": "Upgrades",
                },
                {
                    "source_id": "INV-205",
                    "title": "Invoice Support",
                    "category": "Billing",
                    "section": "Invoice Copies",
                },
            ]
        ],
        "distances": [[0.12, 0.33]],
    }