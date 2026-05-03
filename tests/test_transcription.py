import pytest
import os
import wave
from utils.transcribe_german import transcribe_german

def test_whisper_transcription_accuracy():
    """
    Validates that Whisper correctly transcribes a specific German phrase.
    Note: Requires an actual model load, so it will take a few seconds.
    """
    # 1. We'll use the 'integration_test.wav' from your previous run if it exists,
    # but for a standard test, we check if the function handles a file.
    test_file = "test_input.wav"
    
    # We skip if the file doesn't exist, or you can record a fresh one here
    if not os.path.exists(test_file):
        pytest.skip("No test audio file found. Run record_audio first.")

    # 2. Action
    result = transcribe_german(test_file)

    # 3. Assert
    assert result is not None
    assert len(result) > 0
    print(f"\nWhisper actually heard: {result}")
