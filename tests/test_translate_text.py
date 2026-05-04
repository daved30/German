import pytest
from unittest.mock import patch
from utils.translate_text import translate_text

# We 'patch' the ollama.chat function so it doesn't actually call the local server


@patch('ollama.chat')
def test_translate_text_success(mock_chat):
    # 1. Setup: Define what the fake Ollama should return
    mock_chat.return_value = {
        'message': {
            'content': 'How are you?'
        }
    }

    # 2. Action: Call our utility function
    result = translate_text("glm4:9b", "Wie geht es dir?")

    # 3. Assert: Verify the result is what we expected
    assert result == "How are you?"
    assert isinstance(result, str)


@patch('ollama.chat')
def test_translate_text_error_handling(mock_chat):
    # Setup: Make the mock throw an exception (simulating Ollama being offline)
    mock_chat.side_effect = Exception("Connection refused")

    result = translate_text("glm4:9b", "Hallo")

    # Assert: Verify it returns the error string we defined in the util
    assert result == "[Translation Error]"
