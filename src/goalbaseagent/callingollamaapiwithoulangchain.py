import requests
import json

url = "http://localhost:11434/api/generate"

payload = {
    "model": "llama3.2",   # make sure you've run: ollama pull llama3.2
    "prompt": "Hello! Explain AI in one sentence."
}

response = requests.post(url, json=payload, stream=True)

# Ollama streams responses line by line
for line in response.iter_lines():
    if line:
        data = json.loads(line.decode("utf-8"))
        if "response" in data:
            print(data["response"], end="", flush=True)

print("\n\n✅ Done")