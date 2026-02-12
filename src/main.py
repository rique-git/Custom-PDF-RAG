from pathlib import Path

from .config import PDFS_DIR, MARKDOWN_DIR, PARENT_STORE_PATH, CHILD_COLLECTION
from .ingestion.pdf_ingestion import convert_all_pdfs
from .vectorstore.indexing import index_documents
from .vectorstore.qdrant_client import get_client
from .rag.rag import ask


# -----------------------------
# Readiness checks
# -----------------------------

def pdfs_exist():
    return any(PDFS_DIR.glob("*.pdf"))


def markdowns_exist():
    return any(MARKDOWN_DIR.glob("*.md"))


def parents_exist():
    return any(PARENT_STORE_PATH.glob("*.json"))


def collection_exists():
    client = get_client()
    exists = client.collection_exists(CHILD_COLLECTION)
    client.close()
    return exists


def system_ready():
    return (
        pdfs_exist()
        and markdowns_exist()
        and parents_exist()
        and collection_exists()
    )


# -----------------------------
# Build pipeline
# -----------------------------

def build_pipeline():
    print("\nRebuilding database...")

    # 1. Delete markdown files
    for f in MARKDOWN_DIR.glob("*.md"):
        f.unlink()

    # 2. Delete parent store files
    for f in PARENT_STORE_PATH.glob("*.json"):
        f.unlink()

    # 3. Delete Qdrant collection
    client = get_client()
    if client.collection_exists(CHILD_COLLECTION):
        client.delete_collection(CHILD_COLLECTION)
    client.close()

    # 4. Recreate everything
    convert_all_pdfs(overwrite=True)
    index_documents()

    print("Rebuild complete.\n")



# -----------------------------
# CLI
# -----------------------------

def run_cli():
    print("RAG ready. Type 'exit' to quit.\n")

    while True:
        q = input("Question: ").strip()

        if q.lower() in {"exit", "quit"}:
            break

        if not q:
            continue

        answer = ask(q)

        print("\nAnswer:\n")
        print(answer)
        print("\n" + "-" * 60 + "\n")


# -----------------------------
# Entry
# -----------------------------

if __name__ == "__main__":

    if not pdfs_exist():
        raise RuntimeError("No PDFs found in data/raw. Please add PDFs to that directory and rerun.")

    if not system_ready():
        print("\nSystem not fully built. Building now...\n")
        build_pipeline()

    else:
        rebuild = input("Rebuild database? (y/N): ").strip().lower()

        if rebuild == "y":
            build_pipeline()

    run_cli()
