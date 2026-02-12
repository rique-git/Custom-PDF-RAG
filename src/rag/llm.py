from langchain_ollama import ChatOllama

def get_llm():
    return ChatOllama(
        model="qwen3:4b-instruct-2507-q4_K_M",
        temperature=0,
    )
