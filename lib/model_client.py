import requests

DEFAULT_MODEL_NAME = "llama3.2"
DEFAULT_BASE_URL = "http://localhost:11434"


class ModelClientError(Exception):
    """Raised when the local model service cannot return a usable answer."""


def generate_answer(prompt, model_name=DEFAULT_MODEL_NAME, base_url=DEFAULT_BASE_URL):
    """Send the prompt to a local Ollama model and return the generated answer."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ModelClientError("Prompt must be a non-empty string.")

    url = f"{base_url.rstrip('/')}/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ModelClientError(f"Model service request failed: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise ModelClientError("Model service returned invalid JSON.") from exc

    answer = data.get("response")

    if not isinstance(answer, str) or not answer.strip():
        raise ModelClientError("Model service did not return a usable response.")

    return answer.strip()