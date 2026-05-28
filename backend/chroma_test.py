import sys
from pathlib import Path

# Ensure project package directory is on sys.path so 'rag' can be imported
project_root = Path(__file__).resolve().parent
# Ensure both the backend dir and its parent (project package root) are on sys.path
for p in (project_root, project_root.parent):
    sp = str(p)
    if sp not in sys.path:
        sys.path.insert(0, sp)

from rag.chroma_manager import get_collection
from rag.embedder import generate_embedding

collection = get_collection()

text = "Virat Kohli scored 82 against Mumbai Indians"

embedding = generate_embedding(text)

collection.add(
    documents=[text],
    embeddings=[embedding],
    ids=["test_1"]
)

print("Document stored successfully!")