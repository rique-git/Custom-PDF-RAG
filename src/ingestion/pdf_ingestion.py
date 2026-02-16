import glob
from pathlib import Path
import pymupdf
import pymupdf4llm

from ..config import MARKDOWN_DIR, PDFS_DIR



def pdf_to_markdown(pdf_path, output_dir):
    doc = pymupdf.open(pdf_path)
    md = pymupdf4llm.to_markdown(
        doc,
        page_separators=True,
        ignore_images=True,
        write_images=False,
    )

    cleaned = md.encode("utf-8", errors="surrogatepass").decode("utf-8", errors="ignore")
    output_path = Path(output_dir) / Path(doc.name).stem
    Path(output_path).with_suffix(".md").write_bytes(cleaned.encode("utf-8"))




def convert_all_pdfs(overwrite=False):
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)

    for pdf_path in map(Path, glob.glob(f"{PDFS_DIR}/*.pdf")):
        md_path = (MARKDOWN_DIR / pdf_path.stem).with_suffix(".md")

        if overwrite or not md_path.exists():
            pdf_to_markdown(pdf_path, MARKDOWN_DIR)

            with open(md_path, "r", encoding="utf-8") as f:
                md_text = f.read()

            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_text)

