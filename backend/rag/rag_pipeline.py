from rag.retriever import retrieve_context
from rag.prompt_builder import build_prompt
from rag.generator import generate_response


def ask_cricket_agent(
    question: str,
    top_k: int = 3
):

    retrieved_chunks = retrieve_context(
    question,
    n_results=top_k
)

    if not retrieved_chunks:

        return {
            "question": question,
            "answer": "No relevant cricket information found.",
            "sources": []
        }

    prompt = build_prompt(
        question,
        retrieved_chunks
    )

    answer = generate_response(prompt)

    return {
        "question": question,
        "answer": answer,
        "sources": retrieved_chunks
    }