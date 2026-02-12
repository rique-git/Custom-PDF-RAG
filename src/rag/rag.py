from .retriever import retrieve
from .llm import get_llm


def ask(query: str):

    parents = retrieve(query)

    if not parents:
        return "I do not have information in the indexed documents to answer that."

    context = "\n\n".join(p["page_content"] for p in parents)

    prompt = f"""
            You are a assistant answering questions strictly using the provided context.

            Rules:
            - Use only the information present in the context.
            - Do not use outside knowledge.
            - If the answer is not contained in the context, respond exactly with:
            "I do not have information in the indexed documents to answer that."
            - Always cite the source document in the format [source: filename.pdf].

            Context:
            {context}

            Question:
            {query}
            """

    llm = get_llm()
    response = llm.invoke(prompt)

    return response.content.strip()
