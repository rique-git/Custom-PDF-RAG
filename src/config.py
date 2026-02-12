from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] / "data"


PDFS_DIR = BASE_DIR / "raw"
MARKDOWN_DIR = BASE_DIR / "processed/markdowns"
PARENT_STORE_PATH = BASE_DIR / "processed/parent_store"
QDRANT_PATH = BASE_DIR / "vectorstore"

CHILD_COLLECTION = "child_chunks"
PARENT_COLLECTION = "parent_chunks"
