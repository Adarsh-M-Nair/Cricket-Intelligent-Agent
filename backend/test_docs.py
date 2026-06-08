from backend.rag.chroma_manager import get_collection

collection = get_collection()

results = collection.get(limit=5)

print(results)