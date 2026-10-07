import json
import time
import urllib.request
from pathlib import Path

question = input("Your question: ").strip()

if not question:
    print("Please enter a question.")
    raise SystemExit
    
reference = reference_path = Path(__file__).resolve().parent / "reference.txt"

try:
    reference = reference_path.read_text(encoding="utf-8")
except FileNotFoundError:
    print(f"Reference file not found: {reference_path}")
    raise SystemExit(1)

if not reference.strip():
    print("The reference file is empty.")
    raise SystemExit(1)

grounded_prompt = f"""
Answer the question using only the reference below.
If the reference does not contain the answer, say:
"The reference does not contain enough information."
Use up to two sentences. Do not add claims beyond the reference.
Do not label timeouts as client-side or server-side issues.
Do not include formatting commentary such as "(Two sentences)".

Reference:
{reference}

Question:
{question}
"""    
    
payload = {
    "model": "qwen3:0.6b",
    "prompt": grounded_prompt,
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