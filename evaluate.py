import json
from pathlib import Path

from ask_model import (
    load_reference,
    retrieve_paragraph,
    build_prompt,
    call_model,
)


def main():
    project_folder = Path(__file__).resolve().parent
    cases_path = project_folder / "evaluation_cases.json"

    cases = json.loads(cases_path.read_text(encoding="utf-8"))

    print(f"Loaded {len(cases)} evaluation cases.\n")

    reference = load_reference(project_folder / "reference.txt")
    
    results = []

    for case in cases:
        question = case["question"]
        evidence, score = retrieve_paragraph(question, reference)

        print(f"\nCase: {case['id']}")
        print(f"Question: {question}")
        print(f"Keyword overlap: {score}")

        if score == 0:
            print("No matching evidence; model call skipped.")
            continue

        print(f"Selected evidence:\n{evidence}")
        
        record = {
            "id": case["id"],
            "question": question,
            "score": score,
            "evidence": evidence,
            "expected": case["expected"],
            "must_avoid": case["must_avoid"],
        }

        prompt = build_prompt(question, evidence)

        try:
            answer, elapsed = call_model(prompt)
            
            record["answer"] = answer
            record["elapsed_seconds"] = round(elapsed, 2)

            print(f"Answer: {answer}")
            print(f"Elapsed: {elapsed:.1f} seconds")
            print(f"Expected meaning: {case['expected']}")
            print(f"Must avoid: {case['must_avoid']}")

        except Exception as error:
            print(f"Case failed: {type(error).__name__}: {error}")
            record["error"] = str(error)
        
        results.append(record)
    
    results_path = project_folder / "evaluation_results.json"
    results_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()