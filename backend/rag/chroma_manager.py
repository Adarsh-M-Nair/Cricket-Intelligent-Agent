import chromadb

# Persistent local database
client = chromadb.PersistentClient(path="./chroma_db")

# Create or load collection
collection = client.get_or_create_collection(
    name="cricket_knowledge"
)


def get_collection():
    return collection