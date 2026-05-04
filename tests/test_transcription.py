import pytest
import io
import wave
from utils.transcribe_german import transcribe_german


def test_whisper_transcription_v2_logic():
    """
    Validates that the V2 transcriber accepts and processes a valid RAM buffer.
    """
    # 1. Create a VALID (but silent) WAV file in a RAM buffer
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(b'\x00' * 32000)  # 1 second of silence

    # Reset buffer pointer to the beginning for reading
    buffer.seek(0)

    # 2. Action
    result = transcribe_german(buffer)

    # 3. Assert
    # On silence, Whisper usually returns an empty string "", not None.
    # None only happens if the file logic itself crashes.
    assert result is not None
    assert isinstance(result, str)


def test_transcription_none_handling():
    """Ensures the transcriber handles empty input gracefully."""
    result = transcribe_german(None)
    assert result is None
