MIN_QUESTION_LENGTH = 3


def validate_question_payload(request_data):
    """Validate the JSON body for POST /api/ask.

    Return:
        (question, None) when valid
        (None, error_dict) when invalid
    """
    if not isinstance(payload, dict):
        return None, {
            "error": "invalid_request",
            "message": "Request body must be a JSON object with a question field.",
        }

    if "question" not in payload:
        return None, {
            "error": "missing_question",
            "message": "Request body must include a question field.",
        }

    question = payload["question"]

    if not isinstance(question, str):
        return None, {
            "error": "invalid_question",
            "message": "Question must be a string.",
        }

    question = question.strip()

    if not question:
        return None, {
            "error": "empty_question",
            "message": "Question must not be empty.",
        }

    if len(question) < MIN_QUESTION_LENGTH:
        return None, {
            "error": "short_question",
            "message": (
                f"Question must be at least {MIN_QUESTION_LENGTH} characters long."
            ),
        }

    return question, None