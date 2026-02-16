from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from langchain_qdrant import QdrantVectorStore

from ..config import QDRANT_PATH, CHILD_COLLECTION
from .embeddings import get_dense_embeddings

import os

def get_client():
    host = os.getenv("QDRANT_HOST")
    port = os.getenv("QDRANT_PORT")
    path = os.getenv("QDRANT_PATH")

    if host and port:
        return QdrantClient(host=host, port=int(port))

    if path:
        return QdrantClient(path=path)

    return QdrantClient(host="localhost", port=6333)


def recreate_collection():
    client = get_client()
    embeddings = get_dense_embeddings()

    dim = len(embeddings.embed_query("test"))

    if client.collection_exists(CHILD_COLLECTION):
        client.delete_collection(CHILD_COLLECTION)

    client.create_collection(
        collection_name=CHILD_COLLECTION,
        vectors_config=qmodels.VectorParams(
            size=dim,
            distance=qmodels.Distance.COSINE,
        ),
    )

    client.close()


def get_vector_store():
    client = get_client()
    embeddings = get_dense_embeddings()

    return QdrantVectorStore(
        client=client,
        collection_name=CHILD_COLLECTION,
        embedding=embeddings,
    )
