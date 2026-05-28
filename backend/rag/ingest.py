import json
from pathlib import Path

from rag.embedder import generate_embedding
from rag.chroma_manager import get_collection

collection = get_collection()

# Path to chunks
CHUNKS_PATH = Path("../data/processed/chunks.json")


def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def ingest_chunks():

    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks")

    for idx, chunk in enumerate(chunks):

        # Handle multiple formats
        if isinstance(chunk, dict):

            text = chunk.get("text", "")

            chunk_id = chunk.get("id", f"chunk_{idx}")

            metadata = chunk.get("metadata", {})

        else:
            text = str(chunk)

            chunk_id = f"chunk_{idx}"

            metadata = {}

        if not text.strip():
            continue

        embedding = generate_embedding(text)

        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[chunk_id],
            metadatas=[metadata]
        )

        print(f"Ingested: {chunk_id}")

    print("\nAll chunks ingested successfully!")


if __name__ == "__main__":
    ingest_chunks()