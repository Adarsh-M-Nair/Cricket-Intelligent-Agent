# backend/rag/ingest.py

import json
from pathlib import Path

from backend.rag.embedder import generate_embedding
from backend.rag.chroma_manager import get_collection

collection = get_collection()


# --------------------------------------------------
# Project Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

CHUNKS_PATH = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "chunks.json"
)


# --------------------------------------------------
# Load Chunks
# --------------------------------------------------

def load_chunks():

    print(f"Loading chunks from:\n{CHUNKS_PATH}")

    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"Chunks file not found:\n{CHUNKS_PATH}"
        )

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------
# Ingest Chunks
# --------------------------------------------------

def ingest_chunks():

    chunks = load_chunks()

    print(f"\nLoaded {len(chunks)} chunks\n")

    for idx, chunk in enumerate(chunks):

        # Handle dictionary format
        if isinstance(chunk, dict):

            text = chunk.get("text", "")

            chunk_id = chunk.get(
                "id",
                f"chunk_{idx}"
            )

            metadata = chunk.get(
                "metadata",
                {}
            )

        else:

            text = str(chunk)

            chunk_id = f"chunk_{idx}"

            metadata = {}

        # Skip empty chunks
        if not text.strip():
            continue

        try:

            # Skip if already exists
            existing = collection.get(
                ids=[chunk_id]
            )

            if existing["ids"]:
                print(
                    f"Skipping existing chunk: {chunk_id}"
                )
                continue

            embedding = generate_embedding(text)

            collection.add(
                ids=[chunk_id],
                documents=[text],
                embeddings=[embedding],
                metadatas=[metadata]
            )

            print(
                f"Ingested: {chunk_id}"
            )

        except Exception as e:

            print(
                f"Error ingesting {chunk_id}: {e}"
            )

    print(
        "\nAll chunks ingested successfully!"
    )

    print(
        f"Total vectors in collection: "
        f"{collection.count()}"
    )


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":

    ingest_chunks()