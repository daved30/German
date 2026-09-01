import edge_tts
import os
import uuid


async def generate_speech(text):
    if not text or len(text.strip()) < 2:
        return None

    unique_id = uuid.uuid4().hex
    filename = os.path.abspath(
        f"response_{unique_id}.mp3")  # Use absolute path

    try:
        clean_text = text.replace('*', '').replace('_', '').strip()
        communicate = edge_tts.Communicate(clean_text, "de-DE-KatjaNeural")
        await communicate.save(filename)
        return filename
    except Exception as e:
        print(f"[TTS Error]: {e}")
        return None
