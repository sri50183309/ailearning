import json
import time
import urllib.request
from pathlib import Path
import re

question = input("Your question: ").strip()

if not question:
    print("Please enter a question.")
    raise SystemExit
    
reference_path = Path(__file__).resolve().parent / "reference.txt"

try:
    reference = reference_path.read_text(encoding="utf-8")
except FileNotFoundError:
    print(f"Reference file not found: {reference_path}")
    raise SystemExit(1)

if not reference.strip():
    print("The reference file is empty.")
    raise SystemExit(1)

stop_words = {
    "a", "an", "the", "is", "are", "was", "what", "does",
    "do", "can", "in", "of", "to", "and", "or", "it",
}

def keywords(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return set(words) - stop_words

paragraphs = [
    paragraph.strip()
    for paragraph in reference.split("\n\n")
    if paragraph.strip()
]

question_words = keywords(question)

scores = [
    len(question_words & keywords(paragraph))
    for paragraph in paragraphs
]

best_index = max(range(len(paragraphs)), key=lambda i: scores[i])
selected_reference = paragraphs[best_index]

print("\nKeyword overlap:", scores[best_index])
print("Selected evidence:\n", selected_reference)

grounded_prompt = f"""
Reference:
{selected_reference}

Question:
{question}

Copy the sentence from the reference that directly answers
the question. Return only that sentence.
"""    
    
payload = {
    "model": "qwen3:0.6b",
    "prompt": grounded_prompt,
    "stream": False,
    "think": False,
    "options": {
        "num_ctx": 1024,
        "num_predict": 128,
        "temperature": 0,
    },
    "keep_alive": 0,
}

# print("\n--- Prompt sent to Ollama ---")
# print(payload["prompt"])
# print("--- End of prompt ---\n")

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