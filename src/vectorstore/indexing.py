import json
import uuid
from pathlib import Path
from langchain_core.documents import Document


from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from ..config import MARKDOWN_DIR, PARENT_STORE_PATH
from .qdrant_client import recreate_collection, get_vector_store


def index_documents():

    recreate_collection()
    vector_store = get_vector_store()

    #headers = [("#", "H1"), ("##", "H2"), ("###", "H3")]

    #parent_splitter = MarkdownHeaderTextSplitter(
    #    headers_to_split_on=headers,
    #    strip_headers=False,
    #)

    parent_splitter = RecursiveCharacterTextSplitter(
        separators=["#", "##", "###", "\n\n\n", "\n\n"],
        chunk_size=1500,
        chunk_overlap=200,
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    md_files = sorted(MARKDOWN_DIR.glob("*.md"))

    PARENT_STORE_PATH.mkdir(parents=True, exist_ok=True)

    for file in PARENT_STORE_PATH.glob("*.json"):
        file.unlink()

    all_children = []

    for md_file in md_files:

        text = md_file.read_text(encoding="utf-8")
        parent_texts = parent_splitter.split_text(text)

        parents = [
            Document(
                page_content=chunk,
                metadata={
                    "source": str(md_file.stem) + ".pdf"
                }
            )
            for chunk in parent_texts
        ]

        for parent_doc in parents:
            parent_id = str(uuid.uuid4())

            parent_doc.metadata["parent_id"] = parent_id

            parent_path = PARENT_STORE_PATH / f"{parent_id}.json"

            with open(parent_path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "page_content": parent_doc.page_content,
                        "metadata": parent_doc.metadata,
                    },
                    f,
                    ensure_ascii=False,
                    indent=2,
                )

            children = child_splitter.split_documents([parent_doc])
            all_children.extend(children)

    if all_children:
        vector_store.add_documents(all_children)

