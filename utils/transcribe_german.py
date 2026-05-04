import whisper
import os

WHISPER_MODEL = whisper.load_model("medium")


def transcribe_german(audio_stream):
    if audio_stream is None:
        return None
    try:
        # CRITICAL: Always rewind the RAM buffer before reading
        audio_stream.seek(0)

        with open("v2_temp.wav", "wb") as f:
            f.write(audio_stream.read())

        result = WHISPER_MODEL.transcribe("v2_temp.wav", language="de")
        return result["text"].strip()
    except Exception as e:
        print(f"[Transcription Error]: {e}")
        return None
