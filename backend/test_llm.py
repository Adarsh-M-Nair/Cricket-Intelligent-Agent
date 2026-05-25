import requests

prompt = "Who is the best IPL finisher and why?"

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
)

data = response.json()

print(data["response"])