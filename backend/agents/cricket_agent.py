from .graph import graph

# ----------------------------------
# Test 2
# ----------------------------------

result = graph.invoke(
    {
        "question": "Tell me about Virat Kohli IPL career"
    }
)

print("\nRESULT:")
print(result["final_answer"])
