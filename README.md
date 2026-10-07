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