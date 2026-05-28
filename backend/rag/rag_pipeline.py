from rag.retriever import retrieve_context
from rag.prompt_builder import build_prompt
from rag.generator import generate_response


def ask_cricket_agent(question: str):

    # Step 1: Retrieve context
    retrieved_chunks = retrieve_context(question)

    # Step 2: Build grounded prompt
    prompt = build_prompt(
        question,
        retrieved_chunks
    )

    # Step 3: Generate AI response
    answer = generate_response(prompt)

    return {
        "question": question,
        "answer": answer,
        "sources": retrieved_chunks
    }