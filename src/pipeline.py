from .config import (
    PDFS_DIR,
    MARKDOWN_DIR,
    PARENT_STORE_PATH,
    CHILD_COLLECTION,
)
from .ingestion.pdf_ingestion import convert_all_pdfs
from .vectorstore.indexing import index_documents
from .vectorstore.qdrant_client import get_client


# --------------------------------------------------
# Readiness checks
# --------------------------------------------------

def pdfs_exist() -> bool:
    return any(PDFS_DIR.glob("*.pdf"))


def markdowns_exist() -> bool:
    return any(MARKDOWN_DIR.glob("*.md"))


def parents_exist() -> bool:
    return any(PARENT_STORE_PATH.glob("*.json"))


def collection_exists() -> bool:
    client = get_client()
    try:
        return client.collection_exists(CHILD_COLLECTION)
    finally:
        client.close()


def system_ready() -> bool:
    return (
        pdfs_exist()
        and markdowns_exist()
        and parents_exist()
        and collection_exists()
    )


# --------------------------------------------------
# Destructive cleanup
# --------------------------------------------------

def clear_markdowns() -> None:
    for f in MARKDOWN_DIR.glob("*.md"):
        f.unlink()


def clear_parent_store() -> None:
    for f in PARENT_STORE_PATH.glob("*.json"):
        f.unlink()


def clear_collection() -> None:
    client = get_client()
    try:
        if client.collection_exists(CHILD_COLLECTION):
            client.delete_collection(CHILD_COLLECTION)
    finally:
        client.close()


def clear_all_artifacts() -> None:
    clear_markdowns()
    clear_parent_store()
    clear_collection()


# --------------------------------------------------
# Build pipeline
# --------------------------------------------------

def build_pipeline(force_rebuild: bool = True) -> None:
    """
    Build or rebuild the full RAG pipeline.

    Parameters
    ----------
    force_rebuild : bool
        If True, existing artifacts and collection are deleted
        before rebuilding.
    """

    if not pdfs_exist():
        raise RuntimeError(
            "No PDFs found in data/raw. Add PDFs before building."
        )

    if force_rebuild:
        clear_all_artifacts()

    convert_all_pdfs(overwrite=True)
    index_documents()
