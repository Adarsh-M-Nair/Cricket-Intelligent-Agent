from rag.rag_pipeline import ask_cricket_agent

question = "Who won the match between Mumbai Indians and RCB?"

response = ask_cricket_agent(question)

print("\nQUESTION:")
print(response["question"])

print("\nANSWER:")
print(response["answer"])

print("\nSOURCES:")
for source in response["sources"]:
    print(source["id"])