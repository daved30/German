import pytest
from unittest.mock import patch, MagicMock
from utils.record_audio import record_audio
import io


@patch('speech_recognition.Microphone')
@patch('speech_recognition.Recognizer')
def test_record_audio_success_v2(mock_recognizer, mock_mic):
    """
    Test that record_audio successfully returns a RAM buffer 
    when speech is detected.
    """
    # 1. Setup: Mock the recognizer and the audio data it 'hears'
    mock_inst = mock_recognizer.return_value
    mock_audio = MagicMock()
    # Simulate raw WAV bytes coming from the mic
    mock_audio.get_wav_data.return_value = b"fake_wav_data_in_ram"
    mock_inst.listen.return_value = mock_audio

    # 2. Action: Call the V2 function
    result = record_audio()

    # 3. Assert: Verify we got a BytesIO object containing our fake data
    assert isinstance(
        result, io.BytesIO), "Result should be a io.BytesIO object"
    assert result.getvalue() == b"fake_wav_data_in_ram"


@patch('speech_recognition.Microphone')
@patch('speech_recognition.Recognizer')
def test_record_audio_timeout_v2(mock_recognizer, mock_mic):
    """
    Test that record_audio returns None when a timeout occurs.
    """
    # Setup: Force a WaitTimeoutError
    mock_inst = mock_recognizer.return_value
    from speech_recognition import WaitTimeoutError
    mock_inst.listen.side_effect = WaitTimeoutError

    # Action
    result = record_audio()

    # Assert: V2 returns None on failure/timeout
    assert result is None
