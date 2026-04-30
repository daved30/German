import asyncio      # Handles the timing for the voice engine
import os           # Used to play the audio files on your Mac
import whisper      # The 'brain' that turns your German speech into text
import ollama       # Connects to your local glm4:9b model
import edge_tts     # The high-quality German voice engine
import speech_recognition as sr  # Handles your AirPods/Microphone input

def record_test_audio():
    """Records audio from the mic and saves it to a file for verification."""
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n[Adjusting for background noise... please wait 1 second]")
        r.adjust_for_ambient_noise(source, duration=1)
        
        print("[Recording started: Speak German now!]")
        try:
            # timeout: how long it waits for you to start
            # phrase_time_limit: max length of your sentence
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            
            with open("test_input.wav", "wb") as f:
                f.write(audio.get_wav_data())
            print("[Success: 'test_input.wav' has been created!]")
            
        except sr.WaitTimeoutError:
            print("[Error: No speech detected within 5 seconds]")
        except Exception as e:
            print(f"[Error during recording]: {e}")
            
# 1. Load the model once at the top level
print("Loading Whisper 'small' model... (this may take a moment)")
WHISPER_MODEL = whisper.load_model("small")

def transcribe_german_audio(file_path="test_input.wav"):
    """Converts the recorded wav file into German text."""
    try:
        print(f"[Transcribing {file_path}...]")
        
        # 2. The critical fix: language='de' forces German mode
        result = WHISPER_MODEL.transcribe(file_path, language="de")
        
        text = result["text"].strip()
        print(f"Whisper heard: {text}")
        return text
        
    except Exception as e:
        print(f"[Transcription Error]: {e}")
        return None

# Update your test block to run both:
if __name__ == "__main__":
    record_test_audio()
    transcribe_german_audio()