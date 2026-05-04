import pytest
import io
import wave
import numpy as np
from utils.record_audio import record_audio
from utils.transcribe_german import transcribe_german


def test_integration_ram_to_transcription():
    """
    V2 Integration Test: Validates the full path from Mic -> RAM -> Whisper.
    """
    print("\n--- V2 VALIDATION REQUIRED ---")
    print("Please say 'Das ist ein Test' clearly...")

    # 1. Record to RAM
    audio_stream = record_audio()
    assert isinstance(
        audio_stream, io.BytesIO), "Recorder did not return a RAM buffer."

    # 2. Transcribe using that specific RAM buffer
    text = transcribe_german(audio_stream)

    # 3. Assertions
    assert text is not None, "Transcription returned None."
    assert len(text) > 0, "Transcription resulted in empty text."
    print(f"V2 Whisper heard: {text}")
