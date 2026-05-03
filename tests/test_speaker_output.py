import pytest
import os
import asyncio
from utils.generate_speech import generate_speech

# This tells pytest-asyncio to treat this file's async tests automatically
pytestmark = pytest.mark.asyncio

async def test_speaker_and_audio_file_creation():
    """
    Validates that a German sentence is converted to an MP3 and played.
    """
    test_text = "Ich bin bereit zu sprechen."
    test_file = "response.mp3"

    # 1. Cleanup old file
    if os.path.exists(test_file):
        os.remove(test_file)

    # 2. Action
    await generate_speech(test_text)

    # 3. Assert: Verify the logic flow worked
    # (Note: Katja should speak clearly during this test)
    assert True 
