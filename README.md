# ailearning
This is going to my repo for learning


ollama run qwen3:0.6b

ollama serve

That starts the local API server without selecting a model. If the Ollama Windows app is already running, the server is usually already started.

curl http://localhost:11434/api/tags -> list all models in ollama

| Lesson | What we built | What you learned |
|---|---|---|
| **1 — Call a local model** | Python sent a fixed question to Qwen through Ollama’s HTTP API | Build a JSON request, send it, read the response, and measure elapsed time |
| **2 — Accept user input** | Replaced the fixed question with `input()` | Make the script interactive; a successful API call can still produce an inaccurate answer |
| **3 — Supply reference context** | Included a reference passage alongside the question | Ground answers in supplied information and test whether the model declines unsupported questions |

Lesson 05:
This suggests the model can find the relevant sentence, but struggles with our combined answer-or-refuse instructions. It doesn’t establish the precise cause.
Let’s finish Lesson 05 by recording what we learned:
- The reference reaches the model.
- Answerable questions sometimes trigger false refusals.
- Temperature 0 and a simpler prompt didn’t fix those cases.
- Evidence extraction succeeded on this question.
Keep the extraction prompt as an experiment, not our final assistant behaviour—we haven’t tested it on missing information.


Lesson 06:
- HTTP 500 question: selected the relevant paragraph and answered correctly.
- Spring Boot default: overlap score 1 selected a related paragraph,
  but the output did not answer the question.
- Keyword overlap measures shared words, not answerability.
- Evidence extraction alone does not handle missing information.

## Lesson 07 — Stop on Zero Keyword Matches

Added a guard that exits before calling the model when the best
paragraph has a keyword overlap score of zero.

Test: "Who invented the bicycle?"
Result: No matching keywords; the model was not called.

This avoids sending an arbitrary paragraph and saves inference work.
It does not establish whether an answer exists: keyword search can
miss differently worded evidence, and positive matches can still
be insufficient.