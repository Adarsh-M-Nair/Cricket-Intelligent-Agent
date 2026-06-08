from backend.rag.retriever import retrieve_context

chunks = retrieve_context(
    "Virat Kohli"
)

print(chunks)