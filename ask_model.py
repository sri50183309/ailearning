import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path


STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "what", "does",
    "do", "can", "in", "of", "to", "and", "or", "it",
}


def load_reference(path):
    reference = path.read_text(encoding="utf-8")

    if not reference.strip():
        raise ValueError("The reference file is empty.")

    return reference


def keywords(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return set(words) - STOP_WORDS


def retrieve_paragraph(question, reference):
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

    best_index = max(
        range(len(paragraphs)),
        key=lambda i: scores[i],
    )

    return paragraphs[best_index], scores[best_index]


def build_prompt(question, selected_reference):
    return f"""
Reference:
{selected_reference}

Question:
{question}

Copy the sentence from the reference that directly answers
the question. Return only that sentence.
"""


def call_model(prompt):
    payload = {
        "model": "qwen3:0.6b",
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {
            "num_ctx": 1024,
            "num_predict": 128,
            "temperature": 0,
        },
        "keep_alive": 0,
    }

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    started = time.perf_counter()

    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.load(response)

    elapsed = time.perf_counter() - started
    return result["response"], elapsed


def main():
    question = input("Your question: ").strip()

    if not question:
        print("Please enter a question.")
        return

    reference_path = (
        Path(__file__).resolve().parent / "reference.txt"
    )

    try:
        reference = load_reference(reference_path)
    except FileNotFoundError:
        print(f"Reference file not found: {reference_path}")
        raise SystemExit(1)
    except ValueError as error:
        print(error)
        raise SystemExit(1)

    selected_reference, best_score = retrieve_paragraph(
        question, reference
    )

    if best_score == 0:
        print(
            "\nNo matching keywords were found in the reference. "
            "The model was not called."
        )
        return

    print("\nKeyword overlap:", best_score)
    print("Selected evidence:\n", selected_reference)

    prompt = build_prompt(question, selected_reference)

    print("Asking the local model…")

    try:
        answer, elapsed = call_model(prompt)

        print("\nAnswer:", answer)
        print(f"\nElapsed: {elapsed:.1f} seconds")

    except urllib.error.HTTPError as error:
        print("Ollama error:", error.read().decode("utf-8"))
    except urllib.error.URLError as error:
        print("Connection error:", error.reason)
    except TimeoutError:
        print("The request timed out.")


if __name__ == "__main__":
    main()