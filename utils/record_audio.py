import speech_recognition as sr
import io


def record_audio():
    """
    V2: Records audio and returns a BytesIO object (RAM buffer) 
    instead of saving a file to disk.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[V2: Listening...]")
        # Faster noise adjustment for V2 (0.5s)
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            # Returns the raw WAV data as a stream in RAM
            return io.BytesIO(audio.get_wav_data())
        except Exception as e:
            print(f"[Recording Error]: {e}")
            return None
