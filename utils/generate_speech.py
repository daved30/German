import edge_tts
import os

async def generate_speech(text):
    """Converts text to speech and plays it via afplay."""
    if not text:
        return
        
    try:
        # Clean text
        clean_text = text.replace('*', '').replace('_', '').strip()
        
        # Neural Voice
        communicate = edge_tts.Communicate(clean_text, "de-DE-KatjaNeural")
        await communicate.save("response.mp3")
        
        # Play via native Mac afplay
        print("[Playing AI Response...]")
        os.system("afplay response.mp3")
        
    except Exception as e:
        print(f"[TTS Error]: {e}")
