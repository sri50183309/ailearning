import json
import time
import urllib.request

payload = {
    "model": "qwen3:0.6b",
    "prompt": "Explain an API timeout in two sentences.",
    "stream": False,
    "think": False,
    "options": {
        "num_ctx": 1024,
        "num_predict": 128,
    },
    "keep_alive": 0,
}

request = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

print("Asking the local model…")
started = time.perf_counter()

try:
    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.load(response)

    print("\nAnswer:", result["response"])
    print(f"\nElapsed: {time.perf_counter() - started:.1f} seconds")

except urllib.error.HTTPError as error:
    print("Ollama error:", error.read().decode("utf-8"))
except urllib.error.URLError as error:
    print("Connection error:", error.reason)
except TimeoutError:
    print("The request timed out.")