from .graph import graph


# ----------------------------------
# Test 1
# ----------------------------------

result = graph.invoke(
    {
        "question": "What is Virat Kohli's strike rate?"
    }
)

print("\nRESULT 1")
print(result)


# ----------------------------------
# Test 2
# ----------------------------------

result = graph.invoke(
    {
        "question": "Tell me about Virat Kohli IPL career"
    }
)

print("\nRESULT 2")
print(result)
