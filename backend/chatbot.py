import requests

print("Cricket AI Assistant")
print("Type 'exit' to quit\n")

conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a professional IPL commentator. "
            "Answer questions clearly and conversationally."
        )
    }
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # Add user message to memory
    conversation_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "phi",
            "messages": conversation_history,
            "stream": False
        }
    )

    data = response.json()

    ai_message = data["message"]["content"]

    print("\nAI:", ai_message)
    print()

    # Store AI response in memory
    conversation_history.append(
        {
            "role": "assistant",
            "content": ai_message
        }
    )