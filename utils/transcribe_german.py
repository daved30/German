import whisper
import os
import warnings

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# Load model globally so it stays in RAM between calls
print("Loading Whisper 'medium' model...")
WHISPER_MODEL = whisper.load_model("medium")

def transcribe_german(filepath="test_input.wav"):
    """Converts a wav file into German text."""
    if not os.path.exists(filepath):
        return None
    try:
        result = WHISPER_MODEL.transcribe(filepath, language="de")
        return result["text"].strip()
    except Exception as e:
        print(f"[Transcription Error]: {e}")
        return None
