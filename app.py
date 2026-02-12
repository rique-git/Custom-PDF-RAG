import streamlit as st
from pathlib import Path
import hashlib

from src.main import build_pipeline
from src.rag.rag import ask
from src.config import PDFS_DIR


# --------------------------------------------------
# PDF STATE TRACKING (content-based hash)
# --------------------------------------------------

def compute_pdf_state():
    hash_md5 = hashlib.md5()

    pdfs = sorted(PDFS_DIR.glob("*.pdf"))

    for path in pdfs:
        with open(path, "rb") as f:
            hash_md5.update(f.read())

    return hash_md5.hexdigest()


# --------------------------------------------------
# PDF MANAGEMENT
# --------------------------------------------------

def list_pdfs():
    return list(PDFS_DIR.glob("*.pdf"))


def save_uploaded_pdf(uploaded_file):
    save_path = PDFS_DIR / uploaded_file.name
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())


def delete_pdf(path):
    path.unlink()


# --------------------------------------------------
# STREAMLIT PAGE SETUP
# --------------------------------------------------

st.set_page_config(page_title="Custom RAG", layout="wide")
st.title("Custom RAG")

# Initialize session state
if "last_built_state" not in st.session_state:
    st.session_state.last_built_state = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploader_version" not in st.session_state:
    st.session_state.uploader_version = 0



# --------------------------------------------------
# SIDEBAR — PDF MANAGEMENT
# --------------------------------------------------


with st.sidebar:
    st.header("PDF Management")

    if "uploader_version" not in st.session_state:
        st.session_state.uploader_version = 0

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf",
        key=f"pdf_uploader_{st.session_state.uploader_version}"
    )

    if uploaded_file is not None:
        save_uploaded_pdf(uploaded_file)
        st.success("PDF uploaded.")
        st.session_state.uploader_version += 1
        st.rerun()

    st.subheader("Existing PDFs")

    for pdf in list_pdfs():
        col1, col2 = st.columns([4, 2])
        col1.write(pdf.name)

        if col2.button("Delete", key=pdf.name):
            delete_pdf(pdf)
            st.rerun()

    st.divider()

    if st.button("Rebuild Database"):
        with st.spinner("Rebuilding database..."):
            build_pipeline()
            st.session_state.last_built_state = compute_pdf_state()

            # Clear chat history
            st.session_state.messages = []

        st.success("Database rebuilt.")
        st.rerun()






# --------------------------------------------------
# DATABASE STATE CHECK
# --------------------------------------------------

current_state = compute_pdf_state()

db_outdated = (
    st.session_state.last_built_state is None
    or st.session_state.last_built_state != current_state
)

if db_outdated:
    st.warning("Database is outdated. Please rebuild before using the chat.")
else:
    st.success("Database is up to date.")


# --------------------------------------------------
# CHAT INTERFACE
# --------------------------------------------------

st.header("Chat")

# Hard block if DB not rebuilt
if db_outdated:
    st.stop()

# Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Ask a question about the PDFs..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
