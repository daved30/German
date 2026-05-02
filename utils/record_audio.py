import speech_recognition as sr

def record_audio(filepath="test_input.wav"):
    """Records audio from the mic and saves to a file."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Adjusting for noise... wait 1s]")
        r.adjust_for_ambient_noise(source, duration=1)
        print("[Recording started: Speak German now!]")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            with open(filepath, "wb") as f:
                f.write(audio.get_wav_data())
            return True
        except Exception as e:
            print(f"[Recording Error]: {e}")
            return False
