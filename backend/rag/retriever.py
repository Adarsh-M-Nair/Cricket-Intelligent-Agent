from rag.embedder import generate_embedding
from rag.chroma_manager import get_collection

collection = get_collection()


def retrieve_context(query: str, n_results: int = 3):

    # Generate query embedding
    query_embedding = generate_embedding(query)

    # Search vector database
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    ids = results.get("ids", [[]])[0]

    retrieved_chunks = []

    for doc, meta, chunk_id in zip(documents, metadatas, ids):

        retrieved_chunks.append({
            "id": chunk_id,
            "text": doc,
            "metadata": meta
        })

    return retrieved_chunks