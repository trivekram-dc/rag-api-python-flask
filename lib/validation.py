MIN_QUESTION_LENGTH = 3


def validate_question_request_data(request_data):
    """Validate the JSON body for POST /api/ask.

    Return:
        (question, None) when valid
        (None, error_dict) when invalid
    """
    if not isinstance(request_data, dict):
        return None, {
            "error": "invalid_request",
            "message": "Request body must be a JSON object with a question field.",
        }

    if "question" not in request_data:
        return None, {
            "error": "missing_question",
            "message": "Request body must include a question field.",
        }

    question = request_data["question"]

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

# Backward-compatible alias expected by app/tests
validate_question_payload = validate_question_request_data
