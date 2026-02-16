from langchain_ollama import ChatOllama
import os
from ..config import OLLAMA_BASE_URL

def get_llm():
    return ChatOllama(
        model="qwen3:4b-instruct-2507-q4_K_M",
        temperature=0,
        base_url=os.getenv("OLLAMA_BASE_URL", OLLAMA_BASE_URL)
    )
