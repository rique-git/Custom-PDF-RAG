import json
from pathlib import Path

from ..config import PARENT_STORE_PATH
from ..vectorstore.qdrant_client import get_vector_store


def retrieve(query: str, k: int = 6):

    vector_store = get_vector_store()
    child_hits = vector_store.similarity_search(query, k=k)

    parent_ids = {doc.metadata["parent_id"] for doc in child_hits}

    parents = []

    for pid in parent_ids:
        path = PARENT_STORE_PATH / f"{pid}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                parents.append(json.load(f))

    return parents
