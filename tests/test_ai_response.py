import pytest
from unittest.mock import patch
from utils.get_ai_response import get_ai_response


@patch('ollama.chat')
def test_get_ai_response_streaming(mock_chat):
    # 1. Mock Ollama to simulate a stream of chunks
    mock_chat.return_value = [
        {'message': {'content': 'Hallo'}},
        {'message': {'content': ' Dave!'}}
    ]

    # 2. Capture the generator
    gen = get_ai_response("glm4:9b", "Hi")

    # 3. Collect tokens and verify
    result = "".join(list(gen))
    assert result == "Hallo Dave!"
