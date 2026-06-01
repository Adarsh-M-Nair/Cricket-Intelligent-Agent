def build_prompt(question: str, retrieved_chunks: list):

    context_parts = []

    for chunk in retrieved_chunks:

        metadata = chunk.get("metadata", {})

        if metadata is None:
            metadata = {}

        winner = metadata.get("winner", "Unknown")

        context_parts.append(
            f"""
    SOURCE: {chunk.get("id", "Unknown")}
    WINNER: {winner}

    CONTENT:
    {chunk.get("text", "")}
    """
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are an expert cricket analyst and statistics assistant.

Rules:
1. Answer ONLY using the provided context.
2. Do NOT make up facts.
3. If the answer is not present in the context, reply:
   "I could not find enough cricket information."
4. Keep answers concise and factual.
5. When possible, mention teams, players, scores, winners, or statistics.
6. Use cricket terminology naturally.
7. Answer in complete sentences.
8. Do not repeat the question.
9. Prefer one concise paragraph unless comparison is requested.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt