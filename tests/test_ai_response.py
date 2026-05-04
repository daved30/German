import pytest
from unittest.mock import patch
from utils.get_ai_response import get_ai_response


@patch('ollama.chat')
def test_get_ai_response_stream_logic(mock_chat):
    # Setup mock to return a list (simulating a stream)
    mock_chat.return_value = [
        {'message': {'content': 'Hallo'}},
        {'message': {'content': ' Dave!'}}
    ]

    # Action
    response_gen = get_ai_response("glm4:9b", "Hi")

    # Collect tokens from the generator
    full_text = "".join(list(response_gen))

    # Assert
    assert full_text == "Hallo Dave!"
