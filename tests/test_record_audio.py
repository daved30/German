import pytest
from unittest.mock import patch, MagicMock
from utils.record_audio import record_audio
import os

@patch('speech_recognition.Microphone')
@patch('speech_recognition.Recognizer')
def test_record_audio_success(mock_recognizer, mock_mic):
    # 1. Setup: Mock the audio data and the listen method
    mock_inst = mock_recognizer.return_value
    mock_audio = MagicMock()
    mock_audio.get_wav_data.return_value = b"fake_wav_data"
    mock_inst.listen.return_value = mock_audio

    test_file = "test_pytest.wav"

    # 2. Action
    result = record_audio(test_file)

    # 3. Assert: Did it return True and create a file?
    assert result is True
    assert os.path.exists(test_file)
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)

@patch('speech_recognition.Microphone')
@patch('speech_recognition.Recognizer')
def test_record_audio_timeout(mock_recognizer, mock_mic):
    # Setup: Force a timeout error
    mock_inst = mock_recognizer.return_value
    from speech_recognition import WaitTimeoutError
    mock_inst.listen.side_effect = WaitTimeoutError

    result = record_audio("timeout.wav")

    # Assert: Should return False on timeout
    assert result is False
