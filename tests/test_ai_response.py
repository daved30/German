import pytest
from utils.get_ai_response import get_ai_response


def test_ollama_live_response():
    """
    Real-world check: Does Ollama return a sensible German response?
    """
    model = "glm4:9b"
    prompt = "Hallo, wie heißt du?"

    # Action
    response = get_ai_response(model, prompt)

    # Assert
    assert response is not None
    assert "Error" not in response
    assert len(response) > 5
    print(f"\nAI Response: {response}")
