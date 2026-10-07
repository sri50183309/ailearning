## Lesson 06 — Retrieve a Reference Paragraph Using Keywords

### What changed

Previously, we sent the entire contents of `reference.txt` to Qwen.
Now, Python selects one paragraph based on the user's question and
sends only that paragraph.

The reference is not generated dynamically. It is existing text
selected dynamically from the file.

### How it works

1. Read `reference.txt`.
2. Split the text into paragraphs using blank lines.
3. Extract lowercase words from the question and each paragraph.
4. Remove common words such as "the", "is", and "what".
5. Score each paragraph by counting shared unique keywords.
6. Select the paragraph with the highest score.
7. Insert it into the prompt and send it to Qwen.

### Important variables

- `reference`: the complete text loaded from the file.
- `paragraphs`: the list of paragraphs available for selection.
- `question_words`: the question's keywords.
- `scores`: each paragraph's keyword overlap count.
- `selected_reference`: the highest-scoring paragraph.
- `grounded_prompt`: instructions, selected evidence, and question.

### Python concepts

- `re.findall()`: extracts words using a regular expression.
- `set`: stores unique words.
- Set subtraction (`-`): removes stop words.
- Set intersection (`&`): finds shared words.
- `max(..., key=...)`: selects the index with the highest score.
- An f-string: inserts selected evidence and the question into the prompt.

### Test results

Question: What does HTTP 500 mean?
- Keyword overlap: 2 (`http` and `500`).
- Selected the HTTP 500 paragraph.
- The model returned the correct definition.

Question: What is the default timeout in Spring Boot?
- Keyword overlap: 1 (`timeout`).
- Selected the general timeout paragraph.
- The model returned a true sentence that did not answer the question.

### Limitations

- Shared words do not prove that a paragraph contains the answer.
- This search matches words, not meaning.
- With equal scores, the first matching paragraph is selected.
- Even when every score is zero, the current code selects a paragraph.
- The extraction prompt does not reliably handle missing information.

### Main learning

Retrieval quality and answer quality must be evaluated separately.
A factually correct sentence can still be an incorrect answer to
the user's question.