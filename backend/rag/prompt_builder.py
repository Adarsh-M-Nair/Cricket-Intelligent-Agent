def build_prompt(question: str, retrieved_chunks: list):

    context = "\n\n".join(
        [chunk["text"] for chunk in retrieved_chunks]
    )

    prompt = f"""
You are a cricket analytics assistant.

Answer the question ONLY using the provided context.

If the answer is not in the context, say:
"I could not find enough cricket information."

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt