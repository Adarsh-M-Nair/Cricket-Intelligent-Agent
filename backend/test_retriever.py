from rag.retriever import retrieve_context

query = "Who scored aggressively against Mumbai Indians?"

results = retrieve_context(query)

print("\nRetrieved Results:\n")

for idx, result in enumerate(results, start=1):

    print(f"Result {idx}")
    print("-" * 50)

    print("ID:", result["id"])

    print("TEXT:")
    print(result["text"])

    print("METADATA:")
    print(result["metadata"])

    print("\n")