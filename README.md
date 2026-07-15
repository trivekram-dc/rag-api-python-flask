# Lab: Build a Flask RAG API Endpoint

## Overview

You will be **implementing a Flask RAG API endpoint** within a **customer success knowledge-base scenario** in connection to **Identify → Assemble → Execute → Verify** with **request validation, Chroma retrieval, prompt and context engineering, model-client integration, source attribution, fallback behavior, and structured JSON response design** to a standard where your code passes the provided pytest test suite and returns a grounded answer with supporting sources.

In this lab, you will connect the retrieval foundation from the previous module to a backend AI workflow. A RAG API helps an application retrieve relevant source material, place that context into a structured prompt, call a model, and return a response that users and developers can inspect.

The goal is not just to make an AI model respond. The goal is to build a backend workflow that controls what the model receives, avoids unsupported answers, and returns predictable data that a frontend could display.

## You'll get

**Support:**

- Starter Flask app structure
- Starter files in `lib/`
- A provided customer success knowledge base
- A Chroma seeding script for manual local testing
- A deterministic pytest suite
- Mocked retrieval and model behavior in tests
- Optional Ollama support for local experimentation

**Rules:**

- You may use the starter code, course lessons, Python documentation, and your notes.
- You may run pytest as many times as needed.
- You should not modify the test files for grading.
- You should not hard-code answers for specific test questions.
- You should not hard-code the test fixtures into your implementation.
- You should not use LangChain for this lab.
- You should implement Chroma retrieval in your code, but tests will mock retrieval where needed.
- You do not need internet access or Ollama to pass the tests.
- Ollama is optional for local manual testing after your tests pass.
- Your grade is based on pytest results only.

## You will be able to

- **Validate** incoming JSON requests before the RAG workflow starts.
- **Retrieve** relevant context from a Chroma-style collection.
- **Normalize** Chroma query results into context chunks.
- **Build** a structured RAG prompt from instructions, context, a user question, and response requirements.
- **Call** a model client for local manual testing.
- **Return** structured JSON with an answer and source metadata.
- **Use** fallback behavior when approved context is missing.
- **Verify** the backend workflow using pytest.

## You'll show it by

Creating and submitting a completed Flask RAG API project that implements:

- `POST /api/ask`
- `validate_question_payload()`
- `format_chroma_results()`
- `retrieve_context()`
- `format_context_chunk()`
- `build_rag_prompt()`
- `generate_answer()`
- `format_sources()`
- `format_success_response()`
- `format_fallback_response()`
- `answer_question()`

Your submission will be tested with `pytest`.

## How you'll work

This lab uses the technical process **Identify → Assemble → Execute → Verify**.

That process fits a RAG API because you need to identify the endpoint contract, assemble the route and helper functions, execute the request through retrieval and generation, and verify the answer, sources, JSON shape, and fallback behavior.

## To meet the standard, your work must

- Pass the provided pytest suite.
- Accept valid `POST /api/ask` requests.
- Reject missing, blank, invalid, or too-short questions before retrieval.
- Query Chroma using the user question and `top_k`.
- Normalize retrieved context into dictionaries with text and source metadata.
- Build a prompt with clear sections:
  - `Instructions:`
  - `Context:`
  - `Question:`
  - `Response Requirements:`
- Instruct the model to use only approved context.
- Return a JSON object with:
  - `answer`
  - `sources`
- Include source metadata in successful grounded responses.
- Return a safe fallback response when context is missing.
- Return a clear service error response when the model client fails.
- Keep route, validation, retrieval, prompt, model, response, and orchestration logic separated.

---

## Scenario

You are a junior backend developer on an internal tools team. The Customer Success department supports subscription customers who ask about plan changes, invoices, service credits, workspace exports, account access, and onboarding limits.

Support representatives often ask natural-language questions such as:

> Can I upgrade a customer today and explain what happens to billing?

The approved information exists in customer success policy documents, but representatives do not always know which document to search. Your task is to build a small RAG API that retrieves relevant customer success context from Chroma, asks a local model to answer using that context, and returns an answer with sources.

A strong answer should be:

- grounded in retrieved context,
- clear enough for a support representative to use,
- careful about missing information,
- and source-backed so the response can be reviewed.

---

## Tools and resources

- Python 3.10
- Visual Studio Code or another code editor
- Terminal or integrated terminal
- `pipenv`
- Flask
- ChromaDB
- pytest
- Optional: Ollama installed and running locally
- Optional: a generation model such as `llama3.2`

---

## Instructions

### Setup

Install dependencies:

```bash
pipenv install
pipenv shell
```

Run the tests:

```bash
pytest
```

The tests will fail at first. That is expected. Your job is to implement the starter functions until the test suite passes.

### Step 1: Identify the RAG API goal and output contract

Your endpoint should receive:

```json
{
  "question": "Can I upgrade a customer today?"
}

Your endpoint route must be:

```http
POST /api/ask
```

A successful response must include:

* answer
* sources

A fallback response must include a safe answer and an empty source list.

### Step 2: Implement request validation

Open `lib/validation.py`. Implement: `validate_question_payload(payload)`

This function should:

* Require a JSON object.
* Require a question field.
* Require the question to be a string.
* Trim extra whitespace.
* Reject blank questions.
* Reject questions shorter than 3 characters.
* Return the cleaned question and no error when valid.
* Return no question and an error dictionary when invalid.

### Step 3: Implement Chroma retrieval helpers

Open `lib/retrieval.py`.

Implement:
* `get_chroma_collection()`
* `format_chroma_results()`
* `retrieve_context()`

Your retrieval code should:

* Connect to a local persistent Chroma collection.
* Query with the user question.
* Use the provided `top_k`.
* Request documents, metadata, and distances.
* Normalize Chroma's nested query result shape.
* Return context chunks with text and source metadata.

### Step 4: Implement prompt construction

Open `lib/prompt_builder.py`.

Implement:

* `format_context_chunk()`
* `build_rag_prompt()`

Your prompt should include:

```text
Instructions:
Context:
Question:
Response Requirements:
```

Your prompt should tell the model to:

* Use only the approved context.
* Avoid inventing unsupported details.
* Identify missing information when context is incomplete.
* Answer concisely.
* Use source IDs when helpful.

### Step 5: Implement the model client

Open `lib/model_client.py`.

Implement `generate_answer()`

The model client should:

* Send a prompt to Ollama's `/api/generate` endpoint.
* Use `stream: false`.
* Return the generated response text.
* Raise `ModelClientError` if the model request fails.
* Raise `ModelClientError` if the response is missing or unusable.

The tests mock this behavior, so you do not need Ollama to pass pytest.

### Step 6: Implement response formatting

Open `lib/response_formatter.py`.

Implement:
* `format_sources()`
* `format_success_response()`
* `format_fallback_response()`
* `format_error_response()`

Your response formatting should:

* Return source metadata without including full chunk text.
* Avoid duplicate source entries.
* Return an answer and sources list for success.
* Return a safe fallback answer with sources: `[]`.
* Return clear error dictionaries for validation or model-service failures.

#### Step 7: Implement the RAG service

Open `lib/rag_service.py`. Implement the `answer_question()` function.

This function should coordinate the workflow:

```text
question
→ retrieve context
→ return fallback if no context
→ build prompt
→ call model
→ format answer and sources
```

Do not call the model when no useful context is retrieved.

#### Step 8: Implement the Flask route

Open `app.py`. Implement:

```http
POST /api/ask
```

The route should:

* Read the JSON request body.
* Validate the question.
* Return 400 for invalid input.
* Call the RAG service for valid input.
* Return 200 for successful or fallback RAG responses.
* Return 502 for model-service errors.

#### Step 9: Verify your work

Run:

```bash
pytest -q
```

Keep working until all tests pass.

