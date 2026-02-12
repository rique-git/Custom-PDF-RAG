from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from langchain_qdrant import QdrantVectorStore

from ..config import QDRANT_PATH, CHILD_COLLECTION
from .embeddings import get_dense_embeddings


def get_client():
    return QdrantClient(path=str(QDRANT_PATH))


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
